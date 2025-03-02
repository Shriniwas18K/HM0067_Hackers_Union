  require("dotenv").config();
  const express = require("express");
  const session = require("express-session");
  const path = require("path");
  const mongoose = require("mongoose");
  const MongoStore = require('connect-mongo');
  const flash = require('connect-flash');
  const authRoutes = require('./routes/auth');
  const jobsRoutes = require('./routes/jobs');
  const profileRoutes = require('./routes/profile');

const cors = require('cors'); // Import cors package
  const app = express();
  app.use(cors());

  // Middleware
  app.set("view engine", "ejs");
  app.use(express.urlencoded({ extended: true }));
  app.use(express.json());
  app.use(express.static(path.join(__dirname, "public")));

  // Session configuration with MongoDB store
  app.use(session({
    secret: process.env.SESSION_SECRET || "jobportal",
    resave: false,
    saveUninitialized: false,
    store: MongoStore.create({
      mongoUrl: process.env.MONGODB_URI || "mongodb+srv://Pankaj:More0%2316@hackmatrixdb.sbu0c.mongodb.net/?retryWrites=true&w=majority&appName=hackmatrixdb",
      ttl: 14 * 24 * 60 * 60 // = 14 days
    }),
    cookie: {
      maxAge: 14 * 24 * 60 * 60 * 1000 // 14 days in milliseconds
    }
  }));

  // Flash messages
  app.use(flash());

  // Global variables
  app.use((req, res, next) => {
    res.locals.currentUser = req.session.user || null;
    res.locals.success = req.flash('success');
    res.locals.error = req.flash('error');
    next();
  });

  // MongoDB Connection using mongoose
  const mongoURI = process.env.MONGODB_URI || "mongodb+srv://Pankaj:More0%12316@hackmatrixdb.sbu0c.mongodb.net/?retryWrites=true&w=majority&appName=hackmatrixdb";

  console.log("Connecting to MongoDB...");
  mongoose.connect(mongoURI)
    .then(() => {
      console.log("✅ Successfully connected to MongoDB Atlas");
    })
    .catch(err => {
      console.error(" MongoDB Connection Error:", err);
      process.exit(1);
    });

  // Routes
  app.use('/', authRoutes);
  app.use('/jobs', jobsRoutes);
  app.use('/profile', profileRoutes);

  // Home route
  app.get("/", (req, res) => {
    res.render("index");
  });

  // 404 handler
  app.use((req, res) => {
    res.status(404).render('404');
  });

  // Start the server
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => console.log(`Job portal running on port ${PORT}`));




