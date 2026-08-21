# Moringa Daily Dev

A full-stack developer portfolio and social platform built with React (Vite), Node.js (Express), and PostgreSQL.

---

## Project Structure

```text
cc2-moringa-daily-dev/
├── client/         # Frontend React application (Vite + Tailwind CSS)
└── server/         # Backend Node.js & Express API (PostgreSQL database)
```

## Getting Started Locally
Follow these steps to set up and run the project on your local machine.

### Prerequisites
Make sure you have the following installed:
* **Node.js** (v18 or higher)
* **PostgreSQL**

---

## Step-by-Step Setup

### Step 1: Database Setup

1. Log into your PostgreSQL shell:
   ```bash
   psql -h localhost -U postgres
   ```

2. Create the database:
   ```sql
   CREATE DATABASE moringa_daily_dev;
   ```

3. Connect to the database and run your tables/migrations (including profile columns):
   ```sql
   ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT;
   ALTER TABLE users ADD COLUMN IF NOT EXISTS skills TEXT;
   ALTER TABLE users ADD COLUMN IF NOT EXISTS github_url TEXT;
   ```

### Step 2: Backend Setup (`/server`)

1. Navigate into the server directory:
   ```bash
   cd server
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file inside the `server/` folder with the following variables:    
   ```env
   PORT=5000
   DB_USER=postgres
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=moringa_daily_dev
   JWT_SECRET=your_super_secret_key   
   ```

4. Start the backend server:
   ```bash
   node server.js
   ```
   *The server will run on http://localhost:5000*

### Step 3: Frontend Setup (`/client`)

1. Open a new terminal tab/window and navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   *The app will run on http://localhost:5173*
