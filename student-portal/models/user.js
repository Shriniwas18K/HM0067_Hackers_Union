const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");

const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: { 
    type: String, 
    required: true 
  },
  name: { 
    type: String, 
    required: true, 
    trim: true 
  },
  phoneNumber: {
    type: String,
    required: true,
    validate: {
      validator: function(v) {
        return /^[0-9]{10}$/.test(v); // Ensures exactly 10-digit phone number
      },
      message: props => `${props.value} is not a valid phone number!`
    }
  },
  college: { 
    type: String, 
    default: ""
  },
  dob: { 
    type: Date 
  },
  leetcode: { 
    type: String, 
    trim: true 
  },
  github: { 
    type: String, 
    trim: true 
  },
  linkedin: { 
    type: String, 
    trim: true 
  },
  resume: { 
    type: String 
  }, // Store resume file path
  profileCompleted: {
    type: Boolean,
    default: false
  },
  appliedJobs: [{
    type: String,
    ref: 'Job'
  }]
}, { timestamps: true });

// Method to compare password
UserSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Hash password before saving user
UserSchema.pre("save", async function(next) {
  if (!this.isModified("password")) return next();
  
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

module.exports = mongoose.model("User", UserSchema);