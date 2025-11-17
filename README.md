# Bonus Discount Dashboard

A full-stack data engineering and analytics project that aggregates supermarket discount ("korting") data across the Netherlands and displays it in a modern, filterable web dashboard.

## 🎯 Features

- **Multi-Supermarket Support**: Aggregates discount data from:
  - Albert Heijn
  - Jumbo
  - Lidl
  - Dirk van den Broek

- **Backend API**: RESTful API built with Flask
  - Filter by supermarket, category, discount percentage
  - Search functionality
  - Statistics and analytics endpoints

- **Frontend Dashboard**: Modern React-based UI
  - Responsive design
  - Real-time filtering
  - Clean, intuitive interface
  - Mobile-friendly

- **Data Storage**: SQLite database for easy setup and portability

## 🏗️ Project Structure

```
bonus_discount_dashboard/
├── backend/
│   ├── api/              # Flask API application
│   ├── models/           # Database models and ORM
│   ├── scrapers/         # Web scrapers for each supermarket
│   ├── utils/            # Utility functions and data collection
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── public/           # Static files
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API service layer
│   └── package.json      # Node.js dependencies
├── data/
│   ├── raw/              # Raw scraped data
│   └── processed/        # Processed data
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database and collect sample data:
   ```bash
   python utils/data_collector.py
   ```

5. Start the API server:
   ```bash
   python api/app.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The dashboard will open at `http://localhost:3000`

## 📡 API Endpoints

### GET /api/health
Health check endpoint

### GET /api/discounts
Get all active discounts with optional filters

**Query Parameters:**
- `supermarket` - Filter by supermarket name
- `category` - Filter by category
- `min_discount` - Minimum discount percentage
- `search` - Search in product name
- `limit` - Maximum number of results (default: 100)
- `offset` - Pagination offset (default: 0)

**Example:**
```bash
curl "http://localhost:5000/api/discounts?supermarket=Jumbo&min_discount=20"
```

### GET /api/discounts/:id
Get a specific discount by ID

### GET /api/supermarkets
Get list of all supermarkets with active discounts

### GET /api/categories
Get list of all categories with active discounts

### GET /api/stats
Get statistics about discounts

## 🔧 Configuration

### Backend Configuration

The backend uses SQLite by default. The database file is created at `data/discounts.db`.

To use PostgreSQL or MySQL, modify `backend/models/database.py`:

```python
# For PostgreSQL
engine = create_engine('postgresql://user:password@localhost/dbname')

# For MySQL
engine = create_engine('mysql+pymysql://user:password@localhost/dbname')
```

### Frontend Configuration

Create a `.env` file in the frontend directory to configure the API URL:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## 📊 Data Collection

The data collection system uses web scrapers to gather discount information from supermarket websites.

**Note**: The current implementation includes placeholder scrapers with sample data. To implement actual scraping:

1. Analyze each supermarket's website structure
2. Identify API endpoints or HTML elements containing discount data
3. Update the respective scraper classes in `backend/scrapers/`
4. Consider using Selenium for JavaScript-heavy sites
5. Respect robots.txt and implement rate limiting

### Running Data Collection

```bash
cd backend
python utils/data_collector.py
```

This will:
- Run all configured scrapers
- Store discount data in the database
- Mark expired discounts as inactive

## 🛠️ Development

### Adding a New Supermarket Scraper

1. Create a new scraper class in `backend/scrapers/`:

```python
from .base_scraper import BaseScraper

class NewSupermarketScraper(BaseScraper):
    def __init__(self):
        super().__init__("New Supermarket")
        self.base_url = "https://www.newsupermarket.nl"
    
    def scrape(self):
        # Implement scraping logic
        pass
```

2. Register it in `backend/scrapers/__init__.py`:

```python
from .new_scraper import NewSupermarketScraper

SCRAPERS = {
    # ... existing scrapers
    'new_supermarket': NewSupermarketScraper
}
```

### Testing the API

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Get all discounts
curl http://localhost:5000/api/discounts

# Get discounts with filters
curl "http://localhost:5000/api/discounts?supermarket=Albert%20Heijn&min_discount=25"

# Get statistics
curl http://localhost:5000/api/stats
```

## 🐳 Docker Support (Future Enhancement)

A `docker-compose.yml` file can be added for easy deployment:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

## 📝 TODO / Future Enhancements

- [ ] Implement real web scrapers for each supermarket
- [ ] Add user authentication and saved preferences
- [ ] Implement email notifications for specific discounts
- [ ] Add price history tracking and trends
- [ ] Create mobile app (React Native)
- [ ] Add more supermarkets (Plus, Coop, etc.)
- [ ] Implement caching layer (Redis)
- [ ] Add unit and integration tests
- [ ] Set up CI/CD pipeline
- [ ] Deploy to cloud platform (Heroku, AWS, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This project is for educational purposes. When implementing actual web scraping:
- Always respect the website's `robots.txt` file
- Implement rate limiting to avoid overloading servers
- Consider using official APIs when available
- Be aware of legal implications of web scraping in your jurisdiction
- Check and comply with each supermarket's Terms of Service

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
