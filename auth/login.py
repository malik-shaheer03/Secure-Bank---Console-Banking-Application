"""
Login Manager - Handles user authentication
"""

import getpass
import sys
from utils.file_handler import FileHandler
from utils.password_utils import PasswordUtils
from auth.session import SessionManager

class LoginManager:
    """Manages user login operations"""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    def login(self):
        """Handle user login process"""
        print("\n🔐 LOGIN TO YOUR ACCOUNT")
        print("-" * 30)
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                username = input("Username: ").strip().lower()
                if not username:
                    print("❌ Username cannot be empty.")
                    continue
                
                # Use getpass for secure password input
                try:
                    print("💡 Note: Password will be hidden for security (no characters will be shown)")
                    password = getpass.getpass("Password: ")
                except Exception as e:
                    # Fallback for environments where getpass doesn't work
                    print("⚠️  Secure input not available, password will be visible:")
                    password = input("Password: ")
                
                if not password:
                    print("❌ Password cannot be empty.")
                    continue
                
                if self._authenticate_user(username, password):
                    print(f"✅ Login successful! Welcome back!")
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"❌ Invalid credentials. {remaining} attempts remaining.")
                    else:
                        print("❌ Maximum login attempts exceeded. Please try again later.")
                        return False
                        
            except KeyboardInterrupt:
                print("\n❌ Login cancelled.")
                return False
            except Exception as e:
                print(f"❌ Login error: {e}")
                return False
        
        return False
    
    def _authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            users_data = FileHandler.load_users()
            
            if username not in users_data:
                return False
            
            user_data = users_data[username]
            stored_hash = user_data.get('password_hash')
            
            if PasswordUtils.verify_password(password, stored_hash):
                self.session_manager.create_session(username, user_data)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
