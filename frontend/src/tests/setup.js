import { expect, afterEach, vi, beforeEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Mock clipboard API globally
const mockWriteText = vi.fn(() => Promise.resolve());

Object.defineProperty(navigator, 'clipboard', {
 value: {
  writeText: mockWriteText,
 },
 writable: true,
 configurable: true,
});

// Reset mocks before each test
beforeEach(() => {
 mockWriteText.mockClear();
});

// Cleanup after each test
afterEach(() => {
 cleanup();
});

// Mock environment variables
process.env.VITE_API_URL = 'http://localhost:8000';