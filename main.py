# Asyncio
import asyncio

# UVLoop
import uvloop

# Asyncpg
from asyncpg import create_pool as create_pg_pool

# Bot
from bot import bot

# Misc
import os

# Use uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def run_bot():
    await bot.loop()


async def make_pg_pool():
    dsn = os.environ.get('DATABASE_URL')
    return await create_pg_pool(
        dsn=dsn,
        min_size=5,
        max_size=10)

# Main event loop
loop = asyncio.get_event_loop()

# Attach postgres connection pool to bot
pg_pool = loop.run_until_complete(make_pg_pool())
setattr(bot, 'pg_pool', pg_pool)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == 'loop':
        loop.run_until_complete(run_bot())
    else:
        bot.run_webhook(os.environ.get('APP_URL') + 'webhook')
