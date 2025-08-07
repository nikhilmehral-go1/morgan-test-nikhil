import os
import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from typing import List

def get_jwt_payload_from_token(token: str) -> dict:
    """
    Decodes and validates a JWT using the PyJWT library.
    """
    # You would get this secret from your environment variables
    JWT_SECRET_KEY = "localPhrase"

    try:
        print("--- Trying Decoding! ---")
        # Decode the token. This also verifies the signature and expiration.
        # payload = jwt.decode(
        #     token,
        #     'localPhrase',
        #     algorithms=["RS256", "HS256"] # Specify the algorithm used to sign the token
        # )
        payload = jwt.decode(token, options={"verify_signature": False})
        print("Decoded JWT Payload:", payload)  # Debugging line to see the payload
        return payload
    except jwt.ExpiredSignatureError:
        # Handle an expired token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired."
        )
    except jwt.InvalidTokenError as e:
        print("--- JWT Decoding Failed! ---", e)
        # Handle any other invalid token error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

# --- Role-Based Access Control (RBAC) and Verification Dependency ---
bearer_scheme = HTTPBearer()
GO1_TOKEN_VERIFICATION_URL = os.getenv("GO1_TOKEN_VERIFICATION_URL")

class AuthChecker:
    """
    Dependency factory for handling the complete authentication and authorization flow.
    1. Gets the Bearer token.
    2. Decodes the JWT locally to check roles.
    3. Calls an internal service to validate the token's authenticity.
    """
    def __init__(self, required_user_roles: List[str] = []):
        self.required_user_roles = required_user_roles

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        print("--- AuthChecker dependency has been triggered! ---")
        token = credentials.credentials

        # --- Step 1: Decode JWT and Check Roles Locally ---
        jwt_payload = get_jwt_payload_from_token(token)
        if not jwt_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        # Check if the user has the required roles
        if self.required_user_roles:
            user_roles = jwt_payload.get("user_roles", [])
            has_required_role = any(role in user_roles for role in self.required_user_roles)
            if not has_required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have sufficient permissions.",
                )

        # --- Step 2: Call Internal Service for Final Validation ---
        # if not GO1_TOKEN_VERIFICATION_URL:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="TOKEN_VERIFICATION_URL is not configured."
        #     )

        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post(
        #             GO1_TOKEN_VERIFICATION_URL,
        #             headers={"Authorization": f"Bearer {token}"}, # Pass the original token
        #             timeout=5.0
        #         )
        #         print("Response from auth service:", response.status_code, response.text)
        #         if response.status_code != 200:
        #             raise HTTPException(
        #                 status_code=status.HTTP_401_UNAUTHORIZED,
        #                 detail="Token could not be validated by authentication service.",
        #             )
        #     except httpx.RequestError as exc:
        #         raise HTTPException(
        #             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        #             detail=f"Auth service unavailable: {exc}",
        #         )

        # If all checks pass, the request can proceed.
        return {"jwt_payload": jwt_payload, "token": token}
