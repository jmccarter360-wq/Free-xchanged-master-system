# Quick Start Guide

Get the Free-xchanged-master-system up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/jmccarter360-wq/Free-xchanged-master-system.git
cd Free-xchanged-master-system
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env with your settings if needed
```

5. **Initialize database:**
```bash
# Create empty database
python init_db.py init

# Or create with sample data
python init_db.py seed
```

6. **Start the server:**
```bash
python main.py
```

The API will be running at `http://localhost:8000`

## Try It Out!

1. **Open API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Create your first customer:**
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

3. **Process a transaction (gets 5% cashback automatically):**
```bash
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "amount": 100.00}'
```

4. **Check cashback balance:**
```bash
curl "http://localhost:8000/customers/1/balance"
```

## Running Tests

```bash
pytest tests/ -v
```

## What's Next?

- Check out the [README.md](README.md) for detailed documentation
- Explore the API endpoints at http://localhost:8000/docs
- Configure Stripe integration for real payments
- Deploy to production with proper environment variables

## Need Help?

- Read the full [README.md](README.md)
- Check the API documentation
- Open an issue on GitHub

Happy coding! 🚀
