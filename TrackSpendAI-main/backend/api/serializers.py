import datetime
from rest_framework import serializers
from bson import ObjectId
from .models import (
    Review, User, Transaction, Budget, Account,
    Goal, Portfolio, ContactMessage
)

# -------------------------
# ✅ Common Helper
# -------------------------
def update_instance(instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance

# =======================
# AUTH SERIALIZERS
# =======================

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


# =======================
# ACCOUNT SERIALIZER
# =======================

class AccountSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    account_name = serializers.CharField()
    account_type = serializers.ChoiceField(choices=["bank", "wallet", "credit_card", "cash"])
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    total_income = serializers.FloatField(required=False)
    total_expenses = serializers.FloatField(required=False)
    total_balance = serializers.FloatField(required=False)
    savings_rate = serializers.FloatField(required=False)

    def create(self, validated_data):
        validated_data['user_id'] = User.objects.get(id=ObjectId(validated_data['user_id']))
        return Account(**validated_data).save()

    def update(self, instance, validated_data):
        if 'user_id' in validated_data:
            validated_data['user_id'] = User.objects.get(id=ObjectId(validated_data['user_id']))
        return update_instance(instance, validated_data)


# =======================
# TRANSACTION SERIALIZER
# =======================

def update_account_totals(account):
    transactions = Transaction.objects(account_id=account)
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expenses
    savings_rate = (balance / total_income * 100) if total_income > 0 else 0.0
    account.total_income = total_income
    account.total_expenses = total_expenses
    account.total_balance = balance
    account.savings_rate = round(savings_rate, 2)
    account.save()

def update_matching_budgets(transaction):
    try:
        user = transaction.user_id
        account = transaction.account_id
        category = transaction.category
        matching_budgets = Budget.objects(
            user_id=user,
            account_id=account,
            name=category
        )
        for budget in matching_budgets:
            total_spent = sum(
                t.amount for t in Transaction.objects(
                    user_id=user,
                    account_id=account,
                    category=category,
                    type="expense"
                )
            )
            budget.spent = total_spent
            budget.remaining = budget.limit - total_spent
            budget.toggle = total_spent >= budget.limit
            budget.save()
    except Exception as e:
        print("❌ Budget update failed:", str(e))


class TransactionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    account_id = serializers.CharField()
    type = serializers.ChoiceField(choices=["income", "expense"])
    amount = serializers.FloatField()
    category = serializers.CharField()
    description = serializers.CharField(required=False)
    date = serializers.DateTimeField()
    is_recurring = serializers.BooleanField(default=False)

    def create(self, validated_data):
        validated_data['user_id'] = User.objects.get(id=validated_data['user_id'])
        validated_data['account_id'] = Account.objects.get(id=validated_data['account_id'])
        tx = Transaction(**validated_data).save()
        update_account_totals(tx.account_id)
        update_matching_budgets(tx)
        return tx

    def update(self, instance, validated_data):
        if 'user_id' in validated_data:
            validated_data['user_id'] = User.objects.get(id=validated_data['user_id'])
        if 'account_id' in validated_data:
            validated_data['account_id'] = Account.objects.get(id=validated_data['account_id'])
        instance = update_instance(instance, validated_data)
        update_account_totals(instance.account_id)
        update_matching_budgets(instance)
        return instance


# =======================
# BUDGET SERIALIZER
# =======================

class BudgetSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    account_id = serializers.CharField()
    type = serializers.ChoiceField(choices=["Daily", "Weekly", "Monthly", "Yearly"])
    name = serializers.CharField()
    limit = serializers.FloatField()
    spent = serializers.FloatField(required=False)
    remaining = serializers.FloatField(required=False)
    toggle = serializers.BooleanField(required=False)
    date = serializers.DateTimeField()

    def create(self, validated_data):
        validated_data['user_id'] = User.objects.get(id=validated_data['user_id'])
        validated_data['account_id'] = Account.objects.get(id=validated_data['account_id'])
        if 'remaining' not in validated_data:
            validated_data['remaining'] = validated_data['limit'] - validated_data.get('spent', 0)
        if 'toggle' not in validated_data:
            validated_data['toggle'] = validated_data['spent'] >= validated_data['limit']
        return Budget(**validated_data).save()

    def update(self, instance, validated_data):
        if 'user_id' in validated_data:
            validated_data['user_id'] = User.objects.get(id=validated_data['user_id'])
        if 'account_id' in validated_data:
            validated_data['account_id'] = Account.objects.get(id=validated_data['account_id'])
        return self.update_instance(instance, validated_data)

    def update_instance(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if 'limit' in validated_data or 'spent' in validated_data:
            instance.remaining = instance.limit - instance.spent
            instance.toggle = instance.spent >= instance.limit
        instance.save()
        return instance




# class GoalSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)
#     user_id = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField(required=False, allow_blank=True)
#     targetAmount = serializers.FloatField()
#     currentAmount = serializers.FloatField(required=False, default=0)
#     targetDate = serializers.DateTimeField()
#     category = serializers.CharField()
#     priority = serializers.ChoiceField(choices=["Low", "Medium", "High"])
#     status = serializers.ChoiceField(choices=["In Progress", "Completed"], read_only=True)
#     color = serializers.CharField(required=False)

#     def create(self, validated_data):
#         validated_data["user_id"] = User.objects.get(id=ObjectId(validated_data["user_id"]))
#         validated_data["target_amount"] = validated_data.pop("targetAmount")
#         validated_data["current_amount"] = validated_data.pop("currentAmount", 0)
#         validated_data["target_date"] = validated_data.pop("targetDate")

#         validated_data["status"] = (
#             "Completed" if validated_data["current_amount"] >= validated_data["target_amount"] else "In Progress"
#         )
#         validated_data["created_at"] = datetime.datetime.utcnow()
#         validated_data["updated_at"] = datetime.datetime.utcnow()

#         return Goal(**validated_data).save()

#     def update(self, instance, validated_data):
#         if "user_id" in validated_data:
#             validated_data["user_id"] = User.objects.get(id=ObjectId(validated_data["user_id"]))

#         if "targetAmount" in validated_data:
#             validated_data["target_amount"] = validated_data.pop("targetAmount")
#         if "currentAmount" in validated_data:
#             validated_data["current_amount"] = validated_data.pop("currentAmount")
#         if "targetDate" in validated_data:
#             validated_data["target_date"] = validated_data.pop("targetDate")

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.status = "Completed" if instance.current_amount >= instance.target_amount else "In Progress"
#         instance.updated_at = datetime.datetime.utcnow()
#         instance.save()
#         return instance

#     def to_representation(self, instance):
#         return {
#             "id": str(instance.id),
#             "user_id": str(getattr(instance.user_id, "id", instance.user_id)),
#             "title": instance.title,
#             "description": instance.description,
#             "targetAmount": instance.target_amount,
#             "currentAmount": instance.current_amount,
#             "targetDate": instance.target_date,
#             "category": instance.category,
#             "priority": instance.priority,
#             "status": instance.status,
#             "color": instance.color,
#         }

from rest_framework import serializers
from bson import ObjectId
from .models import Goal, User


class GoalSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    targetAmount = serializers.FloatField()
    currentAmount = serializers.FloatField(required=False, default=0)
    targetDate = serializers.DateTimeField()
    category = serializers.CharField()
    priority = serializers.ChoiceField(choices=["Low", "Medium", "High"])
    status = serializers.ChoiceField(choices=["In Progress", "Completed"], read_only=True)
    color = serializers.CharField(required=False)

    # ------------------
    # CREATE
    # ------------------
    def create(self, validated_data):
        validated_data["user_id"] = User.objects.get(id=ObjectId(validated_data["user_id"]))
        validated_data["target_amount"] = validated_data.pop("targetAmount")
        validated_data["current_amount"] = validated_data.pop("currentAmount", 0)
        validated_data["target_date"] = validated_data.pop("targetDate")

        validated_data["status"] = (
            "Completed" if validated_data["current_amount"] >= validated_data["target_amount"] else "In Progress"
        )
        return Goal(**validated_data).save()

    # ------------------
    # UPDATE
    # ------------------
    def update(self, instance, validated_data):
        if "user_id" in validated_data:
            validated_data["user_id"] = User.objects.get(id=ObjectId(validated_data["user_id"]))

        if "targetAmount" in validated_data:
            validated_data["target_amount"] = validated_data.pop("targetAmount")
        if "currentAmount" in validated_data:
            validated_data["current_amount"] = validated_data.pop("currentAmount")
        if "targetDate" in validated_data:
            validated_data["target_date"] = validated_data.pop("targetDate")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.status = "Completed" if instance.current_amount >= instance.target_amount else "In Progress"
        instance.save()
        return instance

    # ------------------
    # RESPONSE FORMAT
    # ------------------
    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "user_id": str(instance.user_id.id) if instance.user_id else None,
            "title": instance.title,
            "description": instance.description,
            "targetAmount": instance.target_amount,
            "currentAmount": instance.current_amount,
            "targetDate": instance.target_date.isoformat() if instance.target_date else None,
            "category": instance.category,
            "priority": instance.priority,
            "status": instance.status,
            "color": instance.color,
        }


# =======================
# PORTFOLIO SERIALIZER
# =======================


class PortfolioSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    name = serializers.CharField()  # Apple Inc.
    symbol = serializers.CharField()  # AAPL
    type = serializers.ChoiceField(choices=["Stock", "Crypto", "Mutual Fund", "ETF", "Real Estate", "Commodity", "Other"])
    quantity = serializers.FloatField()
    buyPrice = serializers.FloatField()
    currentPrice = serializers.FloatField()
    totalValue = serializers.FloatField(read_only=True)
    gainLoss = serializers.FloatField(read_only=True)
    gainLossPercent = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        try:
            validated_data['user_id'] = User.objects.get(id=ObjectId(validated_data['user_id']))
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User not found"})
        return Portfolio(**validated_data).save()

    def update(self, instance, validated_data):
        if 'user_id' in validated_data:
            try:
                validated_data['user_id'] = User.objects.get(id=ObjectId(validated_data['user_id']))
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_id": "User not found"})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance

    def to_representation(self, instance):
        """Custom output format to match frontend keys exactly"""
        representation = super().to_representation(instance)
        representation["totalValue"] = instance.totalValue
        representation["gainLoss"] = instance.gainLoss
        representation["gainLossPercent"] = instance.gainLossPercent
        return representation



# =======================
# DEBT SERIALIZER
# =======================

# serializers.py (add imports if needed)
from rest_framework import serializers
from bson import ObjectId
from .models import Debt, User

class DebtSerializer(serializers.Serializer):
    # Read-only ID as string
    id = serializers.CharField(read_only=True)
    # Accept user_id as string from frontend
    user_id = serializers.CharField(write_only=True)

    name = serializers.CharField()
    type = serializers.CharField()
    total_amount = serializers.FloatField()
    remaining_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    minimum_payment = serializers.FloatField()
    due_date = serializers.DateField()
    color = serializers.CharField(required=False, allow_blank=True, default="from-gray-400 to-gray-500")

    # For responses, also show user as string id
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        try:
            return str(obj.user_id.id)
        except Exception:
            try:
                return str(obj.user_id.pk)
            except Exception:
                return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Consistent snake_case for backend
        data.update({
            "total_amount": instance.total_amount,
            "remaining_amount": instance.remaining_amount,
            "interest_rate": instance.interest_rate,
            "minimum_payment": instance.minimum_payment,
        })
        return data

    def create(self, validated_data):
        user_id_str = validated_data.pop("user_id", None)
        if not user_id_str:
            raise serializers.ValidationError({"user_id": "This field is required."})
        try:
            user = User.objects.get(id=ObjectId(user_id_str))
        except Exception:
            raise serializers.ValidationError({"user_id": "Invalid user id."})

        debt = Debt(
            user_id=user,
            name=validated_data["name"],
            type=validated_data["type"],
            total_amount=validated_data["total_amount"],
            remaining_amount=validated_data["remaining_amount"],
            interest_rate=validated_data["interest_rate"],
            minimum_payment=validated_data["minimum_payment"],
            due_date=validated_data["due_date"],
            color=validated_data.get("color") or "from-gray-400 to-gray-500",
        )
        debt.save()
        return debt

    def update(self, instance, validated_data):
        # user_id change optional (rare)
        user_id_str = validated_data.pop("user_id", None)
        if user_id_str:
            try:
                user = User.objects.get(id=ObjectId(user_id_str))
                instance.user_id = user
            except Exception:
                raise serializers.ValidationError({"user_id": "Invalid user id."})

        for f in ["name", "type", "total_amount", "remaining_amount", "interest_rate",
                  "minimum_payment", "due_date", "color"]:
            if f in validated_data:
                setattr(instance, f, validated_data[f])
        instance.save()
        return instance


# =======================
# REVIEW SERIALIZER
# =======================

class ReviewSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    rating = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True)
    submitted_at = serializers.DateTimeField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return getattr(obj.user_id, 'username', 'Anonymous')

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user_id"])
        validated_data["user_id"] = user
        existing_review = Review.objects(user_id=user).first()
        if existing_review:
            existing_review.rating = validated_data.get('rating', existing_review.rating)
            existing_review.comment = validated_data.get('comment', existing_review.comment)
            existing_review.submitted_at = datetime.datetime.utcnow()
            existing_review.save()
            return existing_review
        return Review(**validated_data).save()


# =======================
# CONTACT MESSAGE SERIALIZER
# =======================

class ContactMessageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

    def create(self, validated_data):
        contact = ContactMessage(**validated_data)
        contact.save()
        return contact


# --- ML SERIALIZERS (append these at the end of serializers.py) ---
from rest_framework import serializers
from bson import ObjectId
from .models import User, Transaction, MLPrediction, SpendingAnomaly, RecurringPattern

class MLPredictionSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    prediction_type = serializers.CharField()
    target_period = serializers.CharField()
    predicted_income = serializers.FloatField()
    predicted_expense = serializers.FloatField()
    predicted_balance = serializers.FloatField()
    confidence = serializers.FloatField()
    model_version = serializers.CharField()
    created_at = serializers.DateTimeField()

class SpendingAnomalySerializer(serializers.Serializer):
    user_id = serializers.CharField()
    transaction_id = serializers.CharField()
    anomaly_score = serializers.FloatField()
    flag_reason = serializers.CharField()
    flagged_at = serializers.DateTimeField()
    reviewed = serializers.BooleanField()

class RecurringPatternSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    pattern = serializers.CharField()
    category = serializers.CharField()
    frequency = serializers.CharField()
    average_amount = serializers.FloatField()
    last_detected = serializers.DateTimeField()


class SpendingAnomalySerializer(serializers.Serializer):
    transaction = serializers.SerializerMethodField()

    class Meta:
        model = SpendingAnomaly
        fields = "__all__"  # ya explicitly ["id", "transaction_id", "anomaly_score", "flag_reason", "flagged_at", "reviewed", "transaction"]

    def get_transaction(self, obj):
        try:
            from .serializers import TransactionSerializer
            txn = obj.transaction_id
            return TransactionSerializer(txn).data if txn else None
        except Exception:
            return None
