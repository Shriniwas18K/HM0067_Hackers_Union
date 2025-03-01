const express = require('express');
const router = express.Router();
const User = require('../models/user');
const { isAuthenticated, isNotAuthenticated } = require('../middleware/auth');

// Login form
router.get('/login', isNotAuthenticated, (req, res) => {
  res.render('auth/login.ejs  ');
});

// Register form
router.get('/register', isNotAuthenticated, (req, res) => {
  res.render('auth/register');
});

// Register user
router.post('/register', isNotAuthenticated, async (req, res) => {
  try {
    const { name, email, password, phoneNumber } = req.body;
    
    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      req.flash('error', 'Email is already registered');
      return res.redirect('/register');
    }
    
    // Create new user
    const user = new User({
      name,
      email,
      password,
      phoneNumber
    });
    
    await user.save();
    
    req.flash('success', 'Registration successful! Please login');
    res.redirect('/login');
  } catch (err) {
    console.error('Registration error:', err);
    req.flash('error', 'Registration failed: ' + (err.message || 'Unknown error'));
    res.redirect('/register');
  }
});

// Login user
router.post('/login', isNotAuthenticated, async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Find user
    const user = await User.findOne({ email });
    if (!user) {
      req.flash('error', 'Invalid email or password');
      return res.redirect('/login');
    }
    
    // Verify password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      req.flash('error', 'Invalid email or password');
      return res.redirect('/login');
    }
    
    // Store user in session (exclude password)
    const userObj = user.toObject();
    delete userObj.password;
    req.session.user = userObj;
    
    // Check if profile is complete
    if (!user.profileCompleted) {
      req.flash('info', 'Please complete your profile');
      return res.redirect('/profile/complete');
    }
    
    req.flash('success', 'Login successful!');
    res.redirect('/jobs');
  } catch (err) {
    console.error('Login error:', err);
    req.flash('error', 'Login failed: ' + (err.message || 'Unknown error'));
    res.redirect('/login');
  }
});

// Logout
router.get('/logout', isAuthenticated, (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error('Logout error:', err);
    }
    res.redirect('/login');
  });
});

module.exports = router;