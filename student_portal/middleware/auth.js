// Authentication middleware
const isAuthenticated = (req, res, next) => {
    if (req.session.user) {
      return next();
    }
    req.flash('error', 'You must be logged in to view this page');
    res.redirect('/login');
  };
  
  // Redirect if already authenticated
  const isNotAuthenticated = (req, res, next) => {
    if (!req.session.user) {
      return next();
    }
    res.redirect('/jobs');
  };
  
  // Check if profile is complete
  const isProfileComplete = (req, res, next) => {
    if (req.session.user && req.session.user.profileCompleted) {
      return next();
    }
    req.flash('error', 'Please complete your profile first');
    res.redirect('/profile/complete');
  };
  
  module.exports = {
    isAuthenticated,
    isNotAuthenticated,
    isProfileComplete
  };