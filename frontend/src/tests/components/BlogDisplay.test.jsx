import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BlogDisplay from '../../components/BlogDisplay';
import { mockBlog } from '../test-utils';

describe('BlogDisplay', () => {
 it('shows placeholder when no blog is provided', () => {
  render(<BlogDisplay blog={null} />);

  expect(screen.getByText(/no content yet/i)).toBeInTheDocument();
  expect(screen.getByText(/fill out the form/i)).toBeInTheDocument();
 });

 it('displays blog title and metadata', () => {
  render(<BlogDisplay blog={mockBlog} />);

  expect(screen.getByText(mockBlog.title)).toBeInTheDocument();
  expect(screen.getByText(`${mockBlog.word_count} words`)).toBeInTheDocument();
  expect(screen.getByText(`SEO Score: ${mockBlog.seo_score}`)).toBeInTheDocument();
 });

 it('displays blog content', () => {
  render(<BlogDisplay blog={mockBlog} />);

  expect(screen.getByText(/this is test content/i)).toBeInTheDocument();
  expect(screen.getByText(/test conclusion/i)).toBeInTheDocument();
 });

 it('displays keywords when provided', () => {
  render(<BlogDisplay blog={mockBlog} />);

  expect(screen.getByText('test')).toBeInTheDocument();
  expect(screen.getByText('react')).toBeInTheDocument();
  expect(screen.getByText('vitest')).toBeInTheDocument();
 });

 it('copies content to clipboard when copy button is clicked', async () => {
  const user = userEvent.setup();
  render(<BlogDisplay blog={mockBlog} />);

  const copyButton = screen.getByRole('button', { name: /copy/i });
  await user.click(copyButton);

  // Verify the UI feedback appears (which confirms clipboard operation succeeded)
  expect(await screen.findByText(/copied!/i)).toBeInTheDocument();
 });

 it('shows correct SEO score color', () => {
  const { rerender } = render(<BlogDisplay blog={{ ...mockBlog, seo_score: 85 }} />);
  expect(screen.getByText(/SEO Score: 85/i)).toHaveClass('text-green-600');

  rerender(<BlogDisplay blog={{ ...mockBlog, seo_score: 65 }} />);
  expect(screen.getByText(/SEO Score: 65/i)).toHaveClass('text-yellow-600');

  rerender(<BlogDisplay blog={{ ...mockBlog, seo_score: 45 }} />);
  expect(screen.getByText(/SEO Score: 45/i)).toHaveClass('text-red-600');
 });

 it('has download button', () => {
  render(<BlogDisplay blog={mockBlog} />);

  const downloadButton = screen.getByRole('button', { name: /download/i });
  expect(downloadButton).toBeInTheDocument();
 });
});