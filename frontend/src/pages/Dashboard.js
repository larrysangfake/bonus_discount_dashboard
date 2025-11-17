/**
 * Dashboard page - main view for displaying discounts
 */
import React, { useState, useEffect } from 'react';
import { getDiscounts, getSupermarkets, getCategories, getStats } from '../services/api';
import DiscountCard from '../components/DiscountCard';
import FilterBar from '../components/FilterBar';
import './Dashboard.css';

const Dashboard = () => {
  const [discounts, setDiscounts] = useState([]);
  const [supermarkets, setSupermarkets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [stats, setStats] = useState(null);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadDiscounts();
  }, [filters]);

  const loadInitialData = async () => {
    try {
      const [supermarketsData, categoriesData, statsData] = await Promise.all([
        getSupermarkets(),
        getCategories(),
        getStats()
      ]);
      
      setSupermarkets(supermarketsData);
      setCategories(categoriesData);
      setStats(statsData);
    } catch (err) {
      setError('Failed to load initial data');
      console.error(err);
    }
  };

  const loadDiscounts = async () => {
    setLoading(true);
    try {
      const data = await getDiscounts(filters);
      setDiscounts(data.discounts);
      setError(null);
    } catch (err) {
      setError('Failed to load discounts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    if (key === 'reset') {
      setFilters({});
    } else {
      setFilters(prev => ({
        ...prev,
        [key]: value || undefined
      }));
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🛒 Korting Dashboard</h1>
        <p>Alle kortingen van Nederlandse supermarkten op één plek</p>
      </header>

      {stats && (
        <div className="stats-bar">
          <div className="stat-item">
            <h3>{stats.total_discounts}</h3>
            <p>Actieve Kortingen</p>
          </div>
          <div className="stat-item">
            <h3>{stats.average_discount_percentage}%</h3>
            <p>Gemiddelde Korting</p>
          </div>
          <div className="stat-item">
            <h3>{Object.keys(stats.supermarket_counts || {}).length}</h3>
            <p>Supermarkten</p>
          </div>
        </div>
      )}

      <FilterBar
        filters={filters}
        onFilterChange={handleFilterChange}
        supermarkets={supermarkets}
        categories={categories}
      />

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading ? (
        <div className="loading">
          <p>Laden...</p>
        </div>
      ) : (
        <>
          {discounts.length === 0 ? (
            <div className="no-results">
              <p>Geen kortingen gevonden met de huidige filters.</p>
            </div>
          ) : (
            <>
              <div className="results-info">
                <p>{discounts.length} kortingen gevonden</p>
              </div>
              <div className="discounts-grid">
                {discounts.map((discount) => (
                  <DiscountCard key={discount.id} discount={discount} />
                ))}
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default Dashboard;
