# -*- coding: utf-8 -*-
"""
Secure encryption module using Python's cryptography library.
Uses Fernet (AES-128-CBC + HMAC-SHA256) with PBKDF2 key derivation.
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Salt for key derivation (can be customized per deployment)
DEFAULT_SALT = b"grafdedades_salt_v2"
ITERATIONS = 100_000


def derive_key(password: str, salt: bytes = DEFAULT_SALT) -> bytes:
    """
    Derive a Fernet-compatible key from a password using PBKDF2.
    
    Args:
        password: The user's password
        salt: Salt for key derivation (default: application-specific salt)
    
    Returns:
        URL-safe base64-encoded 32-byte key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def derive_key_legacy(password: str) -> bytes:
    """
    Legacy key derivation matching the old Node.js implementation.
    Only use for migrating old data.
    
    Args:
        password: The user's password
    
    Returns:
        URL-safe base64-encoded key (old format)
    """
    # Old method: password.repeat(50).substring(0, 43) + "="
    repeated = (password * 50)[:43] + "="
    return repeated.encode()


def encrypt(data: str, password: str, use_legacy: bool = False) -> str:
    """
    Encrypt data using Fernet encryption.
    
    Args:
        data: The plaintext data to encrypt
        password: The encryption password
        use_legacy: If True, use legacy key derivation (for compatibility)
    
    Returns:
        Encrypted data as a string
    """
    if use_legacy:
        key = derive_key_legacy(password)
    else:
        key = derive_key(password)
    
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted.decode()


def decrypt(encrypted_data: str, password: str, use_legacy: bool = False) -> str:
    """
    Decrypt Fernet-encrypted data.
    
    Args:
        encrypted_data: The encrypted data string
        password: The decryption password
        use_legacy: If True, use legacy key derivation (for old data)
    
    Returns:
        Decrypted plaintext data
    
    Raises:
        cryptography.fernet.InvalidToken: If password is wrong or data corrupted
    """
    if use_legacy:
        key = derive_key_legacy(password)
    else:
        key = derive_key(password)
    
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data.encode())
    return decrypted.decode()


def migrate_encryption(encrypted_data: str, password: str) -> str:
    """
    Migrate data from legacy encryption to new PBKDF2-based encryption.
    
    Args:
        encrypted_data: Data encrypted with legacy key derivation
        password: The password (same for both old and new)
    
    Returns:
        Data re-encrypted with new secure key derivation
    """
    # Decrypt with old key
    plaintext = decrypt(encrypted_data, password, use_legacy=True)
    # Re-encrypt with new key
    return encrypt(plaintext, password, use_legacy=False)
