import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { signupUser } from '../services/authApi';
import PasswordChecklist from '../components/PasswordChecklist';

export default function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showChecklist, setShowChecklist] = useState(true);

  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleAutoGenerate = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()';
    let generated = 'M1!';
    for (let i = 3; i < 14; i++) {
      generated += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setPassword(generated);
    setConfirmPassword(generated);
    setShowChecklist(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    if (!username.trim() || !email.trim() || !password || !confirmPassword) {
      setErrorMsg('Please complete all required fields.');
      return;
    }

    const strictEmailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|co)$/i;
    if (!strictEmailRegex.test(email)) {
      setErrorMsg('Invalid Email: Email must strictly end in .com or .co');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMsg('Passwords do not match.');
      return;
    }

    setIsLoading(true);
    try {
      const data = await signupUser({ username, email, password });
      localStorage.setItem('token', data.token);
      navigate('/dashboard');
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-white">Create Account</h2>
      <p className="text-xs text-slate-400 text-center mt-1">Join Moringa Daily Dev today.</p>

      {errorMsg && (
        <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs text-center">
          {errorMsg}
        </div>
      )}

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Username</label>
          <input 
            type="text" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="moringa_dev"
            className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-sm focus:outline-none focus:border-amber-500 text-white"
          />
        </div>

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

        {/* PASSWORD FIELD */}
        <div>
          <div className="flex justify-between items-center mb-1">
            <label className="block text-xs font-medium text-slate-300">Password</label>
            <button 
              type="button" 
              onClick={handleAutoGenerate} 
              className="text-[11px] text-amber-500 font-semibold hover:underline"
            >
              Auto-Generate
            </button>
          </div>

          <div className="relative">
            <input 
              type={showPassword ? "text" : "password"} 
              value={password}
              onFocus={() => setShowChecklist(true)}
              onChange={(e) => {
                setPassword(e.target.value);
                setShowChecklist(true);
              }}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 pr-10 rounded-lg bg-slate-950 border border-slate-800 text-sm focus:outline-none focus:border-amber-500 text-white"
            />
            
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
        </div>

        {/* EXTERNALIZED PASSWORD CHECKLIST */}
        <PasswordChecklist 
          password={password} 
          showChecklist={showChecklist} 
          setShowChecklist={setShowChecklist} 
        />

        {/* CONFIRM PASSWORD FIELD */}
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Confirm Password</label>
          <div className="relative">
            <input 
              type={showConfirmPassword ? "text" : "password"} 
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 pr-10 rounded-lg bg-slate-950 border border-slate-800 text-sm focus:outline-none focus:border-amber-500 text-white"
            />
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold rounded-lg transition duration-200 disabled:opacity-50"
        >
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>

      <p className="text-xs text-center text-slate-400 mt-6">
        Already have an account?{' '}
        <Link to="/login" className="text-amber-500 font-semibold hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
}