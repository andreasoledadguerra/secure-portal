#totp implementation

import hmac
import hashlib
import time
import base64
import secrets

from app.core.config import settings

def generate_secret(length=20):
    raw = secrets.token_bytes(length)
    return base64.b32encode(raw).decode('utf-8').rstrip('=')

def _hotp(secret_bytes: bytes, counter: int, digits: int = 6) -> str:
    counter_bytes = counter.to_bytes(8, byteorder="big")
    hmac_result = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
    offset = hmac_result[-1] & 0x0F
    binary = int.from_bytes(hmac_result[offset:offset + 4], byteorder="big") & 0x7FFFFFFF
    otp = binary % (10 ** digits)
    return str(otp).zfill(digits)


def _generate_totp(secret_base32: str, interval: int = 30, digits: int = 6):
    secret_bytes = base64.b32decode(secret_base32 + "=" * ((8 - len(secret_base32) % 8) % 8))
    counter = int(time.time()) // settings.TOTP_INTERVAL_SECONDS
    return _hotp(secret_bytes, counter, settings.TOTP_DIGITS)

def verify_totp(secret_base32: str, code: str, interval: int = 30, digits: int = 6, window: int = 1) -> bool:
    secret_bytes = base64.b32decode(secret_base32 + "=" * ((8 - len(secret_base32) % 8) % 8))
    current_counter = int(time.time()) // settings.TOTP_INTERVAL_SECONDS
    for offset in range(-settings.TOTP_WINDOW, settings.TOTP_WINDOW + 1):
        if hmac.compare_digest(_hotp(secret_bytes, current_counter + offset, settings.TOTP_DIGITS), code):
            return True
    return False

#"""Generate URI otpauth:// for QR."""
def generate_otpauth_uri(secret_base32, email, issuer="SVP"):
    return (
        f"otpauth://totp/{issuer}:{email}"
        f"?secret={secret_base32}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
    )