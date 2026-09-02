import { useNavigate } from 'react-router-dom';
import { 
  Zap, 
  Server, 
  Link2, 
  Palette, 
  Settings, 
  Smartphone, 
  Rocket, 
  Bot, 
  Folder 
} from 'lucide-react';

export default function SidebarLeft({ categories = [], currentTab = 'All', setCurrentTab }) {
  const navigate = useNavigate();

  // Helper to map category names to their exact Figma icons
  const getCategoryIcon = (name) => {
    switch (name.toLowerCase()) {
      case 'all':
        return <Zap className="w-4 h-4 text-emerald-400" />;
      case 'devops':
        return <Server className="w-4 h-4 text-sky-400" />;
      case 'fullstack':
        return <Link2 className="w-4 h-4 text-indigo-400" />;
      case 'frontend':
        return <Palette className="w-4 h-4 text-pink-400" />;
      case 'backend':
        return <Settings className="w-4 h-4 text-amber-400" />;
      case 'mobile':
        return <Smartphone className="w-4 h-4 text-purple-400" />;
      case 'career':
        return <Rocket className="w-4 h-4 text-red-400" />;
      case 'ai/ml':
      case 'aiml':
        return <Bot className="w-4 h-4 text-cyan-400" />;
      default:
        return <Folder className="w-4 h-4 text-slate-400" />;
    }
  };

  const contentTypeItems = [
    { name: 'Articles', dotColor: 'bg-emerald-400' },
    { name: 'Videos', dotColor: 'bg-blue-500' },
    { name: 'Podcasts', dotColor: 'bg-purple-500' },
  ];

  return (
    <aside className="w-64 bg-[#0b0e14] border-r border-slate-800 flex flex-col p-4 select-none min-h-[calc(100vh-4rem)] shrink-0">
      
      {/* Brand / Logo */}
      <div 
        onClick={() => setCurrentTab('All')}
        className="flex items-center gap-3 mb-8 px-2 cursor-pointer group"
      >
        <div className="w-8 h-8 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition">
          <span className="text-slate-950 font-black text-sm tracking-tighter">M</span>
        </div>
        <span className="text-slate-100 font-bold text-base tracking-tight group-hover:text-emerald-400 transition">
          MoringaHub
        </span>
      </div>

      {/* DISCOVER SECTION */}
      <div className="mb-6">
        <p className="text-[10px] font-bold tracking-wider text-slate-500 uppercase px-2 mb-2">
          Discover
        </p>
        <nav className="space-y-1">
          {/* 'All' Tab */}
          <button
            onClick={() => setCurrentTab('All')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition ${
              currentTab.toLowerCase() === 'all'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
            }`}
          >
            <div className="flex items-center gap-3">
              <Zap className="w-4 h-4 text-emerald-400" />
              <span>All</span>
            </div>
            {currentTab.toLowerCase() === 'all' && (
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            )}
          </button>

          {/* Dynamic Database Categories */}
          {categories.map((cat) => {
            const isSelected = currentTab.toLowerCase() === cat.name.toLowerCase();
            return (
              <button
                key={cat.id}
                onClick={() => setCurrentTab(cat.name)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition ${
                  isSelected
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <div className="flex items-center gap-3">
                  {getCategoryIcon(cat.name)}
                  <span>{cat.name}</span>
                </div>
                {isSelected && (
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* CONTENT TYPES SECTION */}
      <div className="mb-6">
        <p className="text-[10px] font-bold tracking-wider text-slate-500 uppercase px-2 mb-2">
          Content Types
        </p>
        <nav className="space-y-1">
          {contentTypeItems.map((type) => {
            const isSelected = currentTab.toLowerCase() === type.name.toLowerCase();
            return (
              <button
                key={type.name}
                onClick={() => setCurrentTab(type.name)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition ${
                  isSelected
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className={`w-2 h-2 rounded-full ${type.dotColor}`}></span>
                  <span>{type.name}</span>
                </div>
                {isSelected && (
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Join MoringaHub Box (Only shows up when user is logged out) */}
      {!localStorage.getItem('token') && (
        <div className="mt-auto bg-gradient-to-br from-[#121620] to-[#0e121b] border border-slate-800 rounded-2xl p-4 text-left shadow-lg">
          <h4 className="text-xs font-bold text-slate-100 mb-1">Join MoringaHub</h4>
          <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
            Subscribe to categories, save content, and join the conversation.
          </p>
          <button 
            onClick={() => navigate('/signup')}
            className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs py-2.5 rounded-xl transition shadow-md shadow-emerald-500/10 cursor-pointer"
          >
            Get started
          </button>
        </div>
      )}
    </aside>
  );
}