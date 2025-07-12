import asyncio

async def get_all_users():
    await asyncio.sleep(5)
    all_users = [{"name":"watmon", "age": 24}, {"name": "okello", "age": 26}]
    print(all_users)

async def get_first_user():
    await asyncio.sleep(2)
    one_user = [{"name":"watmon", "age": 24}]
    print(one_user)

async def main():
    await asyncio.gather(
        get_all_users(), get_first_user(), get_name("Eric Jansen")
    )

async def get_name(name):
    await asyncio.sleep(0.1)
    print(name)

print("First line")
print("Second line")
asyncio.run(main())
print("Third line")
print("Last line")