/**
 * FilterBar component - provides filtering controls
 */
import React from 'react';
import './FilterBar.css';

const FilterBar = ({ 
  filters, 
  onFilterChange, 
  supermarkets, 
  categories 
}) => {
  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label htmlFor="search">Zoeken:</label>
        <input
          type="text"
          id="search"
          placeholder="Zoek product..."
          value={filters.search || ''}
          onChange={(e) => onFilterChange('search', e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="supermarket">Supermarkt:</label>
        <select
          id="supermarket"
          value={filters.supermarket || ''}
          onChange={(e) => onFilterChange('supermarket', e.target.value)}
        >
          <option value="">Alle</option>
          {supermarkets.map((sm) => (
            <option key={sm} value={sm}>
              {sm}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="category">Categorie:</label>
        <select
          id="category"
          value={filters.category || ''}
          onChange={(e) => onFilterChange('category', e.target.value)}
        >
          <option value="">Alle</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="min_discount">Min. korting %:</label>
        <input
          type="number"
          id="min_discount"
          min="0"
          max="100"
          placeholder="0"
          value={filters.min_discount || ''}
          onChange={(e) => onFilterChange('min_discount', e.target.value)}
        />
      </div>

      <button 
        className="reset-button"
        onClick={() => onFilterChange('reset', null)}
      >
        Reset Filters
      </button>
    </div>
  );
};

export default FilterBar;
