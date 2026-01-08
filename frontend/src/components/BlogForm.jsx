import React, { useState } from 'react';
import { FileText, Sparkles, Loader2 } from 'lucide-react';

const BlogForm = ({ onGenerate, isGenerating }) => {
  const [formData, setFormData] = useState({
    topic: '',
    tone: 'professional',
    length: 'medium',
    keywords: '',
  });

  const [errors, setErrors] = useState({});

  const toneOptions = [
    { value: 'professional', label: 'Professional', emoji: '💼' },
    { value: 'casual', label: 'Casual', emoji: '😊' },
    { value: 'technical', label: 'Technical', emoji: '🔧' },
    { value: 'educational', label: 'Educational', emoji: '📚' },
  ];

  const lengthOptions = [
    { value: 'short', label: 'Short', description: '600-800 words' },
    { value: 'medium', label: 'Medium', description: '1000-1500 words' },
    { value: 'long', label: 'Long', description: '1800-2500 words' },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user types
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.topic.trim()) {
      newErrors.topic = 'Topic is required';
    } else if (formData.topic.length < 5) {
      newErrors.topic = 'Topic must be at least 5 characters';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      const submitData = {
        ...formData,
        keywords: formData.keywords.trim() || null,
      };
      onGenerate(submitData);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-primary-100 rounded-lg">
          <FileText className="w-6 h-6 text-primary-600" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Generate Blog Post</h2>
          <p className="text-gray-600 text-sm">Create AI-powered content in seconds</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Topic Input */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            Blog Topic *
          </label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleChange}
            placeholder="e.g., The Future of Artificial Intelligence"
            className={`input-field ${errors.topic ? 'border-red-500' : ''}`}
            disabled={isGenerating}
          />
          {errors.topic && (
            <p className="mt-1 text-sm text-red-600">{errors.topic}</p>
          )}
        </div>

        {/* Tone Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Writing Tone
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {toneOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setFormData((prev) => ({ ...prev, tone: option.value }))}
                disabled={isGenerating}
                className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                  formData.tone === option.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                <div className="text-2xl mb-1">{option.emoji}</div>
                <div className="text-sm font-medium">{option.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Length Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Content Length
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {lengthOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setFormData((prev) => ({ ...prev, length: option.value }))}
                disabled={isGenerating}
                className={`p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                  formData.length === option.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                <div className="font-medium text-gray-900">{option.label}</div>
                <div className="text-sm text-gray-600">{option.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Keywords Input */}
        <div>
          <label htmlFor="keywords" className="block text-sm font-medium text-gray-700 mb-2">
            Keywords (Optional)
          </label>
          <input
            type="text"
            id="keywords"
            name="keywords"
            value={formData.keywords}
            onChange={handleChange}
            placeholder="e.g., AI, machine learning, automation"
            className="input-field"
            disabled={isGenerating}
          />
          <p className="mt-1 text-sm text-gray-500">
            Separate keywords with commas for better SEO optimization
          </p>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isGenerating}
          className="w-full btn-primary flex items-center justify-center gap-2 py-3"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Content...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Generate Blog Post
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default BlogForm;