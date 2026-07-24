"""
Utility module for generating unique, cryptographically secure short codes.
"""

import secrets
import string

from .models import ShortURL

# The "alphabet" for our short codes: a-z, A-Z, 0-9.
# 62 characters total.
ALPHABET = string.ascii_letters + string.digits  # 'abc...xyzABC...XYZ012...789'

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random short code of the given length.
    
    Why length 6?
    62^6 = ~56.8 billion unique combinations.
    For a personal/MVP project, this is more than enough.
    For bit.ly scale, you would use 7 or 8, or switch to Base62 incremental encoding.
    
    Why secrets.choice instead of random.choice?
    random uses a pseudo-random number generator (predictable).
    secrets uses the OS's cryptographically strong random source.
    """
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def generate_unique_short_code(length: int = 6, max_attempts: int = 10) -> str:
    """
    Generate a short code and ensure it does not already exist in the database.
    
    We use max_attempts as a safety guard. In theory, with 56 billion combinations,
    collisions are astronomically rare. But in software engineering, we always guard
    against infinite loops.
    """
    for attempt in range(max_attempts):
        code = generate_short_code(length)
        
        # Check if this code already exists in the database.
        # .exists() is optimized: it runs SELECT 1 ... LIMIT 1 instead of fetching rows.
        if not ShortURL.objects.filter(short_code=code).exists():
            return code
    
    # If we somehow exhaust all attempts, raise an error.
    # In production, you might increase length or log this to Sentry.
    raise RuntimeError(
        f"Failed to generate a unique short code after {max_attempts} attempts. "
        "Consider increasing the code length."
    )