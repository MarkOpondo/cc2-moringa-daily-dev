import { Outlet } from 'react-router-dom';
import StudentIllustration from '../components/illustrations/StudentIllustration';

export default function AuthLayout() {
  return (
    <div className="min-h-screen w-full grid grid-cols-1 lg:grid-cols-2 bg-slate-950 text-slate-100">
      
      {/* LEFT COLUMN: Illustration + light branding */}
      <div className="hidden lg:flex flex-col justify-between p-12 bg-gradient-to-br from-amber-500/10 via-slate-900 to-slate-950 border-r border-slate-800/80">
        <span className="text-amber-500 font-semibold text-xs tracking-wider uppercase bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20 w-fit">
          Moringa Daily Dev
        </span>

        <div className="my-auto -mt-8">
          <StudentIllustration className="w-full max-w-sm mx-auto" />
          <h1 className="text-2xl font-display font-bold text-center text-white mt-6">
            Learn out loud, together.
          </h1>
        </div>

        <p className="text-xs text-slate-600">
          © {new Date().getFullYear()} Moringa Daily Dev. All rights reserved.
        </p>
      </div>

      {/* RIGHT COLUMN: Dynamic Auth Page Outlet */}
      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md p-8 bg-slate-900/60 rounded-2xl border border-slate-800/80 shadow-2xl backdrop-blur-sm">
          <Outlet />
        </div>
      </div>

    </div>
  );
}