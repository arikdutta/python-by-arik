import asyncio
import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"


async def fetch_post(client: httpx.AsyncClient, post_id: int) -> dict:
    response = await client.get(f"{BASE_URL}/posts/{post_id}")
    response.raise_for_status()
    return response.json()


async def fetch_user(client: httpx.AsyncClient, user_id: int) -> dict:
    response = await client.get(f"{BASE_URL}/users/{user_id}")
    response.raise_for_status()
    return response.json()


async def main():
    async with httpx.AsyncClient() as client:
        # Run multiple API calls concurrently
        post1, post2, user1 = await asyncio.gather(
            fetch_post(client, 1),
            fetch_post(client, 2),
            fetch_user(client, 1),
        )

    print("--- Post 1 ---")
    print(f"Title: {post1['title']}")

    print("\n--- Post 2 ---")
    print(f"Title: {post2['title']}")

    print("\n--- User 1 ---")
    print(f"Name:  {user1['name']}")
    print(f"Email: {user1['email']}")


if __name__ == "__main__":
    asyncio.run(main())
