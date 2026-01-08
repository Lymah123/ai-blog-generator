import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Download, CheckCircle, FileText, BarChart3, Hash } from 'lucide-react';
import { copyToClipboard, downloadAsFile, getSEOScoreColor, formatDate } from '../utils/helpers';

const BlogDisplay = ({ blog }) => {
  const [copied, setCopied] = useState(false);

  if (!blog) {
    return (
      <div className="card text-center py-12">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Content Yet</h3>
        <p className="text-gray-600">
          Fill out the form and generate your first AI-powered blog post
        </p>
      </div>
    );
  }

  const handleCopy = async () => {
    const fullContent = `# ${blog.title}\n\n${blog.content}`;
    const success = await copyToClipboard(fullContent);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const fullContent = `# ${blog.title}\n\n${blog.content}`;
    const filename = `${blog.title.replace(/[^a-z0-9]/gi, '-').toLowerCase()}.md`;
    downloadAsFile(fullContent, filename);
  };

  return (
    <div className="space-y-6">
      {/* Header with Actions */}
      <div className="card">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{blog.title}</h2>
            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
              <span className="flex items-center gap-1">
                <FileText className="w-4 h-4" />
                {blog.word_count} words
              </span>
              {blog.seo_score && (
                <span className={`flex items-center gap-1 px-2 py-1 rounded-full ${getSEOScoreColor(blog.seo_score)}`}>
                  <BarChart3 className="w-4 h-4" />
                  SEO Score: {blog.seo_score}
                </span>
              )}
              {blog.keywords && (
                <span className="flex items-center gap-1">
                  <Hash className="w-4 h-4" />
                  {blog.keywords.split(',').length} keywords
                </span>
              )}
            </div>
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleCopy}
              className="btn-secondary flex items-center gap-2"
            >
              {copied ? (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copy
                </>
              )}
            </button>
            <button
              onClick={handleDownload}
              className="btn-primary flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Download
            </button>
          </div>
        </div>

        {/* Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
          <div>
            <div className="text-xs text-gray-600 mb-1">Topic</div>
            <div className="font-medium text-gray-900">{blog.topic}</div>
          </div>
          <div>
            <div className="text-xs text-gray-600 mb-1">Tone</div>
            <div className="font-medium text-gray-900 capitalize">{blog.tone}</div>
          </div>
          <div>
            <div className="text-xs text-gray-600 mb-1">Length</div>
            <div className="font-medium text-gray-900 capitalize">{blog.length}</div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="card">
        <div className="prose prose-lg max-w-none">
          <ReactMarkdown>{blog.content}</ReactMarkdown>
        </div>
      </div>

      {/* Keywords Section */}
      {blog.keywords && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {blog.keywords.split(',').map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
              >
                {keyword.trim()}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="card">
        <div className="text-sm text-gray-600">
          Generated on {formatDate(blog.created_at)}
        </div>
      </div>
    </div>
  );
};

export default BlogDisplay;