import { Outlet } from 'react-router-dom';
import StudentIllustration from '../components/illustrations/StudentIllustration';

export default function AuthLayout() {
  return (
    <div className="min-h-screen w-full grid grid-cols-1 lg:grid-cols-2 bg-white text-navy">
      
      {/* LEFT COLUMN: Illustration + branding, using the same peach → coral
          gradient as the real marketing site's homepage hero. */}
      <div className="hidden lg:flex flex-col justify-between p-12 bg-gradient-to-b from-hero-from via-hero-via to-hero-to border-r border-line">
        <span className="text-brand-600 font-semibold text-xs tracking-wider uppercase bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20 w-fit">
          Moringa Daily Dev
        </span>

        <div className="my-auto -mt-8">
          <StudentIllustration className="w-full max-w-sm mx-auto" />
          <h1 className="text-2xl font-display font-bold text-center text-navy mt-6">
            Learn out loud, together.
          </h1>
        </div>

        <p className="text-xs text-navy/60">
          © {new Date().getFullYear()} Moringa Daily Dev. All rights reserved.
        </p>
      </div>

      {/* RIGHT COLUMN: Dynamic Auth Page Outlet */}
      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md p-8 bg-surface rounded-2xl border border-line shadow-2xl">
          <Outlet />
        </div>
      </div>

    </div>
  );
}
