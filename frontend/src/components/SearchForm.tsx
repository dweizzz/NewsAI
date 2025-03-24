// Create a new file called SearchForm.tsx
import React, { useState, useRef, memo } from 'react';

interface SearchFormProps {
  onSearch: (searchTerm: string) => void;
}

// This component will maintain its own state and not re-render when parent re-renders
const SearchForm: React.FC<SearchFormProps> = memo(({ onSearch }) => {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    
    onSearch(inputValue);
    setInputValue('');
    
    // Focus back on input after submission
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="sidebar-search-form"
    >
      <input
        ref={inputRef}
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Search for insights..."
        className="sidebar-search-input"
      />
      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
});

export default SearchForm;

// In your main App.tsx, replace the form with:
// <SearchForm onSearch={(term) => {
//   // Create a new tab here with the term
//   const newTabId = generateTabId();
//   // Rest of your search handling logic...
// }} />