#totp implementation

import hmac
import hashlib
import time
import base64

def generate_secret(length=20):
    import secrets
    random_bytes = secrets.token_bytes(length)
    return base64.b32encode(random_bytes).decode('utf-8').rstrip('=')

def _bytearray_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')