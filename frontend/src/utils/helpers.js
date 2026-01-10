// Format date
export const formatDate = (dateString) => {
 const options = {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
 };
 return new Date(dateString).toLocaleDateString('en-US', options);
};

// Copy to clipboard
export const copyToClipboard = async (text) => {
 try {
  await navigator.clipboard.writeText(text);
  return true;
 } catch (err) {
  console.error('Failed to copy: ', err);
  return false;
 }
};

// Download as file
export const downloadAsFile = (content, filename, type = 'text/markdown') => {
 const blob = new Blob([content], { type });
 const url = URL.createObjectURL(blob);
 const link = document.createElement('a');
 link.href = url;
 link.download = filename;
 document.body.appendChild(link);
 link.click();
 document.body.removeChild(link);
 URL.revokeObjectURL(url);
};

// Get SEO score color
export const getSEOScoreColor = (score) => {
 if (score >= 80) return 'text-green-600 bg-green-100';
 if (score >= 60) return 'text-yellow-600 bg-yellow-100';
 return 'text-red-600 bg-red-100';
};

// Truncate text
export const truncateText = (text, maxLength = 150) => {
 if (text.length <= maxLength) return text;
 return text.substring(0, maxLength) + '...';
};