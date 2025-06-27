"""
Account Manager - Handles basic account operations
"""

import getpass
from utils.file_handler import FileHandler
from utils.password_utils import PasswordUtils
from auth.session import SessionManager

class AccountManager:
    """Manages basic account operations"""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    def check_balance(self):
        """Display current account balance"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            # Get fresh balance from file
            users_data = FileHandler.load_users()
            username = current_user['username']
            balance = users_data[username]['balance']
            
            print(f"\n💰 ACCOUNT BALANCE")
            print("-" * 25)
            print(f"Current Balance: ${balance:.2f}")
            print("-" * 25)
            
            # Update session balance
            self.session_manager.update_session_balance(balance)
            
        except Exception as e:
            print(f"❌ Error checking balance: {e}")
    
    def deposit(self):
        """Handle money deposit"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            print(f"\n💵 DEPOSIT MONEY")
            print("-" * 20)
            
            while True:
                try:
                    amount = float(input("Enter deposit amount ($): "))
                    if amount <= 0:
                        print("❌ Deposit amount must be positive.")
                        continue
                    if amount > 10000:
                        print("❌ Maximum deposit limit is $10,000 per transaction.")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a valid amount.")
                    continue
            
            # Process deposit
            if self._process_deposit(current_user['username'], amount):
                print(f"✅ Successfully deposited ${amount:.2f}")
                self.check_balance()
            else:
                print("❌ Deposit failed. Please try again.")
                
        except Exception as e:
            print(f"❌ Error processing deposit: {e}")
    
    def withdraw(self):
        """Handle money withdrawal"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            print(f"\n💸 WITHDRAW MONEY")
            print("-" * 20)
            
            # Get current balance
            users_data = FileHandler.load_users()
            username = current_user['username']
            current_balance = users_data[username]['balance']
            
            print(f"Available Balance: ${current_balance:.2f}")
            
            while True:
                try:
                    amount = float(input("Enter withdrawal amount ($): "))
                    if amount <= 0:
                        print("❌ Withdrawal amount must be positive.")
                        continue
                    if amount > current_balance:
                        print("❌ Insufficient funds.")
                        continue
                    if amount > 5000:
                        print("❌ Maximum withdrawal limit is $5,000 per transaction.")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a valid amount.")
                    continue
            
            # Process withdrawal
            if self._process_withdrawal(username, amount):
                print(f"✅ Successfully withdrew ${amount:.2f}")
                self.check_balance()
            else:
                print("❌ Withdrawal failed. Please try again.")
                
        except Exception as e:
            print(f"❌ Error processing withdrawal: {e}")
    
    def change_password(self):
        """Handle password change"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            print(f"\n🔑 CHANGE PASSWORD")
            print("-" * 20)
            
            # Verify current password
            try:
                current_password = getpass.getpass("Enter current password: ")
            except Exception as e:
                print("⚠️  Secure input not available, password will be visible:")
                current_password = input("Enter current password: ")
            
            users_data = FileHandler.load_users()
            username = current_user['username']
            stored_hash = users_data[username]['password_hash']
            
            if not PasswordUtils.verify_password(current_password, stored_hash):
                print("❌ Current password is incorrect.")
                return
            
            # Get new password
            while True:
                try:
                    new_password = getpass.getpass("Enter new password: ")
                except Exception as e:
                    print("⚠️  Secure input not available, password will be visible:")
                    new_password = input("Enter new password: ")
                
                if len(new_password) < 6:
                    print("❌ Password must be at least 6 characters long.")
                    continue
                
                try:
                    confirm_password = getpass.getpass("Confirm new password: ")
                except Exception as e:
                    print("⚠️  Secure input not available, password will be visible:")
                    confirm_password = input("Confirm new password: ")
                
                if new_password != confirm_password:
                    print("❌ Passwords don't match.")
                    continue
                break
            
            # Update password
            new_hash = PasswordUtils.hash_password(new_password)
            users_data[username]['password_hash'] = new_hash
            FileHandler.save_users(users_data)
            
            print("✅ Password changed successfully!")
            
        except Exception as e:
            print(f"❌ Error changing password: {e}")
    
    def close_account(self):
        """Handle account closure"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return False
            
            print(f"\n⚠️  CLOSE ACCOUNT")
            print("-" * 20)
            print("⚠️  WARNING: This action cannot be undone!")
            
            # Confirm account closure
            confirm = input("Type 'CLOSE' to confirm account closure: ").strip()
            if confirm != 'CLOSE':
                print("❌ Account closure cancelled.")
                return False
            
            # Verify password
            password = getpass.getpass("Enter your password to confirm: ")
            users_data = FileHandler.load_users()
            username = current_user['username']
            stored_hash = users_data[username]['password_hash']
            
            if not PasswordUtils.verify_password(password, stored_hash):
                print("❌ Password verification failed.")
                return False
            
            # Close account
            users_data[username]['account_status'] = 'closed'
            users_data[username]['closed_at'] = FileHandler.get_current_timestamp()
            
            # Add closure transaction
            transaction = {
                'type': 'account_closure',
                'amount': 0,
                'description': 'Account closed by user',
                'timestamp': FileHandler.get_current_timestamp(),
                'balance_after': users_data[username]['balance']
            }
            users_data[username]['transactions'].append(transaction)
            
            FileHandler.save_users(users_data)
            
            print("✅ Account closed successfully.")
            print("Thank you for banking with us!")
            
            # Logout user
            self.session_manager.logout()
            return True
            
        except Exception as e:
            print(f"❌ Error closing account: {e}")
            return False
    
    def _process_deposit(self, username, amount):
        """Process deposit transaction"""
        try:
            users_data = FileHandler.load_users()
            
            # Update balance
            users_data[username]['balance'] += amount
            new_balance = users_data[username]['balance']
            
            # Add transaction record
            transaction = {
                'type': 'deposit',
                'amount': amount,
                'description': 'Cash deposit',
                'timestamp': FileHandler.get_current_timestamp(),
                'balance_after': new_balance
            }
            users_data[username]['transactions'].append(transaction)
            
            # Save changes
            FileHandler.save_users(users_data)
            
            # Update session
            self.session_manager.update_session_balance(new_balance)
            
            return True
            
        except Exception as e:
            print(f"❌ Deposit processing error: {e}")
            return False
    
    def _process_withdrawal(self, username, amount):
        """Process withdrawal transaction"""
        try:
            users_data = FileHandler.load_users()
            
            # Update balance
            users_data[username]['balance'] -= amount
            new_balance = users_data[username]['balance']
            
            # Add transaction record
            transaction = {
                'type': 'withdrawal',
                'amount': amount,
                'description': 'Cash withdrawal',
                'timestamp': FileHandler.get_current_timestamp(),
                'balance_after': new_balance
            }
            users_data[username]['transactions'].append(transaction)
            
            # Save changes
            FileHandler.save_users(users_data)
            
            # Update session
            self.session_manager.update_session_balance(new_balance)
            
            return True
            
        except Exception as e:
            print(f"❌ Withdrawal processing error: {e}")
            return False
