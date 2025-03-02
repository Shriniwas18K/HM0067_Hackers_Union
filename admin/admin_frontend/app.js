const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const session = require('express-session');
const cors = require('cors');
const app = express();
app.use(cors());
const PORT = process.env.PORT || 3000;

// MongoDB Connection
mongoose.connect('mongodb+srv://Pankaj:More0%2316@hackmatrixdb.sbu0c.mongodb.net/?retryWrites=true&w=majority&appName=hackmatrixdb')
  .then(() => console.log('MongoDB connected'))
  .catch(err => {
    console.error('MongoDB connection error:', err);
    process.exit(1);
  });

// Job Posting Schema & Model
const jobPostingSchema = new mongoose.Schema({
  JobRole: {
    type: String,
    required: true
  },
  OrganizationName: {
    type: String,
    required: true
  },
  Location: {
    type: String,
    required: true
  },
  Salary: {
    type: String,
    required: true
  },
  PostedOn: {
    type: String,
    required: true
  },
  JobDescription: {
    type: String,
    required: true
  },
  Requirements: {
    type: [String],
    required: true
  }
}, { collection: 'job_postings' });

const JobPosting = mongoose.model('JobPosting', jobPostingSchema);

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'hackunion_secret_key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 3600000 } // 1 hour
}));

// Authentication Middleware
const isAuthenticated = (req, res, next) => {
  if (req.session && req.session.isAuthenticated) {
    return next();
  }
  return res.redirect('/');
};

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
// Login page
app.get('/', (req, res) => {
  res.render('login', { error: null });
});

// Login authentication
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  // Check credentials
  if (username === 'admin' && password === 'hackunion') {
    req.session.isAuthenticated = true;
    return res.redirect('/jobs/create');
  } else {
    return res.render('login', { error: 'Invalid username or password' });
  }
});

// Logout route
app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

// Create job form route (protected)
app.get('/jobs/create', isAuthenticated, (req, res) => {
  res.render('jobForm', { success: null, error: null });
});

// Submit job posting (protected)
app.post('/jobs/create', isAuthenticated, async (req, res) => {
  try {
    const { jobRole, organizationName, location, salary, jobDescription, requirements } = req.body;
    
    // Split requirements by new line
    const requirementsArray = requirements.split('\n').filter(req => req.trim() !== '');
    
    const newJobPosting = new JobPosting({
      JobRole: jobRole,
      OrganizationName: organizationName,
      Location: location,
      Salary: salary,
      PostedOn: new Date().toISOString().split('T')[0], // Current date in YYYY-MM-DD format
      JobDescription: jobDescription,
      Requirements: requirementsArray
    });
    
    await newJobPosting.save();
    res.render('jobForm', { success: 'Job posting created successfully!', error: null });
  } catch (err) {
    console.error(err);
    res.render('jobForm', { success: null, error: 'Error creating job posting' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});