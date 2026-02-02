from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from typing import Optional

# Security Scheme
security = HTTPBearer()

# Configuration
BETTER_AUTH_SECRET = os.environ.get("BETTER_AUTH_SECRET", "dev_secret_key")
ALGORITHM = "HS256"

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Decodes the JWT token and returns the user_id.
    """
    token = credentials.credentials
    print(f"DEBUG: Received token: {token[:10]}...") # Log start of token
    try:
        # Debugging: Print secret (partial) to ensure it matches expectation (careful in prod)
        # print(f"DEBUG: Secret using: {BETTER_AUTH_SECRET[:5]}...") 
        
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        print(f"DEBUG: Decoded payload: {payload}")
        
        user_id: str = payload.get("sub") 
        if user_id is None:
             print("DEBUG: No 'sub' in payload")
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_id
    except JWTError as e:
        print(f"DEBUG: JWT Decode Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
        )
