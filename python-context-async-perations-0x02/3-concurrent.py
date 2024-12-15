import aiosqlite
import asyncio

DATABASE = "alx_prodev.db"  

async def async_fetch_all_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM user_data") as cursor:
            rows = await cursor.fetchall()
            print("Results of all users")
            for row in rows:
                print({"id": row[0], "name": row[1], "age": row[2]})
            return rows

async def async_fetch_users_older_than_40():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM user_data WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("\nResults of users older than 40")
            for row in rows:
                print({"id": row[0], "name": row[1], "age": row[2]})
            return rows

async def fetch_concurrently():
    
    results = await asyncio.gather(
        async_fetch_all_users(),
        async_fetch_users_older_than_40()
    )
    return results


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())