"""
Transaction Manager - Handles transaction history and statements
"""

from utils.file_handler import FileHandler
from auth.session import SessionManager

class TransactionManager:
    """Manages transaction history and account statements"""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    def show_transaction_history(self):
        """Display transaction history"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            users_data = FileHandler.load_users()
            username = current_user['username']
            transactions = users_data[username].get('transactions', [])
            
            if not transactions:
                print("\n📊 No transactions found.")
                return
            
            print(f"\n📊 TRANSACTION HISTORY - {current_user['name']}")
            print("=" * 80)
            
            # Show recent transactions (last 20)
            recent_transactions = transactions[-20:]
            
            for i, transaction in enumerate(reversed(recent_transactions), 1):
                self._display_transaction(transaction, i)
            
            if len(transactions) > 20:
                print(f"\n... and {len(transactions) - 20} more transactions")
                print("Generate account statement for complete history.")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Error retrieving transaction history: {e}")
    
    def generate_account_statement(self):
        """Generate and display account statement"""
        try:
            current_user = self.session_manager.get_current_user()
            if not current_user:
                print("❌ Please log in first.")
                return
            
            users_data = FileHandler.load_users()
            username = current_user['username']
            user_data = users_data[username]
            transactions = user_data.get('transactions', [])
            
            # Generate statement
            statement = self._generate_statement_content(user_data, transactions)
            
            # Display statement
            print(statement)
            
            # Option to save to file
            save_option = input("\nSave statement to file? (y/n): ").strip().lower()
            if save_option == 'y':
                filename = f"statement_{username}_{FileHandler.get_current_timestamp().replace(':', '-').replace(' ', '_')}.txt"
                try:
                    with open(filename, 'w') as f:
                        f.write(statement)
                    print(f"✅ Statement saved as {filename}")
                except Exception as e:
                    print(f"❌ Error saving statement: {e}")
            
        except Exception as e:
            print(f"❌ Error generating statement: {e}")
    
    def _display_transaction(self, transaction, index):
        """Display a single transaction"""
        transaction_type = transaction['type']
        amount = transaction['amount']
        description = transaction['description']
        timestamp = transaction['timestamp']
        balance_after = transaction['balance_after']
        
        # Format transaction type
        type_symbols = {
            'deposit': '💵 ⬆️',
            'withdrawal': '💸 ⬇️',
            'transfer_in': '🔄 ⬆️',
            'transfer_out': '🔄 ⬇️',
            'account_closure': '❌'
        }
        
        symbol = type_symbols.get(transaction_type, '📝')
        
        # Format amount with sign
        if transaction_type in ['deposit', 'transfer_in']:
            amount_str = f"+${amount:.2f}"
        elif transaction_type in ['withdrawal', 'transfer_out']:
            amount_str = f"-${amount:.2f}"
        else:
            amount_str = f"${amount:.2f}"
        
        print(f"{index:2d}. {symbol} {transaction_type.replace('_', ' ').title()}")
        print(f"    Amount: {amount_str}")
        print(f"    Description: {description}")
        print(f"    Date: {timestamp}")
        print(f"    Balance After: ${balance_after:.2f}")
        print("-" * 80)
    
    def _generate_statement_content(self, user_data, transactions):
        """Generate complete account statement content"""
        statement_lines = []
        
        # Header
        statement_lines.append("=" * 80)
        statement_lines.append("🏦 SECURE BANK - ACCOUNT STATEMENT")
        statement_lines.append("=" * 80)
        statement_lines.append("")
        
        # Account information
        statement_lines.append("📋 ACCOUNT INFORMATION")
        statement_lines.append("-" * 40)
        statement_lines.append(f"Account Holder: {user_data['name']}")
        statement_lines.append(f"Username: {user_data.get('username', 'N/A')}")
        statement_lines.append(f"Account Status: {user_data.get('account_status', 'active').title()}")
        statement_lines.append(f"Current Balance: ${user_data['balance']:.2f}")
        statement_lines.append(f"Account Created: {user_data.get('created_at', 'N/A')}")
        statement_lines.append(f"Statement Generated: {FileHandler.get_current_timestamp()}")
        statement_lines.append("")
        
        # Transaction summary
        if transactions:
            total_deposits = sum(t['amount'] for t in transactions if t['type'] in ['deposit', 'transfer_in'])
            total_withdrawals = sum(t['amount'] for t in transactions if t['type'] in ['withdrawal', 'transfer_out'])
            
            statement_lines.append("📊 TRANSACTION SUMMARY")
            statement_lines.append("-" * 40)
            statement_lines.append(f"Total Transactions: {len(transactions)}")
            statement_lines.append(f"Total Deposits: ${total_deposits:.2f}")
            statement_lines.append(f"Total Withdrawals: ${total_withdrawals:.2f}")
            statement_lines.append(f"Net Amount: ${total_deposits - total_withdrawals:.2f}")
            statement_lines.append("")
        
        # Transaction details
        if transactions:
            statement_lines.append("📝 TRANSACTION DETAILS")
            statement_lines.append("-" * 80)
            
            for i, transaction in enumerate(reversed(transactions), 1):
                transaction_type = transaction['type']
                amount = transaction['amount']
                description = transaction['description']
                timestamp = transaction['timestamp']
                balance_after = transaction['balance_after']
                
                # Format amount with sign
                if transaction_type in ['deposit', 'transfer_in']:
                    amount_str = f"+${amount:.2f}"
                elif transaction_type in ['withdrawal', 'transfer_out']:
                    amount_str = f"-${amount:.2f}"
                else:
                    amount_str = f"${amount:.2f}"
                
                statement_lines.append(f"{i:3d}. {transaction_type.replace('_', ' ').title()}")
                statement_lines.append(f"     Amount: {amount_str}")
                statement_lines.append(f"     Description: {description}")
                statement_lines.append(f"     Date: {timestamp}")
                statement_lines.append(f"     Balance After: ${balance_after:.2f}")
                statement_lines.append("-" * 80)
        else:
            statement_lines.append("📝 No transactions found.")
            statement_lines.append("")
        
        # Footer
        statement_lines.append("")
        statement_lines.append("Thank you for banking with Secure Bank! 🏦")
        statement_lines.append("=" * 80)
        
        return "\n".join(statement_lines)
