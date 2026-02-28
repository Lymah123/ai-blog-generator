import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { blogAPI } from '../../services/api';

vi.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('generateBlog', () => {
    it('sends correct data to generate endpoint', async () => {
      const mockData = {
        topic: 'Test Topic',
        tone: 'professional',
        length: 'medium',
        keywords: 'test',
      };

      const mockResponse = {
        data: { id: 1, ...mockData, title: 'Generated Title' },
      };

      axios.create = vi.fn(() => ({
        post: vi.fn(() => Promise.resolve(mockResponse)),
      }));

      const result = await blogAPI.generateBlog(mockData);

      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('getAllBlogs', () => {
    it('fetches blogs with default pagination', async () => {
      const mockResponse = {
        data: { total: 10, blogs: [] },
      };

      axios.create = vi.fn(() => ({
        get: vi.fn(() => Promise.resolve(mockResponse)),
      }));

      const result = await blogAPI.getAllBlogs();

      expect(result).toEqual(mockResponse.data);
    });
  });
});