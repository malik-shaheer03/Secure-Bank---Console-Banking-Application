"""
Password Utilities - Handles password hashing and verification
"""

import hashlib
import os
import base64

class PasswordUtils:
    """Utilities for password hashing and verification"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256 with salt"""
        # Generate a random salt
        salt = os.urandom(32)
        
        # Hash the password with salt
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt, 
                                          100000)  # 100,000 iterations
        
        # Combine salt and hash, then encode as base64 string for JSON storage
        combined = salt + password_hash
        return base64.b64encode(combined).decode('utf-8')
    
    @staticmethod
    def verify_password(password, stored_hash_b64):
        """Verify password against stored hash"""
        try:
            # Decode the base64 string back to bytes
            stored_hash = base64.b64decode(stored_hash_b64.encode('utf-8'))
            
            # Extract salt (first 32 bytes) and hash (rest)
            salt = stored_hash[:32]
            stored_password_hash = stored_hash[32:]
            
            # Hash the provided password with the same salt
            password_hash = hashlib.pbkdf2_hmac('sha256',
                                              password.encode('utf-8'),
                                              salt,
                                              100000)
            
            # Compare hashes
            return password_hash == stored_password_hash
            
        except Exception as e:
            print(f"❌ Password verification error: {e}")
            return False
