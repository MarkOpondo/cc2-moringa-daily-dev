import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import { setUser } from '../features/auth/authSlice';
import { signUpUser } from '../services/authApi';

export default function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Password Visibility State
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Password Checklist Dismissal State
  const [showChecklist, setShowChecklist] = useState(true);

  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  // Password Requirements Validation
  const hasMinLength = password.length >= 8;
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

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
      const data = await signUpUser({ username, email, password });
      if (!data?.token) throw new Error('Sign up did not return an access token.');
      if (data.user) {
        dispatch(setUser(data.user));
      }
      navigate('/');
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-center text-cream">Create Account</h2>
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
            className="w-full px-3.5 py-2.5 rounded-lg bg-navy border border-navy-border text-sm focus:outline-none focus:border-brand-500 text-cream"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Email address</label>
          <input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="student@moringa.com"
            className="w-full px-3.5 py-2.5 rounded-lg bg-navy border border-navy-border text-sm focus:outline-none focus:border-brand-500 text-cream"
          />
        </div>

        {/* PASSWORD FIELD */}
        <div>
          <div className="flex justify-between items-center mb-1">
            <label className="block text-xs font-medium text-slate-300">Password</label>
            <button 
              type="button" 
              onClick={handleAutoGenerate} 
              className="text-[11px] text-brand-500 font-semibold hover:underline"
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
              className="w-full px-3.5 py-2.5 pr-10 rounded-lg bg-navy border border-navy-border text-sm focus:outline-none focus:border-brand-500 text-cream"
            />
            
            {/* Hide/Unhide Toggle Button */}
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-cream transition"
              title={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858-5.908a10.02 10.02 0 013.682-.863c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m-2.527 2.527L3 3l18 18" /></svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              )}
            </button>
          </div>
        </div>

        {/* PASSWORD REQUIREMENT CHECKLIST BOX (Disappears when clicked inside) */}
        {showChecklist && (
          <div 
            onClick={() => setShowChecklist(false)}
            className="p-3 bg-navy/90 border border-navy-border rounded-lg text-xs space-y-1.5 cursor-pointer hover:border-navy-border transition"
            title="Click anywhere inside to dismiss"
          >
            <div className="flex justify-between items-center text-slate-400 font-medium mb-1">
              <span>Your password must contain:</span>
              <span className="text-[10px] text-slate-400">(Click box to dismiss)</span>
            </div>
            
            <div className={`flex items-center space-x-2 ${hasMinLength ? 'text-emerald-400' : 'text-slate-400'}`}>
              <span>{hasMinLength ? '✓' : '•'}</span>
              <span>At least 8 characters</span>
            </div>

            <div className={`flex items-center space-x-2 ${(hasLower && hasUpper && hasNumber && hasSpecial) ? 'text-emerald-400' : 'text-slate-400'}`}>
              <span>{(hasLower && hasUpper && hasNumber && hasSpecial) ? '✓' : '•'}</span>
              <span>Includes lowercase, uppercase, number, & special char</span>
            </div>
          </div>
        )}

        {/* CONFIRM PASSWORD FIELD */}
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Confirm Password</label>
          <div className="relative">
            <input 
              type={showConfirmPassword ? "text" : "password"} 
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 pr-10 rounded-lg bg-navy border border-navy-border text-sm focus:outline-none focus:border-brand-500 text-cream"
            />
            
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-cream transition"
              title={showConfirmPassword ? "Hide password" : "Show password"}
            >
              {showConfirmPassword ? (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858-5.908a10.02 10.02 0 013.682-.863c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m-2.527 2.527L3 3l18 18" /></svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              )}
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full py-2.5 bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold rounded-lg transition duration-200 disabled:opacity-50"
        >
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>

      <p className="text-xs text-center text-slate-400 mt-6">
        Already have an account?{' '}
        <Link to="/login" className="text-brand-500 font-semibold hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
}