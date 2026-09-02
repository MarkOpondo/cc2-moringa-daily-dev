import { useNavigate } from 'react-router-dom';
import { Flame, ArrowUpRight } from 'lucide-react';

export default function SidebarRight({ posts = [], onSelectPost }) {
  const navigate = useNavigate();

  // Safely derive real trending posts (sorted dynamically by highest views_count from DB)
  const trendingPosts = [...posts]
    .sort((a, b) => (b.views_count || 0) - (a.views_count || 0))
    .slice(0, 3);

  // Safely derive real latest posts (sorted dynamically by created_at timestamp from DB)
  const latestPosts = [...posts]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, 3);

  return (
    <aside className="w-80 bg-[#0b0e14] border-l border-slate-800 p-5 flex-col gap-6 min-h-[calc(100vh-4rem)] hidden xl:flex select-none">
      
      {/* TRENDING SECTION */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Flame className="w-4 h-4 text-amber-500 animate-pulse" />
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Trending</h3>
        </div>
        
        <div className="flex flex-col gap-3.5">
          {trendingPosts.length > 0 ? (
            trendingPosts.map((post, index) => (
              <div 
                key={post.content_id || index} 
                onClick={() => onSelectPost && onSelectPost(post)}
                className="flex gap-3 items-start group cursor-pointer p-2 rounded-xl hover:bg-slate-900/50 transition"
              >
                <span className="text-slate-600 font-black text-sm w-4 text-center group-hover:text-emerald-500 transition">
                  0{index + 1}
                </span>
                <div className="flex-1">
                  <h4 className="text-slate-200 text-xs font-semibold group-hover:text-emerald-400 transition line-clamp-2 mb-1 leading-snug">
                    {post.title}
                  </h4>
                  <div className="flex items-center gap-2 text-[10px] text-slate-500">
                    <span className="text-emerald-400 font-medium uppercase">{post.content_type || 'Article'}</span>
                    <span>•</span>
                    <span className="flex items-center gap-0.5 text-slate-400">
                      <ArrowUpRight className="w-3 h-3 text-emerald-400" /> {post.views_count || 0} views
                    </span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 italic px-2">No trending posts found in database.</p>
          )}
        </div>
      </div>

      <hr className="border-slate-800/80" />

      {/* LATEST SECTION */}
      <div>
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-4">Latest</h3>
        
        <div className="flex flex-col gap-3.5">
          {latestPosts.length > 0 ? (
            latestPosts.map((post, index) => (
              <div 
                key={post.content_id || index}
                onClick={() => onSelectPost && onSelectPost(post)}
                className="p-2.5 rounded-xl bg-slate-900/30 border border-slate-800/50 hover:border-slate-700 transition cursor-pointer group"
              >
                <h4 className="text-slate-200 text-xs font-medium group-hover:text-emerald-400 transition line-clamp-2 mb-1.5 leading-snug">
                  {post.title}
                </h4>
                <span className="text-slate-500 text-[10px] font-medium">{post.created_at || 'Recent'}</span>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 italic px-2">No recent posts found.</p>
          )}
        </div>
      </div>

      {/* SAVE FOR LATER BOX (Only shows up when user is logged out) */}
      {!localStorage.getItem('token') && (
        <div className="bg-gradient-to-br from-[#121620] to-[#0e121b] border border-slate-800 rounded-2xl p-4 mt-auto shadow-lg">
          <h4 className="text-slate-100 font-bold text-xs mb-1">Save for later</h4>
          <p className="text-slate-400 text-[11px] mb-4 leading-relaxed">
            Sign in to bookmark content, follow writers, and get personalized recommendations.
          </p>
          <button
            onClick={() => navigate('/signup')}
            className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs py-2.5 rounded-xl transition shadow-md shadow-emerald-500/10 cursor-pointer"
          >
            Create free account
          </button>
        </div>
      )}

    </aside>
  );
}