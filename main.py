#!/usr/bin/env python3
"""
Secure Bank - Main Entry Point
A console-based banking application with file storage
"""

import os
import sys
from auth.login import LoginManager
from auth.signup import SignupManager
from auth.session import SessionManager
from banking.account import AccountManager
from banking.transfer import TransferManager
from banking.transactions import TransactionManager
from utils.file_handler import FileHandler

class SecureBankApp:
    """Main application class for Secure Bank"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.login_manager = LoginManager()
        self.signup_manager = SignupManager()
        self.account_manager = AccountManager()
        self.transfer_manager = TransferManager()
        self.transaction_manager = TransactionManager()
        
        # Ensure data directory exists
        FileHandler.ensure_data_directory()
    
    def display_welcome(self):
        """Display welcome message and bank logo"""
        print("\n" + "="*60)
        print("🏦  WELCOME TO SECURE BANK  🏦")
        print("="*60)
        print("Your trusted partner for secure banking operations")
        print("="*60)
        print("💡 Security Note: Passwords are hidden when typing (no characters shown)")
        print("="*60)
    
    def display_main_menu(self):
        """Display main authentication menu"""
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. 🔐 Login to Account")
        print("2. 📝 Create New Account")
        print("3. ❌ Exit")
        print("-" * 30)
    
    def display_banking_menu(self):
        """Display banking operations menu"""
        current_user = self.session_manager.get_current_user()
        print(f"\n💼 BANKING DASHBOARD - Welcome, {current_user['name']}!")
        print("-" * 50)
        print("1. 💰 Check Balance")
        print("2. 💵 Deposit Money")
        print("3. 💸 Withdraw Money")
        print("4. 🔄 Transfer Money")
        print("5. 📊 Transaction History")
        print("6. 📄 Account Statement")
        print("7. 🔑 Change Password")
        print("8. ⚠️  Close Account")
        print("9. 🚪 Logout")
        print("-" * 50)
    
    def handle_main_menu(self):
        """Handle main menu operations"""
        while True:
            self.display_main_menu()
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                if self.login_manager.login():
                    self.handle_banking_menu()
            elif choice == '2':
                self.signup_manager.signup()
            elif choice == '3':
                print("\n👋 Thank you for using Secure Bank!")
                print("Have a great day! 🌟")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please select 1-3.")
    
    def handle_banking_menu(self):
        """Handle banking operations menu"""
        while self.session_manager.is_logged_in():
            self.display_banking_menu()
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == '1':
                self.account_manager.check_balance()
            elif choice == '2':
                self.account_manager.deposit()
            elif choice == '3':
                self.account_manager.withdraw()
            elif choice == '4':
                self.transfer_manager.transfer_money()
            elif choice == '5':
                self.transaction_manager.show_transaction_history()
            elif choice == '6':
                self.transaction_manager.generate_account_statement()
            elif choice == '7':
                self.account_manager.change_password()
            elif choice == '8':
                if self.account_manager.close_account():
                    break
            elif choice == '9':
                self.session_manager.logout()
                print("✅ Successfully logged out!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
    
    def run(self):
        """Main application loop"""
        try:
            self.display_welcome()
            self.handle_main_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    app = SecureBankApp()
    app.run()
