from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(time_cost=4, memory_cost=2 ** 16, parallelism=4)


def hash_password(password: str) -> str:
    return ph.hash(password)


def check_password(hashed: str, password: str) -> bool:
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False


def needs_rehash(hashed: str) -> bool:
    return ph.check_needs_rehash(hashed)
