import hashlib
import secrets

from pwdlib import PasswordHash

# Argon2id with library-recommended parameters.
_password_hash = PasswordHash.recommended()
# Used to keep login timing similar when the user does not exist.
_DUMMY_HASH = _password_hash.hash("dummy-password-for-timing")

MIN_PASSWORD_LENGTH = 8


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    if password_hash is None:
        _password_hash.verify(password, _DUMMY_HASH)
        return False
    return _password_hash.verify(password, password_hash)


def new_token() -> str:
    """Random opaque token for sessions and password resets."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Tokens are stored only as SHA-256 hashes (they are high-entropy, so no salt needed)."""
    return hashlib.sha256(token.encode()).hexdigest()


def password_problem(password: str) -> str | None:
    """Return a human-readable reason if the password is too weak, else None."""
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
    if password.isdigit() or password.isalpha():
        return "Password must contain both letters and numbers or symbols."
    return None
