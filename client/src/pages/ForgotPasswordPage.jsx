import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [statusMsg, setStatusMsg] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email.trim()) return;
    setStatusMsg(`Recovery email sent to ${email} if registered.`);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-white">Reset Password</h2>
      <p className="text-xs text-slate-400 text-center mt-1">Enter your registered email to receive instructions.</p>

      {statusMsg && (
        <div className="mt-4 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs text-center">
          {statusMsg}
        </div>
      )}

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Email address</label>
          <input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="student@moringa.com"
            className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-sm focus:outline-none focus:border-amber-500 text-white"
          />
        </div>

        <button 
          type="submit" 
          className="w-full py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold rounded-lg transition duration-200"
        >
          Send Reset Link
        </button>
      </form>

      <p className="text-xs text-center text-slate-400 mt-6">
        <Link to="/login" className="text-amber-500 font-semibold hover:underline">
          ← Back to Login
        </Link>
      </p>
    </div>
  );
}