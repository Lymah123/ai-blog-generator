import { describe, it, expect } from 'vitest';
import {
  formatDate,
  getSEOScoreColor,
  truncateText,
} from '../../utils/helpers';

describe('Helper Functions', () => {
  describe('formatDate', () => {
    it('formats date correctly', () => {
      const date = '2026-01-06T12:00:00Z';
      const formatted = formatDate(date);
      
      expect(formatted).toContain('2026');
      expect(formatted).toContain('January');
    });
  });

  describe('getSEOScoreColor', () => {
    it('returns green for high scores', () => {
      expect(getSEOScoreColor(85)).toContain('green');
    });

    it('returns yellow for medium scores', () => {
      expect(getSEOScoreColor(65)).toContain('yellow');
    });

    it('returns red for low scores', () => {
      expect(getSEOScoreColor(45)).toContain('red');
    });
  });

  describe('truncateText', () => {
    it('truncates long text', () => {
      const longText = 'A'.repeat(200);
      const truncated = truncateText(longText, 100);
      
      expect(truncated.length).toBeLessThanOrEqual(103);
      expect(truncated).toContain('...');
    });

    it('does not truncate short text', () => {
      const shortText = 'Short text';
      const result = truncateText(shortText, 100);
      
      expect(result).toBe(shortText);
    });
  });
});