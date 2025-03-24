import React, { useState } from 'react';

interface SearchInputProps {
  onSearch: (term: string) => void;
}

const SearchInput: React.FC<SearchInputProps> = ({ onSearch }) => {
  const [localInputValue, setLocalInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (localInputValue.trim()) {
      onSearch(localInputValue);
      setLocalInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="sidebar-search-form">
      <input
        type="text"
        value={localInputValue}
        onChange={(e) => setLocalInputValue(e.target.value)}
        placeholder="Search for insights..."
        className="sidebar-search-input"
      />
    </form>
  );
};

export default SearchInput; 