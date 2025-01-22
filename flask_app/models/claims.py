from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from flask_app.database.db import db
from sqlalchemy.orm import relationship


class MealCount(db.Model):
    __tablename__ = 'meal_counts'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    claims_id = Column(Integer, ForeignKey('claims.id'))  # ForeignKey reference to Claims
    claims = relationship("Claims", back_populates="meal_counts", foreign_keys=[claims_id], remote_side=[(claims_id)])
    
    # Meal count fields
    infant_breakfast_birth_3mos = Column(Integer, default=0)
    infant_breakfast_4_7mos = Column(Integer, default=0)
    infant_breakfast_8_12mos = Column(Integer, default=0)    
    child_breakfast_1yrs = Column(Integer, default=0)
    child_breakfast_2yrs = Column(Integer, default=0)
    child_breakfast_3_5yrs = Column(Integer, default=0)
    child_breakfast_6_12yrs = Column(Integer, default=0)
    infant_AMSnack_birth_3mos = Column(Integer, default=0)
    infant_AMSnack_4_7mos = Column(Integer, default=0)
    infant_AMSnack_8_12mos = Column(Integer, default=0)
    child_AMSnack_1yrs = Column(Integer, default=0)
    child_AMSnack_2yrs = Column(Integer, default=0)
    child_AMSnack_3_5yrs = Column(Integer, default=0)
    child_AMSnack_6_12yrs = Column(Integer, default=0)
    infant_Lunch_birth_3mos = Column(Integer, default=0)
    infant_Lunch_4_7mos = Column(Integer, default=0)
    infant_Lunch_8_12mos = Column(Integer, default=0)
    child_Lunch_1yrs = Column(Integer, default=0)
    child_Lunch_2yrs = Column(Integer, default=0)
    child_Lunch_3_5yrs = Column(Integer, default=0)
    child_Lunch_6_12yrs = Column(Integer, default=0)
    infant_PMSnack_birth_3mos = Column(Integer, default=0)
    infant_PMSnack_4_7mos = Column(Integer, default=0)
    infant_PMSnack_8_12mos = Column(Integer, default=0)
    child_PMSnack_1yrs = Column(Integer, default=0)
    child_PMSnack_2yrs = Column(Integer, default=0)
    child_PMSnack_3_5yrs = Column(Integer, default=0)
    child_PMSnack_6_12yrs = Column(Integer, default=0)
    infant_Supper_birth_3mos = Column(Integer, default=0)
    infant_Supper_4_7mos = Column(Integer, default=0)
    infant_Supper_8_12mos = Column(Integer, default=0)
    child_Supper_1yrs = Column(Integer, default=0)
    child_Supper_2yrs = Column(Integer, default=0)
    child_Supper_3_5yrs = Column(Integer, default=0)
    child_Supper_6_12yrs = Column(Integer, default=0)
    meal_count = Column(Integer, default=0)
    def __repr__(self):
        return f'<MealCount {self.id} {self.meal_count}>'
class Claims(db.Model):
    __tablename__ = 'claims'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'))
    meal_counts_id = Column(Integer, ForeignKey('meal_counts.id'), nullable=False)
    
    # Specify the foreign_keys argument and remote() annotation
    meal_counts = relationship("MealCount", back_populates="claims", foreign_keys=[meal_counts_id], remote_side=[(MealCount.claims_id)])
    receipt = relationship("Receipt", back_populates="claims", foreign_keys=[receipt_id])  # Specify foreign_keys here

    def __repr__(self):
        return f'<Claims {self.id} {self.meal_counts} {self.receipt}>'



class Receipt(db.Model):
    __tablename__ = 'receipt'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    claims_id = Column(Integer, ForeignKey('claims.id'))  # ForeignKey reference to Claims
    paid_to = Column(String(120))
    purchase_type = Column(String(255), nullable=False)
    purchase_cost = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    operating_cost = Column(Float, nullable=True)

    # Specify the foreign_keys argument to clarify which foreign key to use
    claims = relationship('Claims', back_populates='receipt', foreign_keys=[claims_id])

    def __init__(self, paid_to, purchase_type, purchase_cost, purchase_date, operating_cost=None):
        self.paid_to = paid_to
        self.purchase_type = purchase_type
        self.purchase_cost = purchase_cost
        self.purchase_date = purchase_date
        self.operating_cost = operating_cost

    def __repr__(self):
        return f'<Receipt {self.id} {self.purchase_type}>'