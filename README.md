# 🏘️ BROKLINK - Rental Property Platform

A modern, full-stack web application for managing rental property listings. Built with Flask backend and vanilla JavaScript frontend.

## ✨ Features

### 🔐 User Authentication
- **Email/Password Registration** - Secure user signup with password hashing
- **Login System** - Session-based authentication
- **Profile Management** - Update user details and delete account

### 🏠 Property Management
- **Post Properties** - Add new rental listings with detailed information
- **Edit Properties** - Update existing property details
- **Delete Properties** - Remove property listings
- **Toggle Availability** - Mark properties as available or unavailable
- **My Properties Dashboard** - View and manage your posted properties

### 🔍 Search & Filter
- **City Filter** - Filter properties by city
- **Area Filter** - Filter properties by specific areas within cities
- **District Filter** - Browse properties by district
- **Dynamic Filtering** - Real-time filter updates based on available properties

### 🎨 User Experience
- **Responsive Design** - Works on desktop and mobile devices
- **Modern UI** - Clean, yellow-themed interface matching BROKLINK branding
- **Property Cards** - Visual property listings with key details
- **Detail Modals** - Comprehensive property information popups
- **Empty States** - Helpful messages when no properties are posted

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.2** - Python web framework
- **SQLAlchemy 2.0.43** - ORM for database operations
- **Flask-SQLAlchemy 3.1.1** - Flask integration for SQLAlchemy
- **PyMySQL 1.1.0** - MySQL database driver
- **Werkzeug 3.1.3** - WSGI utilities and password hashing
- **Flask-CORS 5.0.0** - Cross-Origin Resource Sharing support

### Frontend
- **HTML5** - Semantic markup with Jinja2 templating
- **CSS3** - Custom styling with modern layouts
- **Vanilla JavaScript** - No framework dependencies
- **Google Fonts (Poppins)** - Typography

### Database
- **MySQL/MariaDB** - Relational database
- **Users Table** - User authentication and profiles
- **Properties Table** - Property listings with full details

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL or MariaDB
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/subhashree8125/rental-platform.git
cd rental-platform
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Database
Update the database connection in `backend/config.py`:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/broklink"
```

### 5. Create Database
```sql
CREATE DATABASE broklink;
```

### 6. Initialize Database Tables
The application will create tables automatically on first run, or you can manually create them:

```sql
-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200),
    mobile_number VARCHAR(15) NOT NULL,
    profile_image VARCHAR(200) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Properties table
CREATE TABLE properties (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    property_type VARCHAR(50) NOT NULL,
    house_type VARCHAR(50) NOT NULL,
    rent_price DECIMAL(10,2) NOT NULL,
    car_parking VARCHAR(50),
    pets VARCHAR(50),
    facing VARCHAR(50),
    furnishing VARCHAR(50),
    description TEXT,
    status VARCHAR(20) DEFAULT 'Available',
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### 7. Run the Application
```bash
python app.py
```

The application will be available at:
- **Local**: http://127.0.0.1:5002
- **Network**: http://192.168.x.x:5002

## 📁 Project Structure

```
rental-platform/
├── backend/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── users.py           # User model
│   │   └── properties.py      # Property model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py     # Profile routes
│   │   └── property_routes.py # Property API routes
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css      # Login/Signup styles
│   │   │   ├── explore.css    # Explore page styles
│   │   │   └── profile.css    # Profile page styles
│   │   ├── js/
│   │   │   ├── login.js       # Login functionality
│   │   │   ├── signup.js      # Signup functionality
│   │   │   ├── explore.js     # Browse & filter properties
│   │   │   ├── profile.js     # Profile management
│   │   │   ├── postproperty.js # Property posting
│   │   │   └── authGuard.js   # Auth protection
│   │   ├── img/               # Images and logo
│   │   └── uploads/           # User-uploaded property images
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Landing page
│   │   ├── login.html         # Login page
│   │   ├── signup.html        # Signup page
│   │   ├── explore.html       # Browse properties
│   │   ├── profile.html       # User profile & properties
│   │   └── postproperty.html  # Post new property
│   ├── tests/                 # Unit tests
│   ├── utils/
│   │   ├── auth.py           # Authentication utilities
│   │   └── validators.py     # Validation helpers
│   ├── app.py                # Main application file
│   ├── config.py             # Configuration
│   ├── db.py                 # Database initialization
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Docker configuration (optional)
├── .gitignore
└── README.md
```

## 🔑 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Properties
- `GET /api/properties` - Get all properties (with filters)
- `POST /api/property` - Create new property
- `GET /api/myproperties` - Get user's properties
- `PUT /api/property/<id>` - Update property
- `DELETE /api/property/<id>` - Delete property
- `PATCH /api/property/<id>/status` - Toggle property status

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile
- `DELETE /api/profile` - Delete user account

## 🎨 Features in Detail

### Property Listing Includes:
- Owner name and contact number
- Full address with city, area, and district
- Property type (House, Flat, PG, Hostel)
- BHK type (1HK, 1BHK, 2BHK, 3BHK, 4+ BHK)
- Monthly rent price
- Car parking availability
- Pet policy
- Facing direction
- Furnishing status
- Detailed description
- Availability status toggle

### Filter System:
- **Cascading Filters**: City → Area → District
- **Dynamic Updates**: Filters update based on available properties
- **Real-time Results**: Instant property list updates

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection (can be enhanced with Flask-WTF)
- Secure password storage (never plain text)

## 🧪 Testing

Run tests using pytest:
```bash
cd backend
pytest tests/
```

## 🐳 Docker Support

Optional Docker deployment:
```bash
docker build -t broklink .
docker run -p 5002:5002 broklink
```

## 🤝 Contributing

This is a student project for SIET AIDS. Contributions, issues, and feature requests are welcome!

## 📝 License

This project is for educational purposes as part of the SIET AIDS program.

## 👥 Authors

- **Team BROKLINK** - SIET AIDS Project

## 🙏 Acknowledgments

- SIET (Sri Eshwar Institute of Technology)
- AIDS Department
- Project Guide and Faculty

## 📞 Support

For support or queries, please contact the development team through the repository issues page.

---

**Made with ❤️ by SIET AIDS Students**
