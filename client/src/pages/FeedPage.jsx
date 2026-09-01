import { useState, useEffect } from 'react';
import { fetchContent, fetchCategories } from '../services/contentApi';

export default function FeedPage() {
  // store the list of posts returned by the backend database to display in the main feed area
  const [posts, setPosts] = useState([]);
  
  // store category options fetched live so the filter navigation bar reflects database records accurately
  const [categories, setCategories] = useState([]);
  
  // track the currently active category filter so selecting a tab updates the API query parameters instantly
  const [selectedCategory, setSelectedCategory] = useState('');
  
  // handle loading states while waiting for network responses so the user sees proper visual feedback
  const [loading, setLoading] = useState(true);
  
  // capture any server errors to display a readable fallback message instead of breaking the interface
  const [error, setError] = useState(null);

  // fetch categories and initial feed data when the component first mounts on the screen
  useEffect(() => {
    async function loadInitialData() {
      try {
        // grab categories and default content simultaneously to optimize page load time
        const [categoriesData, contentData] = await Promise.all([
          fetchCategories(),
          fetchContent()
        ]);
        setCategories(categoriesData);
        setPosts(contentData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false); // clear the loading spinner once data processing finishes successfully
      }
    }
    loadInitialData();
  }, []);

  // re-fetch content whenever the user clicks a different category tab to filter the live feed dynamically
  useEffect(() => {
    async function handleCategoryChange() {
      try {
        setLoading(true);
        const data = await fetchContent(selectedCategory);
        setPosts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    handleCategoryChange();
  }, [selectedCategory]);

  if (loading && posts.length === 0) {
    return <div className="text-center py-12 text-gray-400">Loading live community content...</div>;
  }

  if (error) {
    return <div className="text-center py-12 text-red-500">Error loading feed: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* dynamic category filter bar matching the figma design layout */}
      <div className="flex items-center space-x-4 overflow-x-auto pb-4 border-b border-gray-800">
        <button
          onClick={() => setSelectedCategory('')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            selectedCategory === '' ? 'bg-green-500 text-black font-semibold' : 'text-gray-400 hover:text-white bg-gray-900'
          }`}
        >
          All
        </button>
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              selectedCategory === category.id ? 'bg-green-500 text-black font-semibold' : 'text-gray-400 hover:text-white bg-gray-900'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* main content grid displaying real database posts instead of hardcoded templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {posts.length === 0 ? (
          <p className="text-gray-400 col-span-2 text-center py-10">No content found for this category yet.</p>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden shadow-lg p-5">
              <div className="flex items-center space-x-2 mb-3">
                <span className="text-xs px-2.5 py-1 bg-gray-800 text-green-400 rounded-md font-mono">
                  {post.category_name || 'Tech'}
                </span>
                <span className="text-xs text-gray-400">{post.reading_time || '5 min read'}</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2 hover:text-green-400 transition-colors cursor-pointer">
                {post.title}
              </h3>
              <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                {post.summary || post.body}
              </p>
              <div className="flex items-center justify-between pt-4 border-t border-gray-800/60 text-xs text-gray-400">
                <span>By {post.author_name || 'Community Member'}</span>
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}