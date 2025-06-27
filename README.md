# 🏦 Secure Bank - Console Banking Application

<div align="center">
  <img src="https://img.shields.io/badge/Python_App-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python App Badge"/>
  <img src="https://img.shields.io/badge/Console_App-000000?style=for-the-badge&logo=windows-terminal&logoColor=white" alt="Console Badge"/>
  <img src="https://img.shields.io/badge/JSON_Storage-4A90E2?style=for-the-badge&logo=json&logoColor=white" alt="JSON Storage Badge"/>
  
  **A robust and secure banking experience — built with pure Python and file-based storage** 🛡️
  
  [Features](#-features) • [Installation](#-installation) • [Usage](#-usage-guide) • [Security](#️-security-considerations)
</div>

## 🚀 About

Secure Bank is a fully functional, console-based banking system developed in Python. Designed to simulate real-world banking operations, it includes robust authentication, secure session handling, JSON-based file storage, and complete banking features.

🎯 **Perfect for:** Python learners, academic projects, and file-based simulation systems

## ✨ Features

### 🔐 Authentication & Security
- ✅ Secure login & registration
- 🔑 Password hashing (PBKDF2 + salt)
- 🔒 Session-based authentication
- 🛠️ Password change & validation
- ❌ Account closure with confirmation

### 💳 Banking Operations
- 💰 Balance inquiry
- ➕ Deposit funds (max $10,000)
- ➖ Withdraw funds (max $5,000)
- 🔁 Money transfer between accounts
- 📜 View transaction history
- 📄 Generate account statement

## 🧠 File-Based Storage Engine

We use a transparent JSON-based structure for data persistence:

| File Name | Purpose |
|-----------|---------|
| `users.json` | Stores all user accounts and balances |
| `backup/` | Automatic data backups (optional feature) |
| `transactions/` | Per-user transaction logs with timestamps |

## 🛠️ Technical Architecture

```
📁 SecureBank/
├── 🔐 auth/
│   ├── login.py            # Login logic
│   ├── signup.py           # Registration system
│   └── session.py          # Session handler
├── 💰 banking/
│   ├── account.py          # Deposit, Withdraw, Statement
│   ├── transfer.py         # Money transfers
│   └── transactions.py     # Transaction history
├── ⚙️ utils/
│   ├── file_handler.py     # JSON file I/O
│   └── password_utils.py   # PBKDF2 password hashing
├── 🗂️ data/
│   └── users.json          # Main storage file
├── main.py                 # Entry point
└── README.md               # Project documentation
```

### Core Technologies:
- 🐍 Python 3.6+
- 📄 JSON for data persistence
- 🔐 hashlib, getpass, os, datetime (built-in modules)

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- No external libraries required (uses only built-in modules)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/secure-bank.git
cd secure-bank

# Run the application
python main.py
```

## 💡 Usage Guide

### 👤 Creating an Account
1. Launch the app
2. Select "Create New Account"
3. Provide:
   - Unique username (min 3 characters)
   - Full name
   - Strong password (min 6 chars, mix of letters/numbers)
   - Initial deposit (min $10)

### 🏦 Available Operations
After login:
- **Balance** → View your funds
- **Deposit / Withdraw** → Perform transactions
- **Transfer** → Send money to other users
- **History** → View past transactions
- **Statement** → Generate full report
- **Change Password** → Update credentials
- **Close Account** → Delete account permanently

## 🛡️ Security Considerations

| Security Feature | Implementation |
|------------------|----------------|
| Password Protection | PBKDF2 + Random Salt (100k iterations) |
| Session Management | Secure login sessions |
| Input Validation | Regex + sanitization rules |
| Transaction Limits | Deposit: $10,000 / Withdraw: $5,000 |
| File Security | Protected JSON I/O |

## 🔮 Future Enhancements

- 🌐 **Web Interface** – Flask or Django frontend
- 🗃️ **SQL Database** – Replace JSON with SQLite/PostgreSQL
- 📲 **Mobile Support** – Cross-platform with Flutter/Kivy
- 📧 **Email Alerts** – Notifications on transfers/logins
- 📊 **Analytics Dashboard** – Visual reports & graphs

## 🤝 Contributing

Contributions are welcome! 🚀

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to GitHub (`git push origin feature/NewFeature`)
5. Open a pull request

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muhammad Shaheer Malik**

- 🌐 [Portfolio](https://your-portfolio-link.com)
- 💼 [LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 [GitHub](https://github.com/your-username)
- 📧 [Email](mailto:your.email@example.com)
- 📸 [Instagram](https://instagram.com/your-handle)

---

<div align="center">
  <strong>Made with ❤️ using Python & terminal magic</strong>
  <br><br>
  ⭐ If you found this project useful, please consider giving it a star!
</div>
