/**
 * DiscountCard component - displays a single discount item
 */
import React from 'react';
import './DiscountCard.css';

const DiscountCard = ({ discount }) => {
  const formatPrice = (price) => {
    return price ? `€${price.toFixed(2)}` : 'N/A';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('nl-NL');
  };

  return (
    <div className="discount-card">
      <div className="discount-card-header">
        <span className="supermarket-badge">{discount.supermarket}</span>
        <span className="discount-badge">{discount.discount_percentage}% OFF</span>
      </div>
      
      <div className="discount-card-body">
        <h3 className="product-name">{discount.product_name}</h3>
        
        {discount.category && (
          <p className="category">{discount.category}</p>
        )}
        
        <div className="price-section">
          {discount.original_price && (
            <span className="original-price">{formatPrice(discount.original_price)}</span>
          )}
          <span className="discount-price">{formatPrice(discount.discount_price)}</span>
        </div>
        
        {discount.description && (
          <p className="description">{discount.description}</p>
        )}
        
        <div className="validity">
          <small>
            Geldig tot: {formatDate(discount.valid_until)}
          </small>
        </div>
      </div>
    </div>
  );
};

export default DiscountCard;
