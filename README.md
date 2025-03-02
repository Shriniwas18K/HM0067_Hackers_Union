# 🎓 WORK CONNECT Portal

A comprehensive job portal system with separate admin and student interfaces, built for HackMatrix 3.0. The platform enables efficient job posting, application management, and streamlined hiring processes.

---

## 📌 Table of Contents
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Frontend Guide](#-frontend-guide)
- [Testing](#-testing)
- [Team Information](#-team-information)
---

## 🏗️ System Architecture
The application follows a dual-portal architecture:

### 🔒 Admin Portal (Flask Backend)
- RESTful API service for administrators
- Secure job posting and application management
- User analytics and control

### 👥 Student Portal (Node.js Frontend)
- Interactive user interface for students
- Real-time job search and applications
- Profile management system

---

## ✨ Features

### Admin Features
- 🔐 Secure admin authentication
- 📝 Job posting management
- 👥 User management dashboard
- 📊 Application tracking system
- 📈 Analytics and reporting

### Student Features
- 🔑 User authentication system
- 👤 Profile creation and management
- 📄 Resume upload functionality
- 🔍 Job search and filtering
- ✅ One-click applications
- 📱 Responsive design

---

## 🛠️ Tech Stack

### **Admin Backend**
- Flask
- PyMongo
- Flask-JWT-Extended
- Python-dotenv
- Pytest

### **Student Frontend**
- Node.js
- Express.js
- EJS
- Mongoose
- Bcrypt.js
- Multer
- Express-Session

---

## 📂 Project Structure
```
project_root/
├── admin/
│   └── admin_backend/
│       ├── app.py
│       ├── db.py
│       └── routes/
│           ├── admin.py
│           ├── auth.py
│           ├── jobs.py
│           └── users.py
├── student_portal/
│   ├── app.js
│   ├── models/
│   ├── routes/
│   ├── views/
│   └── public/
└── tests/
```

---

## 🚀 Installation

### Admin Backend Setup
```bash
cd admin/admin_backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Student Portal Setup
```bash
cd student_portal
npm install
npm start
```

### Environment Configuration

#### **Admin Backend (.env)**
```
FLASK_APP=app.py
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017/jobportal
JWT_SECRET=your_secret_key
```

#### **Student Portal (.env)**
```
PORT=3000
MONGODB_URI=mongodb://localhost:27017/jobportal
SESSION_SECRET=your_session_secret
```

---

## 📚 API Documentation

### **Admin Routes**
#### Authentication
- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout

#### Jobs Management
- `GET /api/jobs` - Retrieve job listings
- `POST /api/jobs` - Create a new job
- `PUT /api/jobs/:id` - Update job details
- `DELETE /api/jobs/:id` - Delete a job

#### User Management
- `GET /api/users` - List all users
- `PUT /api/users/:id` - Update user details
- `DELETE /api/users/:id` - Remove a user

### **Student Routes**
#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `GET /auth/logout` - Logout user

#### Profile Management
- `GET /profile` - View user profile
- `POST /profile/update` - Update profile details
- `POST /profile/resume` - Upload resume

#### Jobs
- `GET /jobs` - View job listings
- `GET /jobs/:id` - View job details
- `POST /jobs/:id/apply` - Apply for a job

---

## 🎨 Frontend Views
```
views/
├── auth/
│   ├── login.ejs
│   └── register.ejs
├── jobs/
│   ├── list.ejs
│   └── details.ejs
├── profile/
│   └── dashboard.ejs
└── partials/
    ├── header.ejs
    └── footer.ejs
```

---

## 🧪 Testing

### Admin Backend Tests
```bash
cd admin/admin_backend
python -m pytest tests/
```

### Student Portal Tests
```bash
cd student_portal
npm test
```
---

## 👥 Team Information
- **Team Name**: Hackers_Union
- **Team ID**: HM0067
- **Hackathon**: HackMatrix 3.0
---


