

export default function StudentIllustration({ className = "" }) {
  return (
    <svg viewBox="0 0 400 400" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Ground shadow */}
      <ellipse cx="205" cy="345" rx="130" ry="14" fill="#020617" opacity="0.5" />

      {/* Ambient glow behind the scene */}
      <circle cx="200" cy="190" r="150" fill="url(#glow)" opacity="0.5" />

      {/* Floating accent particles — category-color palette, decorative */}
      <circle cx="72" cy="110" r="6" fill="#38bdf8" opacity="0.7" />
      <circle cx="340" cy="150" r="5" fill="#a78bfa" opacity="0.6" />
      <circle cx="325" cy="260" r="7" fill="#34d399" opacity="0.55" />
      <circle cx="60" cy="230" r="4" fill="#fb7185" opacity="0.6" />
      <circle cx="90" cy="290" r="5" fill="#f59e0b" opacity="0.5" />

      {/* Chat bubble, top-left — represents comments/discussion */}
      <g transform="translate(48, 60)">
        <rect width="72" height="48" rx="14" fill="#1e293b" stroke="#334155" />
        <path d="M18 48 L18 62 L34 48 Z" fill="#1e293b" stroke="#334155" />
        <circle cx="22" cy="24" r="4" fill="#64748b" />
        <circle cx="36" cy="24" r="4" fill="#64748b" />
        <circle cx="50" cy="24" r="4" fill="#f59e0b" />
      </g>

      {/* Notification bell, top-right */}
      <g transform="translate(300, 70)">
        <circle cx="24" cy="24" r="24" fill="#1e293b" stroke="#334155" />
        <path
          d="M24 12c-4.5 0-8 3.6-8 8v5l-3 5h22l-3-5v-5c0-4.4-3.5-8-8-8z"
          fill="#94a3b8"
        />
        <path d="M20 32a4 4 0 008 0" stroke="#94a3b8" strokeWidth="1.5" fill="none" />
        <circle cx="34" cy="12" r="6" fill="#f59e0b" />
      </g>

      {/* Bookmark ribbon, floating alongside the other UI accents */}
      <g transform="translate(58, 190)">
        <path d="M0 0 H22 V32 L11 24 L0 32 Z" fill="#f59e0b" opacity="0.9" />
      </g>

      {/* Desk */}
      <rect x="70" y="288" width="260" height="10" rx="4" fill="#1e293b" />

      {/* Chair back, behind the figure */}
      <rect x="150" y="150" width="90" height="150" rx="22" fill="#1e293b" />

      {/* Figure: flat silhouette, deliberately abstract/non-specific */}
      <g>
        {/* legs */}
        <rect x="168" y="255" width="26" height="45" rx="10" fill="#334155" />
        <rect x="198" y="255" width="26" height="45" rx="10" fill="#334155" />
        {/* torso */}
        <rect x="158" y="188" width="76" height="90" rx="30" fill="#f59e0b" />
        {/* head */}
        <circle cx="196" cy="168" r="26" fill="#fbbf24" />
        {/* arm reaching down to the keyboard — extended to actually touch the keys */}
        <path
          d="M226 216 Q 262 222 264 262 L 248 268 Q 246 234 220 224 Z"
          fill="#fbbf24"
        />
      </g>

      {/* Laptop base */}
      <path d="M230 268 L 330 268 L 322 280 L 222 280 Z" fill="#334155" />
      {/* Laptop screen */}
      <rect x="238" y="188" width="86" height="80" rx="6" fill="#020617" stroke="#334155" strokeWidth="2" />

      {/* Mini app UI rendered on the laptop screen, echoing the real ContentCard */}
      <g transform="translate(246, 196)">
        <rect width="70" height="8" rx="2" fill="#1e293b" />
        <rect x="0" y="4" width="24" height="2" rx="1" fill="#f59e0b" />

        {/* card 1 */}
        <rect x="0" y="16" width="3" height="16" rx="1.5" fill="#38bdf8" />
        <rect x="7" y="18" width="40" height="4" rx="2" fill="#475569" />
        <rect x="7" y="25" width="55" height="3" rx="1.5" fill="#334155" />

        {/* card 2 */}
        <rect x="0" y="38" width="3" height="16" rx="1.5" fill="#a78bfa" />
        <rect x="7" y="40" width="50" height="4" rx="2" fill="#475569" />
        <rect x="7" y="47" width="35" height="3" rx="1.5" fill="#334155" />

        {/* small reaction icon, bottom right of screen */}
        <circle cx="60" cy="58" r="6" fill="#1e293b" />
        <path d="M57.5 58.5 L59.5 60.5 L63 56.5" stroke="#34d399" strokeWidth="1.3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>

      <defs>
        <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.18" />
          <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
        </radialGradient>
      </defs>
    </svg>
  );
}
