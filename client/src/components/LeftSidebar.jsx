import { useState } from 'react';

export default function LeftSidebar({ activeTab, onSelectTab }) {
  // track active navigation item so the user sees clear visual feedback on where they are in the app
  const [active, setActive] = useState(activeTab || 'home');

  const handleNavClick = (tabId) => {
    setActive(tabId);
    if (onSelectTab) onSelectTab(tabId); // pass selected tab upward so parent views can update accordingly
  };

  return (
    <aside className="w-64 hidden lg:flex flex-col justify-between h-screen sticky top-0 bg-black border-r border-gray-800 p-6 text-gray-400">
      <div className="space-y-8">
        {/* brand logo matching the figma header style */}
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center font-bold text-black text-lg">
            M
          </div>
          <span className="text-white font-bold text-lg tracking-wide">MoringaHub</span>
        </div>

        {/* discover navigation section */}
        <div className="space-y-2">
          <p className="text-xs font-mono uppercase text-gray-400 tracking-wider mb-3">Discover</p>
          <button
            onClick={() => handleNavClick('home')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'home' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>🏠 Home Feed</span>
          </button>
          <button
            onClick={() => handleNavClick('devops')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'devops' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>⚙️ DevOps</span>
          </button>
          <button
            onClick={() => handleNavClick('fullstack')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'fullstack' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>💻 Fullstack</span>
          </button>
          <button
            onClick={() => handleNavClick('frontend')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'frontend' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>🎨 Frontend</span>
          </button>
          <button
            onClick={() => handleNavClick('backend')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'backend' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>🗄️ Backend</span>
          </button>
        </div>

        {/* content types section matching the media filters in the figma mockup */}
        <div className="space-y-2">
          <p className="text-xs font-mono uppercase text-gray-400 tracking-wider mb-3">Content Types</p>
          <button
            onClick={() => handleNavClick('articles')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'articles' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>📄 Articles</span>
          </button>
          <button
            onClick={() => handleNavClick('videos')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'videos' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>🎥 Videos</span>
          </button>
          <button
            onClick={() => handleNavClick('podcasts')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              active === 'podcasts' ? 'bg-gray-800 text-green-400 font-semibold' : 'hover:text-white hover:bg-gray-900'
            }`}
          >
            <span>🎙️ Podcasts</span>
          </button>
        </div>
      </div>

      {/* call to action box at the bottom of the sidebar as seen in the figma layout */}
      <div className="bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-xl p-4 shadow-lg">
        <h5 className="text-white font-bold text-sm mb-1">Join MoringaHub</h5>
        <p className="text-xs text-gray-400 mb-3 leading-relaxed">
          Subscribe to categories, save content, and join the conversation.
        </p>
        <button 
          onClick={() => window.location.href = '/signup'}
          className="w-full bg-green-500 hover:bg-green-400 text-black font-semibold text-xs py-2 px-3 rounded-lg transition-colors"
        >
          Get started
        </button>
      </div>
    </aside>
  );
}