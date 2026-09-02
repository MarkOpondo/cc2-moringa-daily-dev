/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Display: headings, card titles, the logo wordmark — bold,
        // rounded sans, matching moringaschool.com's marketing site
        // (not an editorial serif — the real site never uses one).
        display: ["'Manrope'", "sans-serif"],
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
          DEFAULT: "#101f3c",  // primary text, active nav/pill borders
          raised: "#1a2f52",   // dark surfaces (announcement bar, drawer)
          border: "#2c4570",   // borders on dark surfaces
          borderLight: "#3d5a8a", // hover/emphasis borders on dark surfaces
        },
        // Light-theme surfaces — the site is white/paper first now,
        // navy is a text + accent color, not the page background.
        paper: "#ffffff",       // page background
        surface: "#fff8f4",     // warm off-white card/section background
        line: "#e8e2dc",        // default hairline border on light surfaces
        muted: "#6b7280",       // secondary text on light surfaces
        cream: "#fdf6f0", // primary text on dark navy surfaces (announcement bar, drawer)
        brand: {
          400: "#fd8a3d", // lighter orange — soft accents, badges
          500: "#fb6f0f", // primary brand orange
          600: "#e35d00", // darker orange — hover/pressed states, text-on-white
        },
        // Real site's hero gradient stops (peach → coral) — used on the
        // homepage hero and the login screen's branded panel.
        hero: {
          from: "#fffaf7",
          via: "#fedecf",
          to: "#fdba9c",
        },
        // Role badge colors — kept independent of the brand accent so
        // they still read as distinct labels, not competing with orange.
        role: {
          admin: "#0284c7",
          writer: "#7c3aed",
          user: "#64748b",
        },
      },
    },
  },
  plugins: [],
}
