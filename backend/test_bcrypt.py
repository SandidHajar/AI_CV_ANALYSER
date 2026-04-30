from passlib.context import CryptContext
import sys

try:
    pc = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pw = "password123"
    h = pc.hash(pw)
    print(f"Password: {pw}")
    print(f"Hash: {h}")
    v = pc.verify(pw, h)
    print(f"Verify: {v}")
except Exception as e:
    print(f"Error: {e}")
