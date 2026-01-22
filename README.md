# Free-xchanged Master System

A comprehensive cashback and rewards management system built with FastAPI, SQLAlchemy, and Stripe integration.

## Features

- **Ambassador Management**: Create and manage brand ambassadors and groups
- **Customer Management**: Handle customer accounts and profiles
- **QR Code System**: Generate and track QR codes for ambassadors
- **Transaction Processing**: Process customer transactions with automatic cashback
- **Cashback System**: Track and manage customer cashback balances
- **Cashback Transfers**: Transfer cashback between customers
- **Payout Processing**: Process cashback payouts to customers
- **Gift Card System**: Create and redeem gift cards
- **Stripe Integration**: ACH payment processing via Stripe

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Stripe**: Payment processing integration
- **Uvicorn**: ASGI server implementation

## Project Structure

```
.
├── main.py                 # FastAPI application and endpoints
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic schemas for request/response validation
├── services.py            # Business logic services
├── database.py            # Database configuration and connection
├── config.py              # Application configuration
├── logging_config.py      # Logging setup
├── requirements.txt       # Python dependencies
├── integrations/
│   └── stripe.py         # Stripe ACH integration
└── utils/
    ├── error_handlers.py # Custom error handling
    ├── retry_logic.py    # Retry decorator with exponential backoff
    └── validators.py     # Input validation utilities
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jmccarter360-wq/Free-xchanged-master-system.git
cd Free-xchanged-master-system
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

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual configuration values
```

5. Initialize the database:
```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

## Running the Application

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /` - Check API status

### Ambassadors
- `POST /ambassadors/` - Create a new ambassador
- `GET /ambassadors/` - List all ambassadors
- `GET /ambassadors/{ambassador_id}` - Get specific ambassador

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - List all customers
- `GET /customers/{customer_id}` - Get specific customer
- `GET /customers/{customer_id}/balance` - Get customer's cashback balance

### Groups
- `POST /groups/` - Create a new group
- `GET /groups/` - List all groups

### QR Codes
- `POST /qrcodes/` - Create a new QR code
- `GET /qrcodes/{code}` - Get QR code details

### Transactions
- `POST /transactions/` - Create transaction (applies automatic cashback)
- `GET /transactions/` - List all transactions
- `GET /transactions/customer/{customer_id}` - Get customer's transactions

### Cashback Transfers
- `POST /cashback-transfers/` - Transfer cashback between customers
- `GET /cashback-transfers/` - List all cashback transfers

### Payouts
- `POST /payouts/` - Process a cashback payout
- `GET /payouts/` - List all payouts
- `GET /payouts/customer/{customer_id}` - Get customer's payouts

### Gift Cards
- `POST /gift-cards/` - Create a new gift card
- `GET /gift-cards/{code}` - Get gift card details
- `DELETE /gift-cards/{code}` - Redeem a gift card

## Usage Examples

### Creating a Customer
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

### Processing a Transaction
```bash
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 100.00
  }'
```

This will create a transaction for $100 and automatically add $5 (5% cashback) to the customer's cashback balance.

### Checking Cashback Balance
```bash
curl "http://localhost:8000/customers/1/balance"
```

### Transferring Cashback
```bash
curl -X POST "http://localhost:8000/cashback-transfers/" \
  -H "Content-Type: application/json" \
  -d '{
    "from_customer_id": 1,
    "to_customer_id": 2,
    "amount": 10.00
  }'
```

### Processing a Payout
```bash
curl -X POST "http://localhost:8000/payouts/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 50.00
  }'
```

## Configuration

### Database Configuration

The default configuration uses SQLite. To use PostgreSQL or another database:

1. Update `database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"
```

2. Install the appropriate database driver:
```bash
pip install psycopg2-binary  # For PostgreSQL
```

### Cashback Rate

The default cashback rate is 5%. To modify it, edit the `CashbackService` class in `services.py`:

```python
self.cashback_percentage = 0.05  # Change to desired percentage
```

### Stripe Configuration

Update your Stripe API key in `integrations/stripe.py` or use environment variables:

```python
stripe.api_key = os.environ.get('STRIPE_API_KEY')
```

## Testing

Run tests using pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=html
```

## Error Handling

The application includes comprehensive error handling:

- **NotFoundError (404)**: Resource not found
- **ValidationError (400)**: Invalid input data
- **HTTPException**: Various HTTP errors with descriptive messages

## Retry Logic

Critical operations (like payouts) include automatic retry with exponential backoff:

- Maximum 3 attempts
- Initial delay: 1 second
- Backoff multiplier: 2

## Logging

Structured JSON logging is configured by default. Logs include:
- Timestamp
- Log level
- Message

## Security Considerations

- Always use HTTPS in production
- Keep your `.env` file secure and never commit it
- Use strong SECRET_KEY values
- Implement rate limiting for production use
- Add authentication/authorization as needed
- Validate all input data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.
