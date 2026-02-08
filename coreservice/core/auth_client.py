import httpx
from fastapi import HTTPException, status

IAM_BASE_URL = "http://iam:8000"  # داخل docker

async def verify_token_with_iam(token: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{IAM_BASE_URL}/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توکن نامعتبر است.",
            )

        return resp.json()

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="سرویس IAM در دسترس نیست.",
        )
