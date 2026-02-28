import { render } from '@testing-library/react';

// Custom render function with providers if needed
export function renderWithProviders(ui, options = {}) {
  return render(ui, { ...options });
}

// Mock blog data
export const mockBlog = {
  id: 1,
  topic: 'Test Blog Topic',
  tone: 'professional',
  length: 'medium',
  keywords: 'test, react, vitest',
  title: 'Test Blog Title',
  content: '## Introduction\n\nThis is test content.\n\n## Conclusion\n\nTest conclusion.',
  seo_score: 85,
  word_count: 120,
  created_at: '2026-01-06T12:00:00Z',
};

export const mockBlogList = {
  total: 3,
  blogs: [
    mockBlog,
    { ...mockBlog, id: 2, title: 'Second Blog' },
    { ...mockBlog, id: 3, title: 'Third Blog' },
  ],
};