import { useState, useEffect } from 'react';
import { fetchContent } from '../services/contentApi';

export default function TrendingPanel() {
  // store trending and latest posts retrieved live from the database
  const [trendingPosts, setTrendingPosts] = useState([]);
  const [latestPosts, setLatestPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  // fetch and sort posts dynamically so the sidebar displays real database activity instantly
  useEffect(() => {
    async function loadSidebarData() {
      try {
        const data = await fetchContent();
        
        // sort posts by view count to populate the trending section dynamically
        const sortedByViews = [...data].sort((a, b) => (b.views || 0) - (a.views || 0));
        
        // sort posts by creation date to populate the latest section dynamically
        const sortedByDate = [...data].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
        setTrendingPosts(sortedByViews.slice(0, 5)); // display the top 5 most viewed articles
        setLatestPosts(sortedByDate.slice(0, 3));   // display the top 3 newest articles
      } catch (err) {
        console.error('Failed to load sidebar metrics:', err);
      } finally {
        setLoading(false); // remove the loading indicator once data sorting finishes
      }
    }
    loadSidebarData();
  }, []);

  if (loading) {
    return <div className="text-gray-400 text-sm p-4">Loading live metrics...</div>;
  }

  return (
    <aside className="w-80 hidden xl:block space-y-6 text-white text-sm">
      {/* trending section displaying top live stories ranked by user interaction */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 shadow-lg">
        <h4 className="font-bold text-base mb-4 text-white flex items-center justify-between tracking-wide">
          <span>TRENDING</span>
          <span className="text-xs text-green-400 font-mono">LIVE</span>
        </h4>
        <div className="space-y-4">
          {trendingPosts.length === 0 ? (
            <p className="text-gray-400 text-xs">No trending stories found.</p>
          ) : (
            trendingPosts.map((post, index) => (
              <div key={post.id} className="group cursor-pointer">
                <div className="text-xs text-gray-400 mb-1 flex items-center space-x-2 font-mono">
                  <span className="text-green-500 font-bold">0{index + 1}</span>
                  <span>{post.category_name || 'Tech'}</span>
                </div>
                <h5 className="font-semibold text-gray-200 group-hover:text-green-400 transition-colors line-clamp-2">
                  {post.title}
                </h5>
                <div className="text-xs text-gray-400 mt-1">
                  {post.views || 0} views • {post.reading_time || '4 min read'}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* latest section displaying freshly published database records */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 shadow-lg">
        <h4 className="font-bold text-base mb-4 text-white tracking-wide">LATEST</h4>
        <div className="space-y-4">
          {latestPosts.length === 0 ? (
            <p className="text-gray-400 text-xs">No recent posts available.</p>
          ) : (
            latestPosts.map((post) => (
              <div key={post.id} className="group cursor-pointer pb-3 border-b border-gray-800/60 last:border-none last:pb-0">
                <h5 className="font-semibold text-gray-200 group-hover:text-green-400 transition-colors line-clamp-2">
                  {post.title}
                </h5>
                <span className="text-xs text-gray-400 mt-1 block font-mono">
                  {new Date(post.created_at).toLocaleDateString()}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </aside>
  );
}