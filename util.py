from pydantic import BaseModel

def get_version():
    return "1.0.0"

def get_user_agent():
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

class IndexResponse(BaseModel):
    msg: str = None
    version: str = None
    userAgent: str = None

class HealthResponse(BaseModel):
    status: str = None 