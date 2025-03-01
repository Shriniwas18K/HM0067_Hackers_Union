const express = require('express');
const router = express.Router();
const User = require('../models/user');
const { isAuthenticated, isProfileComplete } = require('../middleware/auth');

// Mock job data (replace with actual database model in production)
const jobs = [
  {
    id: '1',
    title: 'Frontend Developer',
    company: 'TechCorp',
    location: 'Pune',
    description: 'We are looking for a skilled frontend developer proficient in React.js and modern CSS frameworks.',
    requirements: 'React.js, JavaScript, CSS, Responsive Design',
    salary: '₹6-10 LPA',
    posted: new Date('2025-02-15')
  },
  {
    id: '2',
    title: 'Backend Engineer',
    company: 'DataSoft',
    location: 'Bengaluru',
    description: 'Join our team to build scalable backend systems using Node.js and MongoDB.',
    requirements: 'Node.js, Express, MongoDB, API Design',
    salary: '₹8-12 LPA',
    posted: new Date('2025-02-20')
  },
  {
    id: '3',
    title: 'Full Stack Developer',
    company: 'WebSolutions',
    location: 'Mumbai',
    description: 'Looking for developers who can work on both frontend and backend technologies to build complete web applications.',
    requirements: 'React, Node.js, MongoDB, AWS',
    salary: '₹10-15 LPA',
    posted: new Date('2025-02-25')
  },
  {
    id: '4',
    title: 'Full Stack Developer',
    company: 'WebSolutions',
    location: 'Mumbai',
    description: 'Looking for developers who can work on both frontend and backend technologies to build complete web applications.',
    requirements: 'React, Node.js, MongoDB, AWS',
    salary: '₹10-15 LPA',
    posted: new Date('2025-02-25')
  },  
  {
    id: '5',
    title: 'Full Stack Developer',
    company: 'WebSolutions',
    location: 'Mumbai',
    description: 'Looking for developers who can work on both frontend and backend technologies to build complete web applications.',
    requirements: 'React, Node.js, MongoDB, AWS',
    salary: '₹10-15 LPA',
    posted: new Date('2025-02-25')
  }
];

// Jobs list router
router.get('/', isAuthenticated, isProfileComplete, (req, res) => {
  const appliedJobIds = req.session.user.appliedJobs || [];
  const Jobs = jobs.filter(job => !appliedJobIds.includes(job.id));
  res.render('jobs/list', { Jobs });
});

// Applied jobs router - MOVED UP before the :id route to prevent route conflicts
router.get('/applied', isAuthenticated, isProfileComplete, (req, res) => {
  const appliedJobIds = req.session.user.appliedJobs || [];
  const appliedJobs = jobs.filter(job => appliedJobIds.includes(job.id));
  
  res.render('jobs/applied', { appliedJobs });
});

// Job description router
router.get('/:id', isAuthenticated, isProfileComplete, (req, res) => {
  const job = jobs.find(j => j.id === req.params.id);
  
  if (!job) {
    req.flash('error', 'Job not found');
    return res.redirect('/jobs');
  }
  
  // Check if user has already applied
  const hasApplied = req.session.user.appliedJobs &&
    req.session.user.appliedJobs.includes(req.params.id);
  
  res.render('jobs/description', { job, hasApplied });
});

// Apply for job router
router.post('/:id/apply', isAuthenticated, isProfileComplete, async (req, res) => {
  try {
    const jobId = req.params.id;
    
    // Check if job exists
    const job = jobs.find(j => j.id === jobId);
    if (!job) {
      req.flash('error', 'Job not found');
      return res.redirect('/jobs');
    }
    
    // Update user's applied jobs
    const user = await User.findById(req.session.user._id);
    
    if (!user.appliedJobs.includes(jobId)) {
      user.appliedJobs.push(jobId);
      await user.save();
      
      // Update session 
      req.session.user.appliedJobs = user.appliedJobs;
      req.flash('success', 'Successfully applied for the job');
    } else {
      req.flash('info', 'You have already applied for this job');
    }
    
    res.redirect('/jobs/applied');
  } catch (err) {
    console.error('Job application error:', err);
    req.flash('error', 'Failed to apply for job: ' + (err.message || 'Unknown error'));
    res.redirect('/jobs/applied');
  }
});

module.exports = router;