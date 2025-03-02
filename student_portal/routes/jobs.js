const express = require('express');
const router = express.Router();
const User = require('../models/user');
const { isAuthenticated, isProfileComplete } = require('../middleware/auth');
const JobPosting = require('../models/jobPosting');

// Jobs list router
router.get('/', isAuthenticated, isProfileComplete, async (req, res) => {
  try {
    const appliedJobIds = req.session.user.appliedJobs || [];
    // Fetch all jobs from the database
    const allJobs = await JobPosting.find({});
    // Filter out jobs that the user has already applied to
    const jobs = allJobs.filter(job => !appliedJobIds.includes(job._id.toString()));
    
    res.render('jobs/list', { jobs });
  } catch (err) {
    console.error('Error fetching jobs:', err);
    req.flash('error', 'Failed to load jobs');
    res.redirect('/');
  }
});

// Applied jobs router
router.get('/applied', isAuthenticated, isProfileComplete, async (req, res) => {
  try {
    console.log('Fetching applied jobs for user:', req.session.user._id);
    const appliedJobIds = req.session.user.appliedJobs || [];
    console.log('Applied job IDs:', appliedJobIds);
    
    // Fetch only the jobs the user has applied to
    const appliedJobs = await JobPosting.find({ _id: { $in: appliedJobIds } });
    console.log('Found applied jobs:', appliedJobs.length);
    
    res.render('jobs/applied', { appliedJobs });
  } catch (err) {
    console.error('Error fetching applied jobs:', err);
    req.flash('error', 'Failed to load applied jobs');
    res.redirect('/jobs');
  }
});

// Job description router
router.get('/:id', isAuthenticated, isProfileComplete, async (req, res) => {
  try {
    const job = await JobPosting.findById(req.params.id);
    
    if (!job) {
      req.flash('error', 'Job not found');
      return res.redirect('/jobs');
    }
    
    // Check if user has already applied
    const hasApplied = req.session.user.appliedJobs && 
      req.session.user.appliedJobs.includes(req.params.id);
    
    res.render('jobs/description', { job, hasApplied });
  } catch (err) {
    console.error('Error fetching job details:', err);
    req.flash('error', 'Failed to load job details');
    res.redirect('/jobs');
  }
});

// Apply for job router
router.post('/:id/apply', isAuthenticated, isProfileComplete, async (req, res) => {
  try {
    const jobId = req.params.id;
    
    // Check if job exists
    const job = await JobPosting.findById(jobId);
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