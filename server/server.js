require('dotenv').config();

const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

const STRICT_EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|co)$/i;

const FORBIDDEN_USERNAMES = [
  'admin', 'administrator', 'adm', 'root', 'user', 'user1', 'test', 'tester', 'guest',
  'operator', 'sysadmin', 'system', 'support', 'helpdesk', 'manager', 'supervisor',
  'john', 'jane', 'smith', 'doe', 'alex', 'chris'
];

const FORBIDDEN_EMAIL_PREFIXES = [
  'billing', 'invoice', 'accounting', 'hr', 'humanresources', 'payroll', 'ceo',
  'executive', 'president', 'noreply', 'no-reply', 'security', 'it', 'help', 'service',
  'documents', 'esignature-portal', 'sharepoint-share', 'onedrive-view', 'dropbox-secure',
  'paypal-disputes', 'chase-security-update'
];

// --- AUTHENTICATION MIDDLEWARE ---
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) return res.status(401).json({ message: 'Access denied. No token provided.' });

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ message: 'Invalid or expired token.' });
    req.user = user;
    next();
  });
};

// --- AUTH ROUTES ---
app.post('/api/auth/signup', async (req, res) => {
  const { username, email, password } = req.body;

  if (!username || !email || !password) {
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  if (!STRICT_EMAIL_REGEX.test(email)) {
    return res.status(400).json({ message: 'Invalid Email Format: Email must end strictly with .com or .co' });
  }

  const lowerUser = username.toLowerCase().trim();
  if (FORBIDDEN_USERNAMES.includes(lowerUser)) {
    return res.status(400).json({ message: `Security Warning: "${username}" is a reserved administrative username.` });
  }

  const emailPrefix = email.split('@')[0].toLowerCase();
  if (FORBIDDEN_EMAIL_PREFIXES.includes(emailPrefix)) {
    return res.status(400).json({ message: `Security Warning: Role-based email prefix "${emailPrefix}@" is blocked.` });
  }

  try {
    const existingCheck = await db.query(
      'SELECT * FROM users WHERE LOWER(email) = LOWER($1) OR LOWER(username) = LOWER($2)',
      [email, username]
    );

    if (existingCheck.rows.length > 0) {
      const match = existingCheck.rows[0];
      if (match.email.toLowerCase() === email.toLowerCase()) {
        return res.status(400).json({ message: 'Email Already Exists: Account already exists with this email address.' });
      }
      return res.status(400).json({ message: 'Username Taken: Please choose a different username.' });
    }

    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);

    const newUser = await db.query(
      'INSERT INTO users (username, email, password_hash) VALUES ($1, $2, $3) RETURNING id, username, email',
      [username, email, passwordHash]
    );

    const token = jwt.sign(
      { id: newUser.rows[0].id, username: newUser.rows[0].username },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.status(201).json({
      message: 'User registered successfully',
      user: newUser.rows[0],
      token
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Database connection or server error.' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: 'Missing required fields.' });
  }

  if (!STRICT_EMAIL_REGEX.test(email)) {
    return res.status(400).json({ message: 'Invalid Email Format: Email must end strictly with .com or .co' });
  }

  try {
    const userResult = await db.query('SELECT * FROM users WHERE LOWER(email) = LOWER($1)', [email]);

    if (userResult.rows.length === 0) {
      return res.status(400).json({ message: 'Invalid Email or Password.' });
    }

    const user = userResult.rows[0];
    const isMatch = await bcrypt.compare(password, user.password_hash);

    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid Email or Password.' });
    }

    const token = jwt.sign(
      { id: user.id, username: user.username },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      message: 'Login successful',
      user: { id: user.id, username: user.username, email: user.email },
      token
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Database connection or server error.' });
  }
});

// --- PROFILE ROUTES ---
app.get('/api/profile', authenticateToken, async (req, res) => {
  try {
    const userResult = await db.query(
      'SELECT id, username, email, bio, skills, github_url FROM users WHERE id = $1',
      [req.user.id]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({ message: 'User not found.' });
    }

    res.json(userResult.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error fetching profile.' });
  }
});

app.put('/api/profile', authenticateToken, async (req, res) => {
  const { bio, skills, github_url } = req.body;
  try {
    const updatedUser = await db.query(
      `UPDATE users 
       SET bio = COALESCE($1, bio), 
           skills = COALESCE($2, skills), 
           github_url = COALESCE($3, github_url) 
       WHERE id = $4 
       RETURNING id, username, email, bio, skills, github_url`,
      [bio, skills, github_url, req.user.id]
    );

    res.json(updatedUser.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error updating profile.' });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));