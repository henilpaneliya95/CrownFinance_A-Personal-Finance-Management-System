import mongoengine as me
import datetime
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime as dt

# ==========================
# USER MODEL
# ==========================
class User(me.Document):
    username = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    meta = {'collection': 'users'}


# ==========================
# ACCOUNT MODEL
# ==========================
class Account(me.Document):
    user_id = me.ReferenceField(User, required=True)
    account_name = me.StringField(required=True)
    account_type = me.StringField(required=True, choices=["bank", "wallet", "credit_card", "cash"])
    created_at = me.DateTimeField(default=datetime.datetime.utcnow)
    description = me.StringField(default="")
    total_income = me.FloatField(default=0.0)
    total_expenses = me.FloatField(default=0.0)
    total_balance = me.FloatField(default=0.0)
    savings_rate = me.FloatField(default=0.0)

    meta = {'collection': 'accounts'}


# ==========================
# TRANSACTION MODEL
# ==========================
CATEGORY_CHOICES = [
    # Income Categories
    "salary", "freelance", "business", "investment", "rental_income",
    "gift", "cashback", "bonus", "commission", "other_income",

    # Expense Categories
    "groceries", "rent", "utilities", "internet", "transportation",
    "education", "health", "shopping", "travel", "other_expense",

    # Other
    "other"
]

class Transaction(me.Document):
    user_id = me.ReferenceField(User, required=True)
    account_id = me.ReferenceField(Account, required=True)
    type = me.StringField(required=True, choices=["income", "expense"])
    amount = me.FloatField(required=True)
    category = me.StringField(required=True, choices=CATEGORY_CHOICES)
    description = me.StringField()
    date = me.DateTimeField(default=datetime.datetime.utcnow)
    is_recurring = me.BooleanField(default=False)

    meta = {'collection': 'transactions'}


# ==========================
# BUDGET MODEL
# ==========================
class Budget(me.Document):
    user_id = me.ReferenceField(User, required=True)
    account_id = me.ReferenceField(Account, required=True)
    type = me.StringField(required=True, choices=["Daily", "Weekly", "Monthly", "Yearly"])
    name = me.StringField(required=True)
    limit = me.FloatField(required=True)
    spent = me.FloatField(default=0)
    remaining = me.FloatField(default=0)
    toggle = me.BooleanField(default=False)
    date = me.DateTimeField(required=True)

    meta = {'collection': 'budgets'}


# ==========================
# GOAL MODEL
# ==========================
class Goal(me.Document):
    user_id = me.ReferenceField(User, required=True)
    title = me.StringField(required=True)
    description = me.StringField(default="")
    target_amount = me.FloatField(required=True)
    current_amount = me.FloatField(default=0)
    target_date = me.DateTimeField(required=True)

    category = me.StringField(choices=[
        "Emergency", "Travel", "Transportation", "Housing",
        "Education", "Investment", "Other"
    ], default="Other")

    priority = me.StringField(choices=["Low", "Medium", "High"], default="Medium")
    status = me.StringField(choices=["In Progress", "Completed"], default="In Progress")
    color = me.StringField(default="from-blue-500 to-blue-600")  # optional UI color

    created_at = me.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "goals"}

# ==========================
# PORTFOLIO MODEL
# ==========================


class Portfolio(me.Document):
    user_id = me.ReferenceField(User, required=True)
    name = me.StringField()
    symbol = me.StringField()
    type = me.StringField()
    quantity = me.FloatField()
    buyPrice = me.FloatField()
    currentPrice = me.FloatField()

    # old fields (to avoid crash until migration)
    asset_name = me.StringField()
    asset_type = me.StringField()
    purchase_price = me.FloatField()
    purchase_date = me.DateTimeField()
    notes = me.StringField()

    meta = {'collection': 'portfolios'}


    @property
    def totalValue(self):
        """Total value = quantity × current price"""
        return round(self.quantity * self.currentPrice, 2)

    @property
    def gainLoss(self):
        """Absolute profit or loss"""
        return round((self.currentPrice - self.buyPrice) * self.quantity, 2)

    @property
    def gainLossPercent(self):
        """Percentage profit or loss"""
        if self.buyPrice > 0:
            return round(((self.currentPrice - self.buyPrice) / self.buyPrice) * 100, 2)
        return 0.0


# ==========================
# DEBT MODEL
# ==========================

# models.py (add this near other Document classes)
from mongoengine import Document, StringField, FloatField, DateField, ReferenceField, DateTimeField
from .models import User  # if models split hain to import adjust karo

class Debt(Document):
    meta = {"collection": "debts", "indexes": ["user_id", "due_date", "type", "name"]}
    user_id = ReferenceField(User, required=True)   # same style as Goals/User references
    name = StringField(required=True, max_length=200)
    type = StringField(required=True, choices=[
        "Credit Card", "Personal Loan", "Auto Loan", "Home Loan", "Student Loan", "Other"
    ])
    total_amount = FloatField(required=True, min_value=0)
    remaining_amount = FloatField(required=True, min_value=0)
    interest_rate = FloatField(required=True, min_value=0)  # percentage
    minimum_payment = FloatField(required=True, min_value=0)
    due_date = DateField(required=True)
    color = StringField(default="from-gray-400 to-gray-500")
    created_at = DateTimeField()
    updated_at = DateTimeField()


# ==========================
# REVIEW MODEL
# ==========================
class Review(me.Document):
    user_id = me.ReferenceField(User, required=True)
    rating = me.IntField(min_value=1, max_value=5, required=True)
    comment = me.StringField(required=False)
    submitted_at = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'reviews'}


# ==========================
# CONTACT MESSAGE MODEL
# ==========================
# conact page

from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class ContactMessage(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True)
    subject = StringField(required=True, max_length=200)
    message = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

# --- ML MODELS (append these at the end of models.py) ---
import datetime
import mongoengine as me

class MLPrediction(me.Document):
    user_id = me.ReferenceField('User', required=True)
    prediction_type = me.StringField(required=True)        # e.g. 'monthly_forecast'
    target_period = me.StringField()                        # e.g. '2025-09'
    predicted_income = me.FloatField(default=0.0)
    predicted_expense = me.FloatField(default=0.0)
    predicted_balance = me.FloatField(default=0.0)
    confidence = me.FloatField(default=0.0)
    model_version = me.StringField(default="v1.0")
    created_at = me.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'ml_predictions'}

class SpendingAnomaly(me.Document):
    user_id = me.ReferenceField('User', required=True)
    transaction_id = me.ReferenceField('Transaction', required=True)
    anomaly_score = me.FloatField(default=0.0)
    flag_reason = me.StringField()
    flagged_at = me.DateTimeField(default=datetime.datetime.utcnow)
    reviewed = me.BooleanField(default=False)
    meta = {'collection': 'spending_anomalies'}

class RecurringPattern(me.Document):
    user_id = me.ReferenceField('User', required=True)
    pattern = me.StringField(required=True)                 # "category ~approx_amount"
    category = me.StringField(required=True)
    frequency = me.StringField(choices=["Weekly", "Monthly", "Irregular"])
    average_amount = me.FloatField(default=0.0)
    last_detected = me.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'recurring_patterns'}
