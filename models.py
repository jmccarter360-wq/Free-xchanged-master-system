from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Ambassador(Base):
    __tablename__ = 'ambassadors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='ambassadors')
    qr_codes = relationship('QRCode', back_populates='ambassador')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ambassadors = relationship('Ambassador', back_populates='group')

class QRCode(Base):
    __tablename__ = 'qr_codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    ambassador_id = Column(Integer, ForeignKey('ambassadors.id'))
    ambassador = relationship('Ambassador', back_populates='qr_codes')

class CashbackBalance(Base):
    __tablename__ = 'cashback_balances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    balance = Column(Float, default=0)
    customer = relationship('Customer')

class GiftCard(Base):
    __tablename__ = 'gift_cards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    value = Column(Float, nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    customer = relationship('Customer')

class CashbackTransfer(Base):
    __tablename__ = 'cashback_transfers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_customer_id = Column(Integer, ForeignKey('customers.id'))
    to_customer_id = Column(Integer, ForeignKey('customers.id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    from_customer = relationship('Customer', foreign_keys=[from_customer_id])
    to_customer = relationship('Customer', foreign_keys=[to_customer_id])

class Payout(Base):
    __tablename__ = 'payouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    customer = relationship('Customer')