const express = require('express');
const router = express.Router();
const User = require('../models/user');
const { isAuthenticated } = require('../middleware/auth');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const dir = path.join(__dirname, '../public/uploads/resumes');
    // Create directory if it doesn't exist
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    cb(null, dir);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    // Accept only pdf files
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed'));
    }
  }
});

// View profile
router.get('/', isAuthenticated, (req, res) => {
  res.render('profile/view');
});

// Complete profile form
router.get('/complete', isAuthenticated, (req, res) => {
  res.render('profile/complete');
});

// Update profile
router.post('/complete', isAuthenticated, upload.single('resume'), async (req, res) => {
  try {
    const { college, dob, skills, github, linkedin } = req.body;
    
    // Get resume file path if uploaded
    const resumePath = req.file ? `/uploads/resumes/${req.file.filename}` : req.session.user.resume;
    
    // Update user
    const updatedUser = await User.findByIdAndUpdate(
      req.session.user._id,
      {
        college,
        dob,
        skills,
        github,
        linkedin,
        resume: resumePath,
        profileCompleted: true
      },
      { new: true }
    );
    
    // Update session
    const userObj = updatedUser.toObject();
    delete userObj.password;
    req.session.user = userObj;
    
    req.flash('success', 'Profile updated successfully');
    res.redirect('/jobs');
  } catch (err) {
    console.error('Profile update error:', err);
    req.flash('error', 'Profile update failed: ' + (err.message || 'Unknown error'));
    res.redirect('/profile/complete');
  }
});

module.exports = router;