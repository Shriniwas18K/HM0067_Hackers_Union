# 🎓 WORK CONNECT - Job Portal Platform

**Admin Frontend:** [HM0067 Hackers_Union Admin Frontend](https://hm0067-hackers-union-admin-frontend-9efk.onrender.com)  
**Student Portal:** [HM0067 Hackers_Union Student Portal](https://hm0067-hackers-union.onrender.com)

WORK CONNECT is a dual-interface job portal system built for HackMatrix 3.0, providing seamless job posting and application management for both administrators and students.

---
To login into admin portal use following credentials :
- username: admin
- password: hackunion

## ⭐ Key Features

### 👨‍🎓 For Students
- **Profile Management**
  - Create and edit detailed profiles
  - Upload resumes (PDF format)
  - Add professional links (GitHub, LinkedIn)

- **Job Applications**
  - Browse available job postings
  - Easy one-click applications
  - Track applied jobs
  - View detailed job descriptions

### 👨‍💼 For Administrators
- **Job Management**
  - Create and manage job postings
  - Set job requirements
  - Monitor posting status

---

## 🛠️ Technology Stack

### 🎨 Frontend
- EJS (Template Engine)
- CSS3 with Modern Features
- JavaScript (ES6+)
- Bootstrap 5.3.0
- Font Awesome 6.4.0

### ⚙️ Backend
- Node.js & Express.js
- MongoDB with Mongoose
- Multer (File Uploads)
- bcrypt.js (Password Hashing)
- Session Management

### 🔐 Security
- Express Session
- MongoDB Session Store
- Authentication Middleware

---

## 📁 Project Structure
```
project/
├── admin/
│   ├── admin_backend/
│   │   ├── routes/
│   │   └── app.py
│   ├── admin_frontend/
│   │   ├── public/
│   │   ├── views/
│   │   └── app.js
│
└── student_portal/
    ├── middleware/
    ├── models/
    ├── public/
    │   ├── css/
    │   ├── js/
    │   └── uploads/
    ├── routes/
    ├── views/
    └── app.js
```

---

## 🚀 Installation & Setup
```

### 1️⃣ Install Dependencies

#### Student Portal
```bash
cd student_portal
npm install
```

#### Admin Frontend
```bash
cd admin/admin_frontend
npm install
```

### 2️⃣ Configure Environment Variables
```
PORT=5000
MONGODB_URI=your_mongodb_uri
SESSION_SECRET=your_session_secret
```

### 3️⃣ Run the Applications

#### Start Student Portal
```bash
cd student_portal
npm start
```

#### Start Admin Frontend
```bash
cd admin/admin_frontend
npm start
```

---

## 💫 Features in Detail

### 🔑 User Authentication
- Secure login/register system
- Session management
- Profile completion tracking

### 👤 Profile Management
- Personal information
- Professional links
- Skills section
- Resume upload

### 📄 Job Management
- Detailed job listings
- Application tracking
- Status updates
- Search and filters

### 🎨 UI Features
- Modern, responsive design
- Animated components
- Interactive elements
- Loading states
- Error handling
- Success notifications

---

## 👥 Team Information
- **Team Name:** Hackers_Union
- **Team ID:** HM0067
- **Event:** HackMatrix 3.0
