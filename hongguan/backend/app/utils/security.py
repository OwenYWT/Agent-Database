from fastapi import HTTPException, Header

async def authenticate_user(authorization: str = Header(None)):
    if not authorization or not validate_token(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {'user_id': '12345'}  # 返回用户信息

def validate_token(token):
    # 验证令牌的逻辑
    return True
