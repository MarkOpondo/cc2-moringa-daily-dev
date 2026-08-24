/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Display: headings, hero text — technical, geometric, a little sharp.
        display: ["'Space Grotesk'", "sans-serif"],
        // Body: everything readable — paragraphs, labels, buttons.
        sans: ["'Manrope'", "sans-serif"],
        // Mono: stats, timestamps, usernames, code-flavored metadata —
        // reinforces the "developer platform" identity in small doses.
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        // Role badge colors — one accent per role, used only for small
        // badges/avatBadges, never as a background, so they read as
        // labels rather than competing with the amber brand accent.
        role: {
          admin: "#38bdf8",   // sky-400
          writer: "#a78bfa",  // violet-400
          user: "#94a3b8",    // slate-400
        },
      },
    },
  },
  plugins: [],
}