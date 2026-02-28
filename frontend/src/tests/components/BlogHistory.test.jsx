import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BlogHistory from '../../components/BlogHistory';
import { mockBlogList } from '../test-utils';
import * as api from '../../services/api';

vi.mock('../../services/api');

describe('BlogHistory', () => {
 beforeEach(() => {
  vi.clearAllMocks();
 });

 it('displays loading state initially', () => {
  api.blogAPI.getAllBlogs = vi.fn(() => new Promise(() => { }));
  render(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={0} />);

  expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
 });

 it('displays blogs when data is loaded', async () => {
  api.blogAPI.getAllBlogs = vi.fn(() => Promise.resolve(mockBlogList));
  render(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={0} />);

  await waitFor(() => {
   expect(screen.getByText('Test Blog Title')).toBeInTheDocument();
   expect(screen.getByText('Second Blog')).toBeInTheDocument();
   expect(screen.getByText('Third Blog')).toBeInTheDocument();
  });
 });

 it('displays empty state when no blogs exist', async () => {
  api.blogAPI.getAllBlogs = vi.fn(() => Promise.resolve({ total: 0, blogs: [] }));
  render(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={0} />);

  await waitFor(() => {
   expect(screen.getByText(/no blogs yet/i)).toBeInTheDocument();
  });
 });

 it('calls onSelectBlog when blog is clicked', async () => {
  const user = userEvent.setup();
  const mockOnSelect = vi.fn();
  api.blogAPI.getAllBlogs = vi.fn(() => Promise.resolve(mockBlogList));

  render(<BlogHistory onSelectBlog={mockOnSelect} refreshTrigger={0} />);

  await waitFor(() => {
   expect(screen.getByText('Test Blog Title')).toBeInTheDocument();
  });

  const blogCard = screen.getByText('Test Blog Title').closest('div');
  await user.click(blogCard);

  expect(mockOnSelect).toHaveBeenCalledWith(mockBlogList.blogs[0]);
 });

 it('deletes blog when delete button is clicked', async () => {
  const user = userEvent.setup();
  window.confirm = vi.fn(() => true);
  api.blogAPI.getAllBlogs = vi.fn(() => Promise.resolve(mockBlogList));
  api.blogAPI.deleteBlog = vi.fn(() => Promise.resolve({ message: 'Deleted' }));

  render(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={0} />);

  await waitFor(() => {
   expect(screen.getByText('Test Blog Title')).toBeInTheDocument();
  });

  const deleteButtons = screen.getAllByTitle('Delete');
  await user.click(deleteButtons[0]);

  expect(window.confirm).toHaveBeenCalled();
  expect(api.blogAPI.deleteBlog).toHaveBeenCalledWith(1);
 });

 it('refreshes blogs when refreshTrigger changes', async () => {
  api.blogAPI.getAllBlogs = vi.fn(() => Promise.resolve(mockBlogList));

  const { rerender } = render(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={0} />);

  await waitFor(() => {
   expect(api.blogAPI.getAllBlogs).toHaveBeenCalledTimes(1);
  });

  rerender(<BlogHistory onSelectBlog={vi.fn()} refreshTrigger={1} />);

  await waitFor(() => {
   expect(api.blogAPI.getAllBlogs).toHaveBeenCalledTimes(2);
  });
 });
});