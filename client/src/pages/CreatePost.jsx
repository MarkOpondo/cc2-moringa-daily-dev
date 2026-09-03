import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Sparkles, Send, Upload, Image as ImageIcon, Leaf } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001';

export default function CreatePost() {
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [description, setDescription] = useState('');
  const [contentType, setContentType] = useState('article');
  const [categories, setCategories] = useState([]);
  const [categoryId, setCategoryId] = useState('');
  const [readTime, setReadTime] = useState('');
  const [tags, setTags] = useState('');
  
  // File upload states
  const [thumbnailFile, setThumbnailFile] = useState(null);
  const [mediaFile, setMediaFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const navigate = useNavigate();

  // Listen for AI Content Insertion Events
  useEffect(() => {
    const handleAiInsert = (e) => {
      const textToInsert = e.detail;
      if (!textToInsert) return;

      setDescription((prev) => (prev ? `${prev}\n\n${textToInsert}` : textToInsert));
    };

    window.addEventListener('ai-insert-content', handleAiInsert);
    return () => window.removeEventListener('ai-insert-content', handleAiInsert);
  }, []);

  // Helper to retrieve auth token
  const getAuthToken = () => {
    let token = localStorage.getItem('token') || localStorage.getItem('access_token');
    if (token) return token;

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('hl_session_')) {
        try {
          const sessionData = JSON.parse(localStorage.getItem(key));
          if (sessionData && sessionData.access_token) {
            return sessionData.access_token;
          }
        } catch {
          // Ignore JSON parse errors
        }
      }
    }
    return null;
  };

  // Fetch categories dynamically from backend
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/categories`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setCategories(data);
          if (data.length > 0) {
            setCategoryId(data[0].id || data[0].CategoryID || data[0].category_id);
          }
        }
      })
      .catch((err) => console.error('Failed to fetch categories:', err));
  }, []);

  const handleSubmit = async (e, isDraft = false) => {
    e.preventDefault();
    setErrorMsg('');
    const token = getAuthToken();

    if (!token) {
      alert('You must be signed in to create a post!');
      navigate('/login');
      return;
    }

    if (!title.trim() || !summary.trim() || !description.trim()) {
      setErrorMsg('Please fill in all required fields (Title, Summary, and Body).');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('summary', summary);
      formData.append('description', description);
      formData.append('content_type', contentType);
      formData.append('category_id', categoryId);
      formData.append('duration', readTime || '5');
      formData.append('hashtags', tags);
      formData.append('is_draft', isDraft);

      if (thumbnailFile) {
        formData.append('thumbnail', thumbnailFile);
      }
      if (mediaFile) {
        formData.append('media_file', mediaFile);
      }

      const response = await fetch(`${API_BASE_URL}/api/content`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}` 
        },
        body: formData
      });

      if (response.ok) {
        if (isDraft) {
          navigate('/');
        } else {
          setIsSubmitted(true);
        }
      } else {
        const errorData = await response.json();
        setErrorMsg(errorData.error || 'Failed to create content');
      }
    } catch (err) {
      console.error('Network error:', err);
      setErrorMsg('An error occurred while connecting to the server.');
    } finally {
      setLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-[#07090e] text-slate-100 flex flex-col items-center justify-center px-4">
        <div className="text-center max-w-md mx-auto space-y-6">
          <div className="w-16 h-16 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl mx-auto flex items-center justify-center text-emerald-400 shadow-xl shadow-emerald-500/5">
            <Leaf className="w-8 h-8" />
          </div>
          
          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight text-white font-serif">Submitted for review!</h1>
            <p className="text-xs text-slate-400 leading-relaxed px-4">
              Your content has been submitted and will be reviewed by an admin before going live.
            </p>
          </div>

          <Link
            to="/"
            className="inline-block bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs px-8 py-3.5 rounded-xl transition shadow-lg shadow-emerald-500/20 cursor-pointer"
          >
            Back to feed
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090e] text-slate-100 py-10 px-4 sm:px-8 lg:px-12">
      <div className="max-w-4xl mx-auto">
        
        {/* Navigation Header */}
        <div className="flex items-center justify-between mb-6">
          <Link 
            to="/" 
            className="inline-flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-emerald-400 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Feed</span>
          </Link>
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3.5 py-1.5 rounded-full">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Creator Studio</span>
          </div>
        </div>

        {/* Main Form Box */}
        <div className="bg-[#0f131d] border border-slate-800/80 rounded-3xl p-8 sm:p-10 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500"></div>

          <div className="mb-8">
            <h1 className="text-2xl font-bold text-white">Create Content</h1>
            <p className="text-xs text-slate-400 mt-1">
              Share your knowledge with the community. Submissions require admin approval before going live.
            </p>
          </div>

          {errorMsg && (
            <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs flex items-center gap-2">
              <span>⚠️</span>
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={(e) => handleSubmit(e, false)} className="space-y-6">
            
            {/* CONTENT TYPE SELECTOR CARDS */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Content Type</label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div 
                  onClick={() => setContentType('article')}
                  className={`p-4 rounded-2xl border cursor-pointer transition flex flex-col justify-between ${contentType === 'article' ? 'bg-emerald-500/10 border-emerald-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">✍️</span>
                    {contentType === 'article' && <div className="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-200">Article</p>
                    <p className="text-[11px] text-slate-400 mt-0.5">Written post or tutorial</p>
                  </div>
                </div>

                <div 
                  onClick={() => setContentType('video')}
                  className={`p-4 rounded-2xl border cursor-pointer transition flex flex-col justify-between ${contentType === 'video' ? 'bg-emerald-500/10 border-emerald-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">🎬</span>
                    {contentType === 'video' && <div className="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-200">Video</p>
                    <p className="text-[11px] text-slate-400 mt-0.5">Video content or recording</p>
                  </div>
                </div>

                <div 
                  onClick={() => setContentType('podcast')}
                  className={`p-4 rounded-2xl border cursor-pointer transition flex flex-col justify-between ${contentType === 'podcast' ? 'bg-emerald-500/10 border-emerald-500 text-white' : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">🎙️</span>
                    {contentType === 'podcast' && <div className="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-200">Podcast</p>
                    <p className="text-[11px] text-slate-400 mt-0.5">Audio interview or podcast</p>
                  </div>
                </div>
              </div>
            </div>

            {/* TITLE */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Title *</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Give your content a clear, descriptive title"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition shadow-inner"
                required
              />
            </div>

            {/* SUMMARY */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Summary / Excerpt *</label>
              <textarea
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="2-3 sentences that hook the reader and describe what they'll learn"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-white placeholder-slate-600 h-20 focus:outline-none focus:border-emerald-500 transition resize-none shadow-inner"
                required
              />
            </div>

            {/* BODY */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                {contentType === 'article' ? 'Article Body *' : contentType === 'video' ? 'Video Details / Show Notes *' : 'Episode Show Notes *'}
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Write your full content here... Use '## Heading' for sections."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-white placeholder-slate-600 h-48 font-mono focus:outline-none focus:border-emerald-500 transition resize-none shadow-inner"
                required
              />
            </div>

            {/* MEDIA FILE UPLOAD */}
            {contentType !== 'article' && (
              <div className="p-5 bg-slate-950 border border-slate-800 rounded-2xl">
                <label className="block text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Upload className="w-4 h-4" />
                  <span>Upload {contentType === 'video' ? 'Video File (.mp4)' : 'Podcast Audio (.mp3, .wav)'} *</span>
                </label>
                <input
                  type="file"
                  accept={contentType === 'video' ? 'video/mp4,video/quicktime' : 'audio/mpeg,audio/wav'}
                  onChange={(e) => setMediaFile(e.target.files[0])}
                  className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-emerald-500/10 file:text-emerald-400 hover:file:bg-emerald-500/20 cursor-pointer"
                />
              </div>
            )}

            {/* CATEGORY & DURATION */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Category *</label>
                <select
                  value={categoryId}
                  onChange={(e) => setCategoryId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-emerald-500 transition cursor-pointer"
                >
                  {categories.map((cat) => {
                    const catId = cat.id || cat.CategoryID || cat.category_id;
                    const catName = cat.name || cat.Name || cat.category_name;
                    return (
                      <option key={catId} value={catId}>
                        {catName}
                      </option>
                    );
                  })}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  {contentType === 'article' ? 'Read Time (min)' : 'Duration (min)'}
                </label>
                <input
                  type="number"
                  value={readTime}
                  onChange={(e) => setReadTime(e.target.value)}
                  placeholder="e.g. 5"
                  min="1"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-emerald-500 transition"
                />
              </div>
            </div>

            {/* THUMBNAIL */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                <ImageIcon className="w-4 h-4 text-emerald-400" />
                <span>Thumbnail / Cover Image *</span>
              </label>
              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(e) => setThumbnailFile(e.target.files[0])}
                className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer bg-slate-950 border border-slate-800 rounded-xl p-2"
              />
            </div>

            {/* TAGS */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Tags</label>
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="python, flask, backend, api (comma separated)"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition"
              />
            </div>

            {/* ACTION BUTTONS */}
            <div className="flex items-center gap-4 pt-4 border-t border-slate-800">
              <button
                type="button"
                onClick={(e) => handleSubmit(e, true)}
                disabled={loading}
                className="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs py-3.5 rounded-xl transition cursor-pointer disabled:opacity-50"
              >
                Save as draft
              </button>

              <button
                type="submit"
                disabled={loading}
                className="w-2/3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs py-3.5 rounded-xl transition cursor-pointer shadow-lg shadow-emerald-500/20 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" />
                <span>{loading ? 'Submitting...' : 'Submit for review'}</span>
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  );
}