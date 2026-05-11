import bcrypt


def verify_hash(plain_text: str, hashed_text: str) -> bool:
    return bcrypt.checkpw(plain_text.encode(), hashed_text.encode())
