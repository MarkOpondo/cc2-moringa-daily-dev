/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Display: headings, card titles, and the logo wordmark — an
        // editorial serif, matching the Figma reference's title style.
        display: ["'Playfair Display'", "serif"],
        // Body: everything readable — paragraphs, labels, buttons.
        sans: ["'Manrope'", "sans-serif"],
        // Mono: stats, timestamps, usernames, code-flavored metadata —
        // reinforces the "developer platform" identity in small doses.
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        // Moringa's actual brand colors, sampled directly from
        // moringaschool.com — not invented values.
        navy: {
          DEFAULT: "#101f3c",  // page background
          raised: "#1a2f52",   // card/surface background
          border: "#2c4570",   // default borders
          borderLight: "#3d5a8a", // hover/emphasis borders
        },
        cream: "#fdf6f0", // primary text on the dark navy background
        brand: {
          400: "#fd8a3d", // lighter orange — soft accents, badges
          500: "#fb6f0f", // primary brand orange
          600: "#e35d00", // darker orange — hover/pressed states, text-on-white
        },
        // Real site's hero gradient stops (white → peach → warm orange) —
        // used on the login screen's branded panel only.
        hero: {
          from: "#fffaf7",
          via: "#fedecf",
          to: "#fdba9c",
        },
        // Role badge colors — kept independent of the brand accent so
        // they still read as distinct labels, not competing with orange.
        role: {
          admin: "#38bdf8",
          writer: "#a78bfa",
          user: "#94a3b8",
        },
      },
    },
  },
  plugins: [],
}