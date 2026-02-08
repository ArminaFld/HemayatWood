from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.auth_client import verify_token_with_iam

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    return await verify_token_with_iam(token)
