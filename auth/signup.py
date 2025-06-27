"""
Signup Manager - Handles new user registration
"""

import getpass
import re
from utils.file_handler import FileHandler
from utils.password_utils import PasswordUtils

class SignupManager:
    """Manages user registration operations"""
    
    def signup(self):
        """Handle user registration process"""
        print("\n📝 CREATE NEW ACCOUNT")
        print("-" * 30)
        
        try:
            # Get user details
            user_data = self._collect_user_data()
            if not user_data:
                return False
            
            # Create account
            if self._create_account(user_data):
                print("✅ Account created successfully!")
                print(f"Welcome to Secure Bank, {user_data['name']}!")
                print(f"Your initial balance: ${user_data['balance']:.2f}")
                return True
            else:
                print("❌ Failed to create account. Please try again.")
                return False
                
        except KeyboardInterrupt:
            print("\n❌ Account creation cancelled.")
            return False
        except Exception as e:
            print(f"❌ Signup error: {e}")
            return False
    
    def _collect_user_data(self):
        """Collect and validate user registration data"""
        # Username
        while True:
            username = input("Choose a username: ").strip().lower()
            if not self._validate_username(username):
                continue
            if self._username_exists(username):
                print("❌ Username already exists. Please choose another.")
                continue
            break
        
        # Full name
        while True:
            name = input("Full name: ").strip().title()
            if not self._validate_name(name):
                continue
            break
        
        # Password
        while True:
            try:
                print("💡 Note: Password will be hidden for security (no characters will be shown)")
                password = getpass.getpass("Create password (6+ chars, letters + numbers): ")
            except Exception as e:
                # Fallback for environments where getpass doesn't work
                print("⚠️  Secure input not available, password will be visible:")
                password = input("Create password (6+ chars, letters + numbers): ")
            
            if not self._validate_password(password):
                continue
            
            try:
                confirm_password = getpass.getpass("Confirm password: ")
            except Exception as e:
                # Fallback for environments where getpass doesn't work
                print("⚠️  Secure input not available, password will be visible:")
                confirm_password = input("Confirm password: ")
            
            if password != confirm_password:
                print("❌ Passwords don't match. Please try again.")
                continue
            break
        
        # Initial deposit
        while True:
            try:
                deposit = float(input("Initial deposit amount ($): "))
                if deposit < 0:
                    print("❌ Initial deposit cannot be negative.")
                    continue
                if deposit < 10:
                    print("❌ Minimum initial deposit is $10.00.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid amount.")
                continue
        
        return {
            'username': username,
            'name': name,
            'password': password,
            'balance': deposit
        }
    
    def _validate_username(self, username):
        """Validate username format"""
        if len(username) < 3:
            print("❌ Username must be at least 3 characters long.")
            return False
        if not re.match("^[a-zA-Z0-9_]+$", username):
            print("❌ Username can only contain letters, numbers, and underscores.")
            return False
        return True
    
    def _validate_name(self, name):
        """Validate full name"""
        if len(name.strip()) < 2:
            print("❌ Name must be at least 2 characters long.")
            return False
        if not re.match("^[a-zA-Z\s]+$", name):
            print("❌ Name can only contain letters and spaces.")
            return False
        return True
    
    def _validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long.")
            return False
        if not re.search(r"[A-Za-z]", password):
            print("❌ Password must contain at least one letter.")
            return False
        if not re.search(r"\d", password):
            print("❌ Password must contain at least one number.")
            return False
        return True
    
    def _username_exists(self, username):
        """Check if username already exists"""
        try:
            users_data = FileHandler.load_users()
            return username in users_data
        except:
            return False
    
    def _create_account(self, user_data):
        """Create new user account"""
        try:
            users_data = FileHandler.load_users()
            
            # Hash password
            password_hash = PasswordUtils.hash_password(user_data['password'])
            
            # Create user record
            users_data[user_data['username']] = {
                'name': user_data['name'],
                'password_hash': password_hash,
                'balance': user_data['balance'],
                'account_status': 'active',
                'created_at': FileHandler.get_current_timestamp(),
                'transactions': []
            }
            
            # Save to file
            FileHandler.save_users(users_data)
            
            # Log initial deposit transaction
            if user_data['balance'] > 0:
                transaction = {
                    'type': 'deposit',
                    'amount': user_data['balance'],
                    'description': 'Initial deposit',
                    'timestamp': FileHandler.get_current_timestamp(),
                    'balance_after': user_data['balance']
                }
                users_data[user_data['username']]['transactions'].append(transaction)
                FileHandler.save_users(users_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating account: {e}")
            return False
