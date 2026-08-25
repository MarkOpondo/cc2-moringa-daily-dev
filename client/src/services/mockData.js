// This file simulates the Flask + PostgreSQL backend described in the ERD,
// entirely in memory, so the frontend can be built and demoed before the
// real backend exists.

let nextId = 1000;
export const genId = () => String(nextId++);

const now = Date.now();
const daysAgo = (n) => new Date(now - n * 86400000).toISOString();

export const users = [
  { id: "u1", username: "amina_dev", email: "amina@moringaschool.com", role: "admin", isActive: true, createdAt: daysAgo(120) },
  { id: "u2", username: "brian_writes", email: "brian@moringaschool.com", role: "tech_writer", isActive: true, createdAt: daysAgo(100) },
  { id: "u3", username: "chebet_k", email: "chebet@moringaschool.com", role: "tech_writer", isActive: true, createdAt: daysAgo(90) },
  { id: "u4", username: "davidm", email: "david@moringaschool.com", role: "user", isActive: true, createdAt: daysAgo(60) },
  { id: "u5", username: "faith_codes", email: "faith@moringaschool.com", role: "user", isActive: true, createdAt: daysAgo(40) },
  { id: "u6", username: "george_o", email: "george@moringaschool.com", role: "user", isActive: false, createdAt: daysAgo(200) },
];

export const profiles = {
  u1: { bio: "Program lead. Keeping the community sharp.", profileImage: "", interests: ["DevOps", "Career"] },
  u2: { bio: "Backend engineer turned technical writer. Ex-Andela.", profileImage: "", interests: ["Backend", "DevOps"] },
  u3: { bio: "Frontend alum, now mentoring. React & design systems.", profileImage: "", interests: ["Frontend", "Design"] },
  u4: { bio: "Fullstack student, into cloud infra.", profileImage: "", interests: ["Fullstack", "DevOps"] },
  u5: { bio: "Data track. Loves a good dashboard.", profileImage: "", interests: ["Data Science"] },
  u6: { bio: "", profileImage: "", interests: [] },
};

export const categories = [
  { id: "c1", name: "Frontend", description: "React, CSS, accessibility, browser APIs.", createdBy: "u1" },
  { id: "c2", name: "Backend", description: "APIs, databases, server architecture.", createdBy: "u1" },
  { id: "c3", name: "DevOps", description: "CI/CD, containers, cloud infrastructure.", createdBy: "u1" },
  { id: "c4", name: "Fullstack", description: "End-to-end app building.", createdBy: "u1" },
  { id: "c5", name: "Career", description: "Interviews, portfolios, job hunting in tech.", createdBy: "u1" },
  { id: "c6", name: "Data Science", description: "ML, analytics, and data engineering.", createdBy: "u1" },
];

export const content = [
  {
    id: "n1",
    title: "What I wish I knew before my first backend interview",
    body: "Landing a backend role isn't just about knowing syntax — it's about being able to talk through trade-offs. In my first interview I could write a working API in Flask, but I froze when asked why I chose a relational database over a document store. Here's the framework I use now: think in terms of read/write patterns first, consistency requirements second, and team familiarity third. If your data has clear relationships and you need strong consistency, Postgres wins. If you're storing loosely structured logs at huge scale, a document store starts to make more sense.\n\nThe other thing that caught me off guard: interviewers care more about how you debug than whether you get it right the first time. Narrate your thinking. Say what you'd check first, second, third. That's the signal they're actually looking for.",
    type: "article",
    mediaUrl: "",
    authorId: "u2",
    categoryId: "c2",
    status: "approved",
    createdAt: daysAgo(2),
  },
  {
    id: "n2",
    title: "Live coding: building a design system component from scratch",
    body: "A recorded session where we build an accessible dropdown component from zero — covering keyboard navigation, ARIA roles, and how to structure the CSS so it survives contact with a real design system.",
    type: "video",
    mediaUrl: "https://example.com/videos/design-system-dropdown",
    authorId: "u3",
    categoryId: "c1",
    status: "approved",
    createdAt: daysAgo(4),
  },
  {
    id: "n3",
    title: "Docker for people who just want their app to run the same everywhere",
    body: "A practical, no-jargon walkthrough of containerizing a Flask + React project — what actually goes in the Dockerfile, what belongs in docker-compose, and the three mistakes almost everyone makes on their first attempt (hint: one of them is forgetting .dockerignore exists).",
    type: "article",
    mediaUrl: "",
    authorId: "u2",
    categoryId: "c3",
    status: "approved",
    createdAt: daysAgo(6),
  },
  {
    id: "n4",
    title: "Alumni spotlight: from bootcamp to Staff Engineer in 4 years",
    body: "An interview with a Moringa alum now working as a Staff Engineer at a fintech scale-up, on what actually mattered for career growth — and what didn't.",
    type: "audio",
    mediaUrl: "https://example.com/audio/alumni-spotlight-1",
    authorId: "u1",
    categoryId: "c5",
    status: "approved",
    createdAt: daysAgo(9),
  },
  {
    id: "n5",
    title: "Reading a query plan without panicking",
    body: "EXPLAIN ANALYZE looks intimidating until you know which three numbers actually matter. This walks through a slow query end to end and shows exactly where the time was going.",
    type: "article",
    mediaUrl: "",
    authorId: "u2",
    categoryId: "c2",
    status: "pending",
    createdAt: daysAgo(1),
  },
  {
    id: "n6",
    title: "Why your first 'full stack app' should be smaller than you think",
    body: "A case for shipping something embarrassingly simple before reaching for the feature list — with a real example of a project scoped down from 14 features to 3.",
    type: "article",
    mediaUrl: "",
    authorId: "u4",
    categoryId: "c4",
    status: "approved",
    createdAt: daysAgo(12),
  },
  {
    id: "n7",
    title: "A gentle intro to pandas for people who think spreadsheets are fine, actually",
    body: "You don't need to love data science to benefit from knowing pandas. This starts from 'what a DataFrame even is' and ends with a real cleanup of a messy CSV.",
    type: "article",
    mediaUrl: "",
    authorId: "u5",
    categoryId: "c6",
    status: "approved",
    createdAt: daysAgo(15),
  },
];

export const comments = [
  { id: "cm1", contentId: "n1", userId: "u4", parentCommentId: null, body: "This reframing of the DB question is genuinely useful, thank you.", createdAt: daysAgo(1) },
  { id: "cm2", contentId: "n1", userId: "u2", parentCommentId: "cm1", body: "Glad it helped! The 'narrate your debugging' part is the one people forget under pressure.", createdAt: daysAgo(1) },
  { id: "cm3", contentId: "n1", userId: "u5", parentCommentId: null, body: "Following this framework for my interview next week.", createdAt: daysAgo(0) },
  { id: "cm4", contentId: "n3", userId: "u4", parentCommentId: null, body: "The .dockerignore mistake got me too 😅", createdAt: daysAgo(5) },
];

export const reactions = [
  { id: "r1", userId: "u4", contentId: "n1", type: "like" },
  { id: "r2", userId: "u5", contentId: "n1", type: "like" },
  { id: "r3", userId: "u6", contentId: "n1", type: "like" },
  { id: "r4", userId: "u4", contentId: "n3", type: "like" },
];

export const subscriptions = [
  { id: "s1", userId: "u4", categoryId: "c3" },
  { id: "s2", userId: "u4", categoryId: "c4" },
  { id: "s3", userId: "u5", categoryId: "c6" },
];

export const wishlist = [
  { id: "w1", userId: "u4", contentId: "n2" },
  { id: "w2", userId: "u4", contentId: "n7" },
];

export const notifications = [
  { id: "nt1", userId: "u4", contentId: "n3", message: "New in DevOps: \"Docker for people who just want their app to run the same everywhere\"", isRead: false, createdAt: daysAgo(6) },
  { id: "nt2", userId: "u4", contentId: "n6", message: "New in Fullstack: \"Why your first 'full stack app' should be smaller than you think\"", isRead: false, createdAt: daysAgo(12) },
  { id: "nt3", userId: "u4", contentId: "n1", message: "brian_writes replied to a thread you're in", isRead: true, createdAt: daysAgo(1) },
];

export const reports = [
  { id: "rp1", contentId: "n5", reportedBy: "u6", reason: "Seems like a duplicate of an earlier post.", status: "open", createdAt: daysAgo(1) },
];

// Simulates real network latency so loading states are actually visible
// and meaningful during development, instead of resolving instantly.
export const delay = (ms = 400) => new Promise((res) => setTimeout(res, ms));
