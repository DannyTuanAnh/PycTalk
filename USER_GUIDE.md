# PycTalk - Modern Login System

## Quick Start Guide

### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# For Ubuntu/Debian (if needed for PyQt6)
sudo apt-get install libegl1 libgl1-mesa-dri
```

### 2. Database Setup
- **With MySQL**: Follow `database/schema.md` to set up MySQL
- **For Testing**: The system automatically uses a mock database when MySQL is not available

### 3. Running the Application

#### Start Server:
```bash
cd server
python3 main_server.py
```

#### Start Client (Login UI):
```bash
cd client/Login
python3 login_signIn.py
```

### 4. Test Credentials

| Username | Password | Email |
|----------|----------|-------|
| admin | admin123 | admin@pyctalk.com |
| test | test123 | test@pyctalk.com |

## Features Implemented ✅

### 🎨 Modern Gradient UI
- Beautiful gradient background (blue to purple)
- Glassmorphism card design with shadows
- Responsive input fields with focus effects
- Modern button styling with hover animations
- Professional typography and spacing

### 🔐 Security Features
- SHA256 password hashing
- Login attempt logging
- Input validation
- SQL injection prevention
- Secure client-server communication

### 🚀 Client-Server Architecture
- Multi-threaded server handling multiple clients
- Asynchronous login processing
- JSON-based communication protocol
- Professional error handling
- Connection management

### 💾 Database Integration
- MySQL database support
- Mock database for testing
- User management system
- Login logs tracking
- Auto-table creation

### 🎯 User Experience
- Centered, responsive design
- Loading states during login
- Success/error message dialogs
- Remember me checkbox
- Professional Vietnamese interface

## Architecture

```
PycTalk/
├── client/                 # Client-side application
│   ├── UI/                 # Modern PyQt6 interface
│   │   └── loginUI.py      # Gradient login UI
│   ├── Login/              # Login controller
│   │   └── login_signIn.py # Main login logic
│   └── Request/            # Client-server communication
│       └── handle_request_client.py
├── server/                 # Server-side application
│   ├── main_server.py      # Multi-threaded server
│   └── Login_server/
│       └── LoginHandle.py  # Authentication logic
└── database/               # Database layer
    ├── db.py              # Connection management
    ├── mock_db.py         # Testing database
    └── schema.md          # Database schema
```

## Testing

The system includes comprehensive testing:
- Mock database for environments without MySQL
- Automated login flow testing
- Error handling verification
- Multi-user authentication testing

## Production Deployment

For production use:
1. Set up MySQL database following `database/schema.md`
2. Update database credentials in `database/db.py`
3. Configure server host/port settings
4. Set up proper SSL/TLS for secure communication
5. Implement proper logging and monitoring

Ready for production deployment! 🚀