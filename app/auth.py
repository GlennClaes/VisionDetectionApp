import hashlib

SALT = b'salt1234'

class Auth:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            SALT,
            100_000
        ).hex()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return Auth.hash_password(password) == password_hash