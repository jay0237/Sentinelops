from fastapi import Header, HTTPException

API_KEY = "sentinelops-secret-key"

def verify_api_key(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401,
        details="Invalid API key"
        )

        return x_api_key