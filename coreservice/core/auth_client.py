import os
import httpx
from fastapi import HTTPException, status

IAM_BASE_URL = os.getenv("IAM_BASE_URL", "http://127.0.0.1:8000")


async def verify_token_with_iam(token: str) -> dict:
    url = f"{IAM_BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}

    print(">>> [CORE] Calling IAM:", url)
    print(">>> [CORE] Auth header starts with:", headers["Authorization"][:20])

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
    except httpx.RequestError as e:
        print(">>> [CORE] IAM request error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IAM service is not reachable",
        )

    print(">>> [CORE] IAM status:", resp.status_code)
    print(">>> [CORE] IAM body:", resp.text)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return resp.json()
