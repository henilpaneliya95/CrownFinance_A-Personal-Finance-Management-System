**CLASS DIAGRAM - CROWN FINANCE**

---

## **OVERVIEW**

The Crown Finance Class Diagram represents the complete object-oriented architecture of the financial management system. It defines 13 core classes that work together to provide a comprehensive platform for personal finance management, budgeting, goal tracking, and AI-powered financial insights.

### **Architecture Summary:**

**13 Core Classes** organized into three functional layers:

1. **User Management Layer:** User, UserProfile, Feedback
   - Handles user registration, authentication, profile management, and system feedback

2. **Financial Operations Layer:** Account, Transaction, Category, Payment, Budget, Goal
   - Manages financial accounts, transactions, categorization, payments, budget control, and goal tracking

3. **Analytics & Reporting Layer:** Dashboard, AIInsight, Report, Notification
   - Provides visual analytics, AI-driven recommendations, report generation, and real-time notifications

### **Key Design Principles:**

- **User-Centric Design:** All classes relate to the User class, which is the central entity
- **Modular Architecture:** Each class has specific responsibilities (SRP - Single Responsibility Principle)
- **Relationship-Based:** 1:1, 1:Many relationships define data flow and dependencies
- **Data Integrity:** Consistent status tracking, date management, and transaction validation
- **Extensibility:** Dashboard, Report, and AIInsight classes can be extended with new features

### **Class Relationships:**

| Relationship | Classes | Purpose |
|---|---|---|
| **1:1** | User ↔ Dashboard, UserProfile | One user has one dashboard and one profile |
| **1:Many** | User → Account, Transaction, Goal | One user can have multiple accounts, transactions, goals |
| **1:Many** | Account → Transaction, Budget | One account contains multiple transactions and budgets |
| **1:Many** | Transaction → Category | Transactions are classified into categories |
| **1:Many** | User → Notification, AIInsight, Report | One user receives multiple notifications and insights |

### **Data Flow:**

```
User Registration
    ↓
User Creates Account → Account stores balance
    ↓
User adds Transaction → Transaction categorized & tracked
    ↓
Dashboard aggregates data → Analytics generated
    ↓
Budget & Goal status checked → Notifications sent
    ↓
AIInsight analyzes patterns → Recommendations provided
    ↓
Report generated → User feedback collected
```

---

**Class Descriptions:**

**1. User**
• **Attributes:** user_id, email_id, password, fullname, contactno, address, status, registrationdate, lastlogindate
• **Methods:** registerUser(), login(), updateProfile(), changePassword(), logout()
• **Description:** This class represents users/customers who can register, log in, manage their financial data, and access Crown Finance features.

---

**2. Account**
• **Attributes:** account_id, user_id, accounttype, accountname, balance, currency, createddate, status
• **Methods:** createAccount(), getBalance(), updateBalance(), viewAccountDetails()
• **Description:** Represents user financial accounts (Savings, Checking, Investment) where transactions are tracked and balance is maintained.

---

**3. Transaction**
• **Attributes:** transaction_id, account_id, user_id, transactiontype, amount, category_id, description, transactiondate, status
• **Methods:** addTransaction(), editTransaction(), deleteTransaction(), getTransactionHistory(), calculateTotal()
• **Description:** Handles all financial transactions (income/expense) linked to accounts with categorization and date tracking.

---

**4. Category**
• **Attributes:** category_id, categoryname, categorytype, icon, description, status
• **Methods:** addCategory(), viewCategory(), editCategory(), deleteCategory()
• **Description:** Defines expense/income categories (Food, Transport, Salary, Bonus, etc.) used for transaction classification.

---

**5. Budget**
• **Attributes:** budget_id, user_id, category_id, budgetlimit, startdate, enddate, spent_amount, status
• **Methods:** createBudget(), updateBudget(), checkBudgetStatus(), generateAlert()
• **Description:** Manages budget limits set by users for different expense categories with spending tracking.

---

**6. Goal**
• **Attributes:** goal_id, user_id, goalname, targetamount, currentamount, startdate, targetdate, status
• **Methods:** createGoal(), updateGoalProgress(), checkGoalStatus(), completeGoal()
• **Description:** Tracks user financial goals (Savings, Investment, Debt Payoff) with progress monitoring and timeline.

---

**7. Dashboard**
• **Attributes:** dashboard_id, user_id, totalincome, totalexpense, netbalance, last_updated
• **Methods:** generateAnalytics(), getSummary(), getCharts(), refreshDashboard()
• **Description:** Provides comprehensive financial overview with analytics, charts, and summaries for user's financial health.

---

**8. Payment**
• **Attributes:** payment_id, user_id, paymentmethod, cardno, expirydate, cvv, cardholder, status
• **Methods:** addPaymentMethod(), removePaymentMethod(), validatePayment(), processPayment()
• **Description:** Manages payment methods and payment-related details for transactions and bill payments.

---

**9. Notification**
• **Attributes:** notification_id, user_id, notificationtype, message, createddate, readstatus, priority
• **Methods:** sendNotification(), markAsRead(), deleteNotification(), getNotifications()
• **Description:** Generates and manages budget alerts, goal milestones, spending warnings, and system notifications.

---

**10. AIInsight**
• **Attributes:** insight_id, user_id, insighttype, description, recommendation, confidencescore, createddate
• **Methods:** generateInsight(), analyzeSpending(), predictTrend(), getSuggestions()
• **Description:** Provides AI-powered financial insights, spending analysis, recommendations, and predictive analytics.

---

**11. Report**
• **Attributes:** report_id, user_id, reporttype, startdate, enddate, generateddate, fileformat, status
• **Methods:** generateReport(), exportReport(), viewReport(), downloadReport()
• **Description:** Generates financial reports (monthly, yearly, category-wise) for user analysis and record-keeping.

---

**12. UserProfile**
• **Attributes:** profile_id, user_id, firstname, lastname, profilepic, phoneno, address, city, country, pincode, status
• **Methods:** updateProfile(), uploadProfilePic(), viewProfile(), deleteAccount()
• **Description:** Manages detailed user profile information and personal preferences for the Crown Finance application.

---

**13. Feedback**
• **Attributes:** feedback_id, user_id, feedbacktype, message, rating, createddate, status
• **Methods:** submitFeedback(), rateFeedback(), viewFeedback(), respondToFeedback()
• **Description:** Captures user feedback, suggestions, and ratings for Crown Finance system improvement and customer satisfaction.
