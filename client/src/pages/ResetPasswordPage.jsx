import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { resetPassword } from '../services/authApi';

// Reached via a link like /reset-password?token=abc123, which is the URL
// the backend's password reset email should point to. The token itself
// is generated and validated server-side — this page just collects the
// new password and forwards the token along with it.
export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords don't match.");
      return;
    }

    setIsLoading(true);
    try {
      await resetPassword(token, password);
      navigate('/login', { state: { justReset: true } });
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="text-center">
        <h2 className="text-2xl font-bold text-navy">Invalid reset link</h2>
        <p className="text-xs text-muted mt-2">
          This link is missing its reset token. Request a new one from the login page.
        </p>
        <Link to="/forgot-password" className="text-brand-500 font-semibold text-xs hover:underline mt-4 inline-block">
          ← Request a new link
        </Link>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-navy">Set a new password</h2>
      <p className="text-xs text-muted text-center mt-1">Choose a new password for your account.</p>

      {error && (
        <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs text-center">
          {error}
        </div>
      )}

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-xs font-medium text-navy/70 mb-1">New password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm focus:outline-none focus:border-brand-500 text-navy"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-navy/70 mb-1">Confirm new password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm focus:outline-none focus:border-brand-500 text-navy"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2.5 bg-brand-500 hover:bg-brand-600 text-white font-semibold rounded-lg transition duration-200 disabled:opacity-50"
        >
          {isLoading ? 'Saving…' : 'Reset Password'}
        </button>
      </form>

      <p className="text-xs text-center text-muted mt-6">
        <Link to="/login" className="text-brand-500 font-semibold hover:underline">
          ← Back to Login
        </Link>
      </p>
    </div>
  );
}
