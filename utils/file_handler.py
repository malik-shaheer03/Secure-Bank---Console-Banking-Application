"""
File Handler - Manages file operations for data storage
"""

import json
import os
from datetime import datetime

class FileHandler:
    """Handles file operations for user data storage"""
    
    DATA_DIR = "data"
    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    
    @classmethod
    def ensure_data_directory(cls):
        """Ensure data directory exists"""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)
    
    @classmethod
    def load_users(cls):
        """Load users data from JSON file"""
        try:
            cls.ensure_data_directory()
            if os.path.exists(cls.USERS_FILE):
                # Check if file is empty or corrupted
                if os.path.getsize(cls.USERS_FILE) == 0:
                    # File is empty, initialize with empty dict
                    return {}
                
                with open(cls.USERS_FILE, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        return {}
                    return json.loads(content)
            else:
                # File doesn't exist, create it with empty dict
                cls.save_users({})
                return {}
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("🔧 Attempting to fix corrupted data file...")
            # Backup corrupted file and create new one
            try:
                if os.path.exists(cls.USERS_FILE):
                    backup_name = f"{cls.USERS_FILE}.corrupted.backup"
                    os.rename(cls.USERS_FILE, backup_name)
                    print(f"📁 Corrupted file backed up as: {backup_name}")
                cls.save_users({})
                return {}
            except Exception as backup_error:
                print(f"❌ Error fixing data file: {backup_error}")
                return {}
        except Exception as e:
            print(f"❌ Error loading user data: {e}")
            return {}
    
    @classmethod
    def save_users(cls, users_data):
        """Save users data to JSON file"""
        try:
            cls.ensure_data_directory()
            
            # Validate that the data is JSON serializable
            json.dumps(users_data)  # Test serialization
            
            # Write to temporary file first, then rename (atomic operation)
            temp_file = cls.USERS_FILE + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump(users_data, f, indent=2)
            
            # Replace the original file
            if os.path.exists(cls.USERS_FILE):
                os.replace(temp_file, cls.USERS_FILE)
            else:
                os.rename(temp_file, cls.USERS_FILE)
            
            return True
        except TypeError as e:
            print(f"❌ Data serialization error: {e}")
            print("❌ Cannot save data - contains non-serializable objects")
            return False
        except Exception as e:
            print(f"❌ Error saving user data: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            return False
    
    @classmethod
    def get_current_timestamp(cls):
        """Get current timestamp as string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @classmethod
    def backup_data(cls):
        """Create backup of user data"""
        try:
            if os.path.exists(cls.USERS_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(cls.DATA_DIR, f"users_backup_{timestamp}.json")
                
                with open(cls.USERS_FILE, 'r') as source:
                    with open(backup_file, 'w') as backup:
                        backup.write(source.read())
                
                return backup_file
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None
