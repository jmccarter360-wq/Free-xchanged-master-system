from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Ambassador schemas
class AmbassadorBase(BaseModel):
    name: str
    email: EmailStr


class AmbassadorCreate(AmbassadorBase):
    group_id: Optional[int] = None


class AmbassadorResponse(AmbassadorBase):
    id: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True


# Customer schemas
class CustomerBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# Group schemas
class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupResponse(GroupBase):
    id: int

    class Config:
        from_attributes = True


# QRCode schemas
class QRCodeBase(BaseModel):
    code: str


class QRCodeCreate(QRCodeBase):
    ambassador_id: int


class QRCodeResponse(QRCodeBase):
    id: int
    ambassador_id: int

    class Config:
        from_attributes = True


# Transaction schemas
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")


class TransactionCreate(TransactionBase):
    customer_id: int


class TransactionResponse(TransactionBase):
    id: int
    customer_id: int
    date: datetime

    class Config:
        from_attributes = True


# CashbackTransfer schemas
class CashbackTransferBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transfer amount must be positive")


class CashbackTransferCreate(CashbackTransferBase):
    from_customer_id: int
    to_customer_id: int


class CashbackTransferResponse(CashbackTransferBase):
    id: int
    from_customer_id: int
    to_customer_id: int
    date: datetime

    class Config:
        from_attributes = True


# Payout schemas
class PayoutBase(BaseModel):
    amount: float = Field(..., gt=0, description="Payout amount must be positive")


class PayoutCreate(PayoutBase):
    customer_id: int


class PayoutResponse(PayoutBase):
    id: int
    customer_id: int
    date: datetime

    class Config:
        from_attributes = True


# GiftCard schemas
class GiftCardBase(BaseModel):
    code: str
    value: float = Field(..., gt=0, description="Gift card value must be positive")


class GiftCardCreate(GiftCardBase):
    pass


class GiftCardResponse(GiftCardBase):
    id: int

    class Config:
        from_attributes = True


# CashbackBalance schemas
class CashbackBalanceResponse(BaseModel):
    customer_id: int
    balance: float

    class Config:
        from_attributes = True
