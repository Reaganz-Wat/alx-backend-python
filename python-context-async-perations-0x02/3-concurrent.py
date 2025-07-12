import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("../python-decorators-0x01/users.db") as db:
        try:
            cursor = await db.execute("SELECT * FROM users")
            users = await cursor.fetchall()
            print(f"All users: {users}")
            return users
        except Exception as e:
            print(f"Error: {e}")

async def async_fetch_older_users():
    async with aiosqlite.connect("../python-decorators-0x01/users.db") as db:
        try:
            cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
            results = await cursor.fetchall()
            print(f"Users with age greater than 40: {results}")
            return results
        except aiosqlite.OperationalError as e:
            print(f"Error: {e}")

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )

asyncio.run(fetch_concurrently())