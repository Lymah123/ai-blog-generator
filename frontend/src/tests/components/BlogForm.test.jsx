import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BlogForm from '../../components/BlogForm';

describe('BlogForm', () => {
 it('renders all form elements', () => {
  render(<BlogForm onGenerate={vi.fn()} isGenerating={false} />);

  expect(screen.getByLabelText(/blog topic/i)).toBeInTheDocument();
  expect(screen.getByText(/writing tone/i)).toBeInTheDocument();
  expect(screen.getByText(/content length/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/keywords/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /generate blog post/i })).toBeInTheDocument();
 });

 it('shows validation error for empty topic', async () => {
  const user = userEvent.setup();
  render(<BlogForm onGenerate={vi.fn()} isGenerating={false} />);

  const submitButton = screen.getByRole('button', { name: /generate blog post/i });
  await user.click(submitButton);

  expect(screen.getByText(/topic is required/i)).toBeInTheDocument();
 });

 it('shows validation error for short topic', async () => {
  const user = userEvent.setup();
  render(<BlogForm onGenerate={vi.fn()} isGenerating={false} />);

  const topicInput = screen.getByLabelText(/blog topic/i);
  await user.type(topicInput, 'AI');

  const submitButton = screen.getByRole('button', { name: /generate blog post/i });
  await user.click(submitButton);

  expect(screen.getByText(/topic must be at least 5 characters/i)).toBeInTheDocument();
 });

 it('calls onGenerate with correct data on valid submission', async () => {
  const user = userEvent.setup();
  const mockOnGenerate = vi.fn();
  render(<BlogForm onGenerate={mockOnGenerate} isGenerating={false} />);

  const topicInput = screen.getByLabelText(/blog topic/i);
  await user.type(topicInput, 'The Future of AI');

  const keywordsInput = screen.getByLabelText(/keywords/i);
  await user.type(keywordsInput, 'AI, technology');

  const submitButton = screen.getByRole('button', { name: /generate blog post/i });
  await user.click(submitButton);

  await waitFor(() => {
   expect(mockOnGenerate).toHaveBeenCalledWith({
    topic: 'The Future of AI',
    tone: 'professional',
    length: 'medium',
    keywords: 'AI, technology',
   });
  });
 });

 it('disables form during generation', () => {
  render(<BlogForm onGenerate={vi.fn()} isGenerating={true} />);

  const topicInput = screen.getByLabelText(/blog topic/i);
  const submitButton = screen.getByRole('button', { name: /generating content/i });

  expect(topicInput).toBeDisabled();
  expect(submitButton).toBeDisabled();
  expect(screen.getByText(/generating content/i)).toBeInTheDocument();
 });

 it('allows tone selection', async () => {
  const user = userEvent.setup();
  const mockOnGenerate = vi.fn();
  render(<BlogForm onGenerate={mockOnGenerate} isGenerating={false} />);

  const casualButton = screen.getByText('Casual');
  await user.click(casualButton);

  const topicInput = screen.getByLabelText(/blog topic/i);
  await user.type(topicInput, 'Test Topic');

  const submitButton = screen.getByRole('button', { name: /generate blog post/i });
  await user.click(submitButton);

  await waitFor(() => {
   expect(mockOnGenerate).toHaveBeenCalledWith(
    expect.objectContaining({ tone: 'casual' })
   );
  });
 });

 it('allows length selection', async () => {
  const user = userEvent.setup();
  const mockOnGenerate = vi.fn();
  render(<BlogForm onGenerate={mockOnGenerate} isGenerating={false} />);

  const longButton = screen.getByText('Long');
  await user.click(longButton);

  const topicInput = screen.getByLabelText(/blog topic/i);
  await user.type(topicInput, 'Test Topic');

  const submitButton = screen.getByRole('button', { name: /generate blog post/i });
  await user.click(submitButton);

  await waitFor(() => {
   expect(mockOnGenerate).toHaveBeenCalledWith(
    expect.objectContaining({ length: 'long' })
   );
  });
 });
});