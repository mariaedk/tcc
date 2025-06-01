"""
@author maria
date: 2025-05-13
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

senha_hash = hash_password("pesquisa123")
print(senha_hash)
