// Define JobPosting Schema
const mongoose = require("mongoose");
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
  
  // Create JobPosting model
  const JobPosting = mongoose.model('JobPosting', jobPostingSchema);
  module.exports = JobPosting;