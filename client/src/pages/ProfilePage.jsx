import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchProfile, updateProfile } from '../services/profileApi';

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    bio: '',
    skills: '',
    github_url: '',
  });
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [statusMsg, setStatusMsg] = useState({ type: '', text: '' });
  const navigate = useNavigate();

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await fetchProfile();
        setProfile({
          username: data.username || '',
          email: data.email || '',
          bio: data.bio || '',
          skills: data.skills || '',
          github_url: data.github_url || '',
        });
      } catch (err) {
        setStatusMsg({ type: 'error', text: err.message });
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setStatusMsg({ type: '', text: '' });
    try {
      await updateProfile({
        bio: profile.bio,
        skills: profile.skills,
        github_url: profile.github_url,
      });
      setStatusMsg({ type: 'success', text: 'Profile updated successfully!' });
      setIsEditing(false);
    } catch (err) {
      setStatusMsg({ type: 'error', text: err.message });
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <p className="text-slate-400 text-sm">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 w-full">
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-amber-500">Developer Profile</h1>
          <button
            onClick={handleLogout}
            className="px-3.5 py-1.5 text-xs bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-lg transition"
          >
            Logout
          </button>
        </div>

        {statusMsg.text && (
          <div
            className={`mb-4 p-3 rounded-lg text-xs text-center border ${
              statusMsg.type === 'error'
                ? 'bg-red-500/10 border-red-500/20 text-red-400'
                : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
            }`}
          >
            {statusMsg.text}
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div>
            <label className="block text-xs text-slate-400">Username</label>
            <p className="text-base font-semibold text-slate-200">{profile.username}</p>
          </div>

          <div>
            <label className="block text-xs text-slate-400">Email</label>
            <p className="text-base font-semibold text-slate-200">{profile.email}</p>
          </div>

          {isEditing ? (
            <form onSubmit={handleSave} className="space-y-4 pt-2">
              <div>
                <label className="block text-xs text-slate-300 mb-1">Bio</label>
                <textarea
                  value={profile.bio}
                  onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-amber-500"
                  rows="3"
                />
              </div>

              <div>
                <label className="block text-xs text-slate-300 mb-1">Skills / Tech Stack</label>
                <input
                  type="text"
                  value={profile.skills}
                  onChange={(e) => setProfile({ ...profile, skills: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs text-slate-300 mb-1">GitHub Profile URL</label>
                <input
                  type="url"
                  value={profile.github_url}
                  onChange={(e) => setProfile({ ...profile, github_url: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-amber-500"
                />
              </div>

              <div className="flex gap-2">
                <button
                  type="submit"
                  className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs rounded-lg transition"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div className="space-y-4 pt-2 border-t border-slate-800">
              <div>
                <label className="block text-xs text-slate-400">Bio</label>
                <p className="text-sm text-slate-300">{profile.bio || 'No bio added yet.'}</p>
              </div>

              <div>
                <label className="block text-xs text-slate-400">Skills</label>
                <p className="text-sm text-slate-300">{profile.skills || 'No skills listed yet.'}</p>
              </div>

              <div>
                <label className="block text-xs text-slate-400">GitHub</label>
                {profile.github_url ? (
                  <a
                    href={profile.github_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm text-amber-500 hover:underline"
                  >
                    {profile.github_url}
                  </a>
                ) : (
                  <p className="text-sm text-slate-300">Not provided</p>
                )}
              </div>

              <button
                onClick={() => setIsEditing(true)}
                className="mt-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs rounded-lg transition"
              >
                Edit Profile
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}