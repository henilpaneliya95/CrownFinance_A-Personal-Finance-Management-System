from django.urls import path
from .views import (
    # Auth Views
    AnomalyByUserAPIView,
    BudgetListByUserNoAuthView,
    DebtAPIView,
    ExpensePredictionAPIView,
   
    GoalAPIView,
    GoalETAPredictionAPIView,
    RecurringByUserAPIView,
    RunAnomalyDetectionAPIView,
    RunRecurringDetectionAPIView,
    # GoalDetailAPIView,
    SignupView,
    LoginView,

    # Account Views
    AccountListCreateAPIView,
    AccountDetailView,
    AccountUpdateView,
    AccountDeleteView,

    # Transaction Views
    TransactionListCreateAPIView,
    TransactionDetailView,
    TransactionUpdateView,
    TransactionDeleteView,
    TransactionsByUserView,
    TransactionsByAccountView,

    # Budget Views
    BudgetCreateView,
    BudgetListByUserView,
    BudgetListByAccountView,
    BudgetDetailView,

    # Goal Views
    # GoalListCreateAPIView,


    # Portfolio Views
    PortfolioListCreateAPIView,
    PortfolioDetailView,

    # Debt Views


    # Other Features
    ReviewView,
    ContactMessageView,
)

urlpatterns = [

    # ========================
    # AUTHENTICATION ENDPOINTS
    # ========================
    path('users/signup/', SignupView.as_view(), name='user-signup'),  # Register a new user
    path('users/login/', LoginView.as_view(), name='user-login'),     # Login and get JWT token

    # =================
    # ACCOUNT ENDPOINTS
    # =================
    path('accounts/', AccountListCreateAPIView.as_view(), name='account-list-create'),  # GET all accounts / POST new account
    path('accounts/<str:pk>/', AccountDetailView.as_view(), name='account-detail'),     # GET account details
    path('accounts/<str:pk>/update/', AccountUpdateView.as_view(), name='account-update'),  # PUT update account
    path('accounts/<str:pk>/delete/', AccountDeleteView.as_view(), name='account-delete'),  # DELETE account

    # =====================
    # TRANSACTION ENDPOINTS
    # =====================
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list'),  # GET all / POST new transaction
    path('transactions/<str:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),  # GET transaction details
    path('transactions/<str:pk>/update/', TransactionUpdateView.as_view(), name='transaction-update'),  # PUT update transaction
    path('transactions/<str:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),  # DELETE transaction
    path('transactions/users/<str:user_id>/', TransactionsByUserView.as_view(), name='transactions-by-user'),  # GET transactions by user
    path('transactions/accounts/<str:account_id>/', TransactionsByAccountView.as_view(), name='transactions-by-account'),  # GET transactions by account

    # ===============
    # BUDGET ENDPOINTS
    # ===============
    path('budgets/', BudgetCreateView.as_view(), name='create-budget'),  # POST create budget
    path('budgets/users/<str:user_id>/', BudgetListByUserView.as_view(), name='list-budgets-by-user'),  # GET budgets by user
    path('budgets/accounts/<str:account_id>/', BudgetListByAccountView.as_view(), name='list-budgets-by-account'),  # GET budgets by account
    path('budgets/<str:pk>/', BudgetDetailView.as_view(), name='budget-detail'),  # GET, PUT, DELETE a specific budget
    path("budgets/noauth/<str:user_id>/", BudgetListByUserNoAuthView.as_view(), name="budgets-by-user-noauth"),
    # =============
    # GOAL ENDPOINTS
   
    # path("goals/", GoalListCreateAPIView.as_view(), name="goal-list-create"),
    # path("goals/<str:pk>/", GoalDetailAPIView.as_view(), name="goal-detail"),
    path("goals/", GoalAPIView.as_view(), name="goals"),
    path("goals/<str:pk>/", GoalAPIView.as_view(), name="goal-detail"),

    # =================
    # PORTFOLIO ENDPOINTS
    # =================
    path('portfolios/', PortfolioListCreateAPIView.as_view(), name='portfolio-list-create'),   # GET all / POST new
    path('portfolios/<str:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),      # GET, PUT, DELETE single 
    
    # =============
    # DEBT ENDPOINTS
    # =============
    # urls.py  (add under Goals block)
    path("debts/", DebtAPIView.as_view(), name="debt-list-create"),
    path("debts/<str:pk>/", DebtAPIView.as_view(), name="debt-detail"),
   
    # =========
    # REVIEWS
    # =========
    path('review/', ReviewView.as_view(), name='review'),  # POST or GET reviews

    # =========
    # CONTACT
    # =========
    path("contact/", ContactMessageView.as_view(), name="contact"),
    
    # --- ML ROUTES ---
    path('ml/predict-expense/<str:user_id>/', ExpensePredictionAPIView.as_view(), name='predict-expense'),
    path('ml/anomalies/run/<str:user_id>/', RunAnomalyDetectionAPIView.as_view(), name='run-anomalies'),
    path('ml/recurring/run/<str:user_id>/', RunRecurringDetectionAPIView.as_view(), name='run-recurring'),
    path('ml/goals/eta/<str:user_id>/', GoalETAPredictionAPIView.as_view(), name='goals-eta'),
    # ML - Anomalies & Recurring Patterns
    path('ml/anomalies/users/<str:user_id>/', AnomalyByUserAPIView.as_view(), name='anomalies-by-user'),
    path('ml/recurring/users/<str:user_id>/', RecurringByUserAPIView.as_view(), name='recurring-by-user'),

    
]
