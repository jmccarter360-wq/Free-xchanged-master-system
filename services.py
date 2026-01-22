from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from models import (
    Customer, CashbackBalance, Transaction, 
    CashbackTransfer, Payout
)
from utils.validators import is_valid_amount
from utils.error_handlers import NotFoundError, ValidationError
from utils.retry_logic import retry


class CashbackService:
    """Service for managing cashback balances and transfers"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cashback_percentage = 0.05  # 5% cashback rate
    
    def get_balance(self, customer_id: int) -> float:
        """Get customer's cashback balance"""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFoundError(f"Customer {customer_id} not found")
        
        balance = self.db.query(CashbackBalance).filter(
            CashbackBalance.customer_id == customer_id
        ).first()
        
        if not balance:
            # Create balance if it doesn't exist
            balance = CashbackBalance(customer_id=customer_id, balance=0)
            self.db.add(balance)
            self.db.commit()
            self.db.refresh(balance)
        
        return balance.balance
    
    def add_balance(self, customer_id: int, amount: float) -> float:
        """Add amount to customer's cashback balance"""
        if not is_valid_amount(amount):
            raise ValidationError("Invalid amount")
        
        balance = self.db.query(CashbackBalance).filter(
            CashbackBalance.customer_id == customer_id
        ).first()
        
        if not balance:
            balance = CashbackBalance(customer_id=customer_id, balance=0)
            self.db.add(balance)
        
        balance.balance += amount
        self.db.commit()
        self.db.refresh(balance)
        
        return balance.balance
    
    def deduct_balance(self, customer_id: int, amount: float) -> float:
        """Deduct amount from customer's cashback balance"""
        if not is_valid_amount(amount):
            raise ValidationError("Invalid amount")
        
        balance = self.db.query(CashbackBalance).filter(
            CashbackBalance.customer_id == customer_id
        ).first()
        
        if not balance or balance.balance < amount:
            raise ValidationError("Insufficient balance")
        
        balance.balance -= amount
        self.db.commit()
        self.db.refresh(balance)
        
        return balance.balance
    
    def transfer_cashback(self, from_customer_id: int, to_customer_id: int, amount: float) -> CashbackTransfer:
        """Transfer cashback from one customer to another"""
        if not is_valid_amount(amount):
            raise ValidationError("Invalid amount")
        
        if from_customer_id == to_customer_id:
            raise ValidationError("Cannot transfer to the same customer")
        
        # Verify both customers exist
        from_customer = self.db.query(Customer).filter(Customer.id == from_customer_id).first()
        to_customer = self.db.query(Customer).filter(Customer.id == to_customer_id).first()
        
        if not from_customer:
            raise NotFoundError(f"Customer {from_customer_id} not found")
        if not to_customer:
            raise NotFoundError(f"Customer {to_customer_id} not found")
        
        # Deduct from sender
        self.deduct_balance(from_customer_id, amount)
        
        # Add to recipient
        self.add_balance(to_customer_id, amount)
        
        # Record the transfer
        transfer = CashbackTransfer(
            from_customer_id=from_customer_id,
            to_customer_id=to_customer_id,
            amount=amount,
            date=datetime.now()
        )
        self.db.add(transfer)
        self.db.commit()
        self.db.refresh(transfer)
        
        return transfer


class TransactionService:
    """Service for managing transactions"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cashback_service = CashbackService(db)
    
    def process_transaction(self, customer_id: int, amount: float) -> Transaction:
        """Process a transaction and apply cashback"""
        if not is_valid_amount(amount):
            raise ValidationError("Invalid amount")
        
        # Verify customer exists
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFoundError(f"Customer {customer_id} not found")
        
        # Create transaction
        transaction = Transaction(
            customer_id=customer_id,
            amount=amount,
            date=datetime.now()
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        # Apply cashback
        cashback_amount = amount * self.cashback_service.cashback_percentage
        self.cashback_service.add_balance(customer_id, cashback_amount)
        
        return transaction


class PayoutService:
    """Service for managing payouts"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cashback_service = CashbackService(db)
    
    @retry(max_attempts=3, delay=1, backoff=2)
    def process_payout(self, customer_id: int, amount: float) -> Payout:
        """Process a payout from customer's cashback balance"""
        if not is_valid_amount(amount):
            raise ValidationError("Invalid amount")
        
        # Verify customer exists
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFoundError(f"Customer {customer_id} not found")
        
        # Verify sufficient balance
        current_balance = self.cashback_service.get_balance(customer_id)
        if current_balance < amount:
            raise ValidationError(f"Insufficient balance. Available: {current_balance}")
        
        # Deduct from balance
        self.cashback_service.deduct_balance(customer_id, amount)
        
        # Create payout record
        payout = Payout(
            customer_id=customer_id,
            amount=amount,
            date=datetime.now()
        )
        self.db.add(payout)
        self.db.commit()
        self.db.refresh(payout)
        
        # Here you would integrate with payment processor (e.g., Stripe)
        # For now, we just record the payout
        
        return payout
