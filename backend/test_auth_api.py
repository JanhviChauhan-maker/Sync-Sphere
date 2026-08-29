import httpx
import asyncio

async def test_auth():
    async with httpx.AsyncClient(base_url="http://localhost:8000/v1") as client:
        print("Testing /docs")
        docs_res = await client.get("/docs")
        print("Docs Status:", docs_res.status_code)

        print("\nTesting /auth/login with random email")
        login_res = await client.post("/auth/login", json={"email": "random@test.com", "password": "password"})
        print("Login Status:", login_res.status_code)
        
        # We expect a 401 because the user shouldn't exist, but NOT a 500 error!
        if login_res.status_code == 500:
            print("Login failed with 500!")
            print(login_res.text)
        else:
            print("Login handled properly!")
            print(login_res.json())

        print("\nTesting /auth/register with random email")
        reg_res = await client.post("/auth/register", json={
            "email": "random3@test.com", 
            "password": "Password123!", 
            "first_name": "Test", 
            "last_name": "User",
            "org_name": "Org",
            "org_slug": "org5"
        })
        print("Register Status:", reg_res.status_code)
        if reg_res.status_code == 500:
            print("Register failed with 500!")
            print(reg_res.text)
        else:
            print("Register handled properly!")
            print(reg_res.json())

if __name__ == "__main__":
    asyncio.run(test_auth())
