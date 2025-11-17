#!/usr/bin/env python3
"""
API Integration Test Script

Tests all API endpoints to ensure they're working correctly.
"""

import requests
import sys
import json

API_BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint."""
    print("Testing /api/health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_discounts():
    """Test discounts endpoint."""
    print("\nTesting /api/discounts...")
    try:
        response = requests.get(f"{API_BASE_URL}/discounts")
        assert response.status_code == 200
        data = response.json()
        assert "discounts" in data
        assert "total" in data
        assert isinstance(data["discounts"], list)
        print(f"✅ Discounts endpoint passed ({data['total']} discounts found)")
        return True
    except Exception as e:
        print(f"❌ Discounts endpoint failed: {e}")
        return False

def test_discounts_with_filters():
    """Test discounts endpoint with filters."""
    print("\nTesting /api/discounts with filters...")
    try:
        # Test supermarket filter
        response = requests.get(f"{API_BASE_URL}/discounts?supermarket=Jumbo")
        assert response.status_code == 200
        data = response.json()
        for discount in data["discounts"]:
            assert discount["supermarket"] == "Jumbo"
        print(f"  ✅ Supermarket filter passed")
        
        # Test min_discount filter
        response = requests.get(f"{API_BASE_URL}/discounts?min_discount=30")
        assert response.status_code == 200
        data = response.json()
        for discount in data["discounts"]:
            assert discount["discount_percentage"] >= 30
        print(f"  ✅ Min discount filter passed")
        
        return True
    except Exception as e:
        print(f"❌ Filters test failed: {e}")
        return False

def test_supermarkets():
    """Test supermarkets endpoint."""
    print("\nTesting /api/supermarkets...")
    try:
        response = requests.get(f"{API_BASE_URL}/supermarkets")
        assert response.status_code == 200
        data = response.json()
        assert "supermarkets" in data
        assert isinstance(data["supermarkets"], list)
        assert len(data["supermarkets"]) > 0
        print(f"✅ Supermarkets endpoint passed ({len(data['supermarkets'])} supermarkets)")
        return True
    except Exception as e:
        print(f"❌ Supermarkets endpoint failed: {e}")
        return False

def test_categories():
    """Test categories endpoint."""
    print("\nTesting /api/categories...")
    try:
        response = requests.get(f"{API_BASE_URL}/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) > 0
        print(f"✅ Categories endpoint passed ({len(data['categories'])} categories)")
        return True
    except Exception as e:
        print(f"❌ Categories endpoint failed: {e}")
        return False

def test_stats():
    """Test stats endpoint."""
    print("\nTesting /api/stats...")
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_discounts" in data
        assert "supermarket_counts" in data
        assert "average_discount_percentage" in data
        print(f"✅ Stats endpoint passed")
        print(f"   Total discounts: {data['total_discounts']}")
        print(f"   Average discount: {data['average_discount_percentage']}%")
        return True
    except Exception as e:
        print(f"❌ Stats endpoint failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("API Integration Tests")
    print("=" * 60)
    
    tests = [
        test_health,
        test_discounts,
        test_discounts_with_filters,
        test_supermarkets,
        test_categories,
        test_stats
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
