import React, { useState, useEffect } from 'react';
import { History, Trash2, Eye, Calendar, FileText, Loader2, RefreshCw } from 'lucide-react';
import { blogAPI } from '../services/api';
import { formatDate, truncateText, getSEOScoreColor } from '../utils/helpers';

const BlogHistory = ({ onSelectBlog, refreshTrigger }) => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleting, setDeleting] = useState(null);

  const fetchBlogs = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await blogAPI.getAllBlogs();
      setBlogs(data.blogs || []);
    } catch (err) {
      setError('Failed to load blog history');
      console.error('Error fetching blogs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlogs();
  }, [refreshTrigger]);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this blog post?')) {
      return;
    }

    try {
      setDeleting(id);
      await blogAPI.deleteBlog(id);
      setBlogs(blogs.filter((blog) => blog.id !== id));
    } catch (err) {
      alert('Failed to delete blog post');
      console.error('Error deleting blog:', err);
    } finally {
      setDeleting(null);
    }
  };

  const handleView = (blog) => {
    onSelectBlog(blog);
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-primary-600 animate-spin" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="text-center py-12">
          <div className="text-red-600 mb-4">{error}</div>
          <button onClick={fetchBlogs} className="btn-primary flex items-center gap-2 mx-auto">
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-100 rounded-lg">
            <History className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Blog History</h2>
            <p className="text-sm text-gray-600">
              {blogs.length} {blogs.length === 1 ? 'post' : 'posts'} generated
            </p>
          </div>
        </div>
        <button
          onClick={fetchBlogs}
          className="btn-secondary flex items-center gap-2"
          title="Refresh"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {blogs.length === 0 ? (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Blogs Yet</h3>
          <p className="text-gray-600">
            Generate your first blog post to see it here
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {blogs.map((blog) => (
            <div
              key={blog.id}
              className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-md transition-all duration-200 cursor-pointer group"
              onClick={() => handleView(blog)}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                    {blog.title || blog.topic}
                  </h3>
                  
                  <p className="text-sm text-gray-600 mb-3">
                    {truncateText(blog.content.replace(/#{1,6}\s/g, '').replace(/\n/g, ' '), 150)}
                  </p>

                  <div className="flex flex-wrap items-center gap-3 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {formatDate(blog.created_at)}
                    </span>
                    <span className="flex items-center gap-1">
                      <FileText className="w-3 h-3" />
                      {blog.word_count} words
                    </span>
                    <span className="px-2 py-1 bg-gray-100 rounded-full capitalize">
                      {blog.tone}
                    </span>
                    <span className="px-2 py-1 bg-gray-100 rounded-full capitalize">
                      {blog.length}
                    </span>
                    {blog.seo_score && (
                      <span className={`px-2 py-1 rounded-full font-medium ${getSEOScoreColor(blog.seo_score)}`}>
                        SEO: {blog.seo_score}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleView(blog)}
                    className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                    title="View"
                  >
                    <Eye className="w-5 h-5" />
                  </button>
                  <button
                    onClick={(e) => handleDelete(blog.id, e)}
                    disabled={deleting === blog.id}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Delete"
                  >
                    {deleting === blog.id ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <Trash2 className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BlogHistory;