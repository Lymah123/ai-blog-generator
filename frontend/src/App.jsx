import React, { useState, useEffect } from 'react';
import { Sparkles, AlertCircle, CheckCircle } from 'lucide-react';
import BlogForm from './components/BlogForm';
import BlogDisplay from './components/BlogDisplay';
import BlogHistory from './components/BlogHistory';
import { blogAPI, checkHealth } from './services/api';

function App() {
  const [currentBlog, setCurrentBlog] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const [refreshHistory, setRefreshHistory] = useState(0);

  // Check API health on mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await checkHealth();
        setApiStatus('connected');
      } catch (err) {
        setApiStatus('disconnected');
        console.error('API health check failed:', err);
      }
    };
    checkAPI();
  }, []);

  const handleGenerate = async (formData) => {
    setIsGenerating(true);
    setError(null);
    setSuccess(false);

    try {
      const result = await blogAPI.generateBlog(formData);
      setCurrentBlog(result);
      setSuccess(true);
      setRefreshHistory((prev) => prev + 1); // Trigger history refresh

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to generate blog post';
      setError(errorMessage);
      console.error('Error generating blog:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSelectBlog = (blog) => {
    setCurrentBlog(blog);
    setError(null);
    setSuccess(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Blog Generator</h1>
                <p className="text-sm text-gray-600">Powered by AI • Create content in seconds</p>
              </div>
            </div>

            {/* API Status Indicator */}
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${apiStatus === 'connected'
                    ? 'bg-green-500'
                    : apiStatus === 'disconnected'
                      ? 'bg-red-500'
                      : 'bg-yellow-500'
                  }`}
              />
              <span className="text-sm text-gray-600">
                {apiStatus === 'connected'
                  ? 'Connected'
                  : apiStatus === 'disconnected'
                    ? 'Disconnected'
                    : 'Checking...'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert Messages */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-medium text-red-900 mb-1">Error</h3>
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-red-600 hover:text-red-800"
            >
              ×
            </button>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-medium text-green-900 mb-1">Success!</h3>
              <p className="text-sm text-green-700">Your blog post has been generated successfully.</p>
            </div>
            <button
              onClick={() => setSuccess(false)}
              className="text-green-600 hover:text-green-800"
            >
              ×
            </button>
          </div>
        )}

        {/* API Disconnected Warning */}
        {apiStatus === 'disconnected' && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-medium text-yellow-900 mb-1">Backend Disconnected</h3>
              <p className="text-sm text-yellow-700">
                Cannot connect to the API server. Make sure the backend is running at{' '}
                <code className="bg-yellow-100 px-1 rounded">
                  {import.meta.env.VITE_API_URL || 'http://localhost:8000'}
                </code>
              </p>
            </div>
          </div>
        )}

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Form */}
          <div className="space-y-8">
            <BlogForm onGenerate={handleGenerate} isGenerating={isGenerating} />
          </div>

          {/* Right Column - Display */}
          <div className="space-y-8">
            <BlogDisplay blog={currentBlog} />
          </div>
        </div>

        {/* Blog History - Full Width */}
        <div className="mt-12">
          <BlogHistory onSelectBlog={handleSelectBlog} refreshTrigger={refreshHistory} />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>
              Built with ❤️ using React, FastAPI, and Hugging Face •{' '}
              <a
                href="https://github.com/Lymah123/ai-blog-generator"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                View on GitHub
              </a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;