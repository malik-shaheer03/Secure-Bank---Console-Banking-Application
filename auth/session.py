"""
Session Manager - Handles user session management
"""

class SessionManager:
    """Manages user sessions"""
    
    _instance = None
    _current_user = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance
    
    def create_session(self, username, user_data):
        """Create a new user session"""
        self._current_user = {
            'username': username,
            'name': user_data['name'],
            'balance': user_data['balance'],
            'account_status': user_data.get('account_status', 'active')
        }
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self._current_user
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self._current_user is not None
    
    def logout(self):
        """End current user session"""
        self._current_user = None
    
    def update_session_balance(self, new_balance):
        """Update balance in current session"""
        if self._current_user:
            self._current_user['balance'] = new_balance
