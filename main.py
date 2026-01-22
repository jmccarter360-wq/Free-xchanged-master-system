from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uvicorn
import os

from database import engine, Base, get_db
from models import (
    Ambassador, Customer, Group, QRCode, CashbackBalance, 
    GiftCard, Transaction, CashbackTransfer, Payout
)
from schemas import (
    AmbassadorCreate, AmbassadorResponse,
    CustomerCreate, CustomerResponse,
    GroupCreate, GroupResponse,
    QRCodeCreate, QRCodeResponse,
    TransactionCreate, TransactionResponse,
    CashbackTransferCreate, CashbackTransferResponse,
    PayoutCreate, PayoutResponse,
    GiftCardCreate, GiftCardResponse,
    CashbackBalanceResponse
)
from services import CashbackService, TransactionService, PayoutService
from logging_config import setup_logging
from utils.error_handlers import NotFoundError, ValidationError

# Initialize logger
logger = setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Free-xchanged Master System",
    description="A cashback and rewards management system",
    version="1.0.0"
)

# Configure CORS - In production, replace with specific domains
# Example: allow_origins=["https://yourdomain.com", "https://app.yourdomain.com"]
cors_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "message": exc.message}
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Validation Error", "message": exc.message}
    )

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Free-xchanged Master System API", "status": "running"}

# Ambassador endpoints
@app.post("/ambassadors/", response_model=AmbassadorResponse, tags=["Ambassadors"])
async def create_ambassador(ambassador: AmbassadorCreate, db: Session = Depends(get_db)):
    """Create a new ambassador"""
    db_ambassador = db.query(Ambassador).filter(Ambassador.email == ambassador.email).first()
    if db_ambassador:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_ambassador = Ambassador(**ambassador.model_dump())
    db.add(new_ambassador)
    db.commit()
    db.refresh(new_ambassador)
    logger.info(f"Created ambassador: {new_ambassador.id}")
    return new_ambassador

@app.get("/ambassadors/", response_model=list[AmbassadorResponse], tags=["Ambassadors"])
async def list_ambassadors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all ambassadors"""
    ambassadors = db.query(Ambassador).offset(skip).limit(limit).all()
    return ambassadors

@app.get("/ambassadors/{ambassador_id}", response_model=AmbassadorResponse, tags=["Ambassadors"])
async def get_ambassador(ambassador_id: int, db: Session = Depends(get_db)):
    """Get a specific ambassador by ID"""
    ambassador = db.query(Ambassador).filter(Ambassador.id == ambassador_id).first()
    if not ambassador:
        raise HTTPException(status_code=404, detail="Ambassador not found")
    return ambassador

# Customer endpoints
@app.post("/customers/", response_model=CustomerResponse, tags=["Customers"])
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    # Create initial cashback balance
    cashback_balance = CashbackBalance(customer_id=new_customer.id, balance=0)
    db.add(cashback_balance)
    db.commit()
    
    logger.info(f"Created customer: {new_customer.id}")
    return new_customer

@app.get("/customers/", response_model=list[CustomerResponse], tags=["Customers"])
async def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all customers"""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@app.get("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/{customer_id}/balance", response_model=CashbackBalanceResponse, tags=["Customers"])
async def get_customer_balance(customer_id: int, db: Session = Depends(get_db)):
    """Get customer's cashback balance"""
    cashback_service = CashbackService(db)
    balance = cashback_service.get_balance(customer_id)
    return {"customer_id": customer_id, "balance": balance}

# Group endpoints
@app.post("/groups/", response_model=GroupResponse, tags=["Groups"])
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """Create a new group"""
    new_group = Group(**group.model_dump())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    logger.info(f"Created group: {new_group.id}")
    return new_group

@app.get("/groups/", response_model=list[GroupResponse], tags=["Groups"])
async def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all groups"""
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups

# QR Code endpoints
@app.post("/qrcodes/", response_model=QRCodeResponse, tags=["QR Codes"])
async def create_qrcode(qrcode: QRCodeCreate, db: Session = Depends(get_db)):
    """Create a new QR code"""
    # Verify ambassador exists
    ambassador = db.query(Ambassador).filter(Ambassador.id == qrcode.ambassador_id).first()
    if not ambassador:
        raise HTTPException(status_code=404, detail="Ambassador not found")
    
    new_qrcode = QRCode(**qrcode.model_dump())
    db.add(new_qrcode)
    db.commit()
    db.refresh(new_qrcode)
    logger.info(f"Created QR code: {new_qrcode.id}")
    return new_qrcode

@app.get("/qrcodes/{code}", response_model=QRCodeResponse, tags=["QR Codes"])
async def get_qrcode(code: str, db: Session = Depends(get_db)):
    """Get QR code by code value"""
    qrcode = db.query(QRCode).filter(QRCode.code == code).first()
    if not qrcode:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qrcode

# Transaction endpoints
@app.post("/transactions/", response_model=TransactionResponse, tags=["Transactions"])
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction and apply cashback"""
    transaction_service = TransactionService(db)
    new_transaction = transaction_service.process_transaction(
        transaction.customer_id,
        transaction.amount
    )
    logger.info(f"Created transaction: {new_transaction.id}")
    return new_transaction

@app.get("/transactions/", response_model=list[TransactionResponse], tags=["Transactions"])
async def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all transactions"""
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/transactions/customer/{customer_id}", response_model=list[TransactionResponse], tags=["Transactions"])
async def get_customer_transactions(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all transactions for a customer"""
    transactions = db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).offset(skip).limit(limit).all()
    return transactions

# Cashback Transfer endpoints
@app.post("/cashback-transfers/", response_model=CashbackTransferResponse, tags=["Cashback Transfers"])
async def create_cashback_transfer(transfer: CashbackTransferCreate, db: Session = Depends(get_db)):
    """Transfer cashback between customers"""
    cashback_service = CashbackService(db)
    new_transfer = cashback_service.transfer_cashback(
        transfer.from_customer_id,
        transfer.to_customer_id,
        transfer.amount
    )
    logger.info(f"Created cashback transfer: {new_transfer.id}")
    return new_transfer

@app.get("/cashback-transfers/", response_model=list[CashbackTransferResponse], tags=["Cashback Transfers"])
async def list_cashback_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all cashback transfers"""
    transfers = db.query(CashbackTransfer).offset(skip).limit(limit).all()
    return transfers

# Payout endpoints
@app.post("/payouts/", response_model=PayoutResponse, tags=["Payouts"])
async def create_payout(payout: PayoutCreate, db: Session = Depends(get_db)):
    """Process a cashback payout"""
    payout_service = PayoutService(db)
    new_payout = payout_service.process_payout(
        payout.customer_id,
        payout.amount
    )
    logger.info(f"Created payout: {new_payout.id}")
    return new_payout

@app.get("/payouts/", response_model=list[PayoutResponse], tags=["Payouts"])
async def list_payouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all payouts"""
    payouts = db.query(Payout).offset(skip).limit(limit).all()
    return payouts

@app.get("/payouts/customer/{customer_id}", response_model=list[PayoutResponse], tags=["Payouts"])
async def get_customer_payouts(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all payouts for a customer"""
    payouts = db.query(Payout).filter(
        Payout.customer_id == customer_id
    ).offset(skip).limit(limit).all()
    return payouts

# Gift Card endpoints
@app.post("/gift-cards/", response_model=GiftCardResponse, tags=["Gift Cards"])
async def create_gift_card(gift_card: GiftCardCreate, db: Session = Depends(get_db)):
    """Create a new gift card"""
    new_gift_card = GiftCard(**gift_card.model_dump())
    db.add(new_gift_card)
    db.commit()
    db.refresh(new_gift_card)
    logger.info(f"Created gift card: {new_gift_card.id}")
    return new_gift_card

@app.get("/gift-cards/{code}", response_model=GiftCardResponse, tags=["Gift Cards"])
async def get_gift_card(code: str, db: Session = Depends(get_db)):
    """Get gift card by code"""
    gift_card = db.query(GiftCard).filter(GiftCard.code == code).first()
    if not gift_card:
        raise HTTPException(status_code=404, detail="Gift card not found")
    return gift_card

@app.delete("/gift-cards/{code}", tags=["Gift Cards"])
async def redeem_gift_card(code: str, customer_id: int, db: Session = Depends(get_db)):
    """Redeem a gift card and add value to customer's cashback balance"""
    gift_card = db.query(GiftCard).filter(GiftCard.code == code).first()
    if not gift_card:
        raise HTTPException(status_code=404, detail="Gift card not found")
    
    cashback_service = CashbackService(db)
    cashback_service.add_balance(customer_id, gift_card.value)
    
    # Delete the gift card after redemption
    db.delete(gift_card)
    db.commit()
    
    logger.info(f"Redeemed gift card {code} for customer {customer_id}")
    return {"message": "Gift card redeemed successfully", "value": gift_card.value}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
