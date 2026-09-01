const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001';

export default function UserAvatar({ username, profileImage, size = "w-8 h-8" }) {
  const imageUrl = profileImage 
    ? (profileImage.startsWith('http') ? profileImage : `${API_BASE_URL}${profileImage}`) 
    : null;

  return (
    <div className="flex items-center gap-2">
      <div className={`${size} rounded-full overflow-hidden bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0`}>
        {imageUrl ? (
          <img src={imageUrl} alt={username} className="w-full h-full object-cover" />
        ) : (
          <span className="text-xs font-bold text-slate-300 uppercase">
            {username?.charAt(0) || 'U'}
          </span>
        )}
      </div>
      {username && <span className="text-xs font-medium text-slate-200">{username}</span>}
    </div>
  );
}