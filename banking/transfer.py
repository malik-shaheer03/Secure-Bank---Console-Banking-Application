"""
Transfer Manager - Handles money transfers between accounts
"""

from utils.file_handler import FileHandler
from auth.session import SessionManager

class TransferManager:
    """Manages money transfer operations"""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    def transfer_money(self):
        """Handle money transfer between accounts"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            print(f"\n🔄 TRANSFER MONEY")
            print("-" * 20)
            
            # Get recipient username
            recipient_username = input("Enter recipient's username: ").strip().lower()
            if not recipient_username:
                print("❌ Recipient username cannot be empty.")
                return
            
            if recipient_username == current_user['username']:
                print("❌ Cannot transfer money to yourself.")
                return
            
            # Check if recipient exists
            users_data = FileHandler.load_users()
            if recipient_username not in users_data:
                print("❌ Recipient account not found.")
                return
            
            # Check if recipient account is active
            if users_data[recipient_username].get('account_status') != 'active':
                print("❌ Recipient account is not active.")
                return
            
            # Get current balance
            sender_username = current_user['username']
            sender_balance = users_data[sender_username]['balance']
            recipient_name = users_data[recipient_username]['name']
            
            print(f"Transferring to: {recipient_name}")
            print(f"Your available balance: ${sender_balance:.2f}")
            
            # Get transfer amount
            while True:
                try:
                    amount = float(input("Enter transfer amount ($): "))
                    if amount <= 0:
                        print("❌ Transfer amount must be positive.")
                        continue
                    if amount > sender_balance:
                        print("❌ Insufficient funds.")
                        continue
                    if amount > 10000:
                        print("❌ Maximum transfer limit is $10,000 per transaction.")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a valid amount.")
                    continue
            
            # Get transfer description
            description = input("Transfer description (optional): ").strip()
            if not description:
                description = f"Transfer to {recipient_name}"
            
            # Confirm transfer
            print(f"\n📋 TRANSFER CONFIRMATION")
            print("-" * 30)
            print(f"From: {current_user['name']} ({sender_username})")
            print(f"To: {recipient_name} ({recipient_username})")
            print(f"Amount: ${amount:.2f}")
            print(f"Description: {description}")
            print("-" * 30)
            
            confirm = input("Confirm transfer? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Transfer cancelled.")
                return
            
            # Process transfer
            if self._process_transfer(sender_username, recipient_username, amount, description):
                print("✅ Transfer completed successfully!")
                print(f"${amount:.2f} transferred to {recipient_name}")
                
                # Show updated balance
                updated_balance = users_data[sender_username]['balance'] - amount
                print(f"Your new balance: ${updated_balance:.2f}")
                self.session_manager.update_session_balance(updated_balance)
            else:
                print("❌ Transfer failed. Please try again.")
                
        except Exception as e:
            print(f"❌ Error processing transfer: {e}")
    
    def _process_transfer(self, sender_username, recipient_username, amount, description):
        """Process the money transfer"""
        try:
            users_data = FileHandler.load_users()
            
            # Update sender balance
            users_data[sender_username]['balance'] -= amount
            sender_new_balance = users_data[sender_username]['balance']
            
            # Update recipient balance
            users_data[recipient_username]['balance'] += amount
            recipient_new_balance = users_data[recipient_username]['balance']
            
            # Create timestamp
            timestamp = FileHandler.get_current_timestamp()
            
            # Add transaction to sender
            sender_transaction = {
                'type': 'transfer_out',
                'amount': amount,
                'description': f"{description} (to {users_data[recipient_username]['name']})",
                'recipient': recipient_username,
                'timestamp': timestamp,
                'balance_after': sender_new_balance
            }
            users_data[sender_username]['transactions'].append(sender_transaction)
            
            # Add transaction to recipient
            recipient_transaction = {
                'type': 'transfer_in',
                'amount': amount,
                'description': f"{description} (from {users_data[sender_username]['name']})",
                'sender': sender_username,
                'timestamp': timestamp,
                'balance_after': recipient_new_balance
            }
            users_data[recipient_username]['transactions'].append(recipient_transaction)
            
            # Save changes
            FileHandler.save_users(users_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Transfer processing error: {e}")
            return False
