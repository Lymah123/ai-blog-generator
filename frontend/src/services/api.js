import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
 baseURL: `${API_BASE_URL}/api/v1`,
 headers: {
   'Content-Type': 'application/json',
 },
 timeout: 120000,
});

// API Methods
export const blogAPI = {
 // Generate new blog
 generateBlog: async (data) => {
   const response = await api.post('/generate', data);
   return response.data;
 },

 // Get all blogs
 getAllBlogs: async (skip = 0, limit = 20) => {
   const response = await api.get(`/blogs?skip=${skip}&limit=${limit}`);
   return response.data;
 },

 // Get single blog
 getBlog: async (id) => {
   const response = await api.get(`/blogs/${id}`);
   return response.data;
 },

 // Delete blog
 deleteBlog: async (id) => {
   const response = await api.delete(`/blogs/${id}`);
   return response.data;
 },
};

// Health Check
export const checkHealth = async () => {
 try {
   const response = await axios.get(`${API_BASE_URL}/health`);
   return response.data;
 } catch (error) {
   throw error;
 }
};

export default api;