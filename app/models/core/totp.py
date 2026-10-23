#totp implementation

import hmac
import hashlib
import time
import base64
import secrets

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


def _generate_totp(secret_bytes, interval=30, digits=6):
    # Calcular el contador de tiempo
    counter = int(time.time()) // interval
    counter_bytes = counter.to_bytes(8, byteorder='big')
    # HMAC-SHA1
    hmac_result = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
    # Dynamic truncation
    offset = hmac_result[-1] & 0x0f
    binary = _bytearray_to_int(hmac_result[offset:offset+4]) & 0x7fffffff
    # Generar los dígitos
    otp = binary % (10 ** digits)
    return str(otp).zfill(digits)

def verify_totp(secret_base32, code, interval=30, window=1):
    secret_bytes = base64.b32decode(secret_base32 + '=' * ((8 - len(secret_base32) % 8) % 8))  # añadir padding si es necesario
    current_interval = int(time.time()) // interval
    for i in range(-window, window+1):
        # Calculamos el counter para el intervalo actual + i
        counter = current_interval + i
        counter_bytes = counter.to_bytes(8, byteorder='big')
        hmac_result = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
        offset = hmac_result[-1] & 0x0f
        binary = _bytearray_to_int(hmac_result[offset:offset+4]) & 0x7fffffff
        otp = str(binary % (10 ** 6)).zfill(6)
        if hmac.compare_digest(otp, code):
            return True
    return False

def generate_totp_uri(secret_base32, email, issuer="SVP"):
    """Generate URI otpauth:// for QR."""
    return f"otpauth://totp/{issuer}:{email}?secret={secret_base32}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
