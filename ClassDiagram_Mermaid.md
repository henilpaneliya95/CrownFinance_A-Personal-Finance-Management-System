classDiagram
    class User {
        -int user_id
        -string email_id
        -string password
        -string fullname
        -string contactno
        -string address
        -string status
        -datetime registrationdate
        -datetime lastlogindate
        +login()
        +registerUser()
        +updateProfile()
        +changePassword()
        +logout()
    }

    class Account {
        -int account_id
        -int user_id
        -enum accounttype
        -string accountname
        -float balance
        -string currency
        -datetime createddate
        -string status
        +createAccount()
        +getBalance()
        +updateBalance()
        +viewAccountDetails()
    }

    class Transaction {
        -int transaction_id
        -int account_id
        -int user_id
        -string transactiontype
        -float amount
        -int category_id
        -string description
        -datetime transactiondate
        -string status
        +addTransaction()
        +editTransaction()
        +deleteTransaction()
        +getTransactionHistory()
        +calculateTotal()
    }

    class Category {
        -int category_id
        -string categoryname
        -string categorytype
        -string icon
        -string description
        -string status
        +addCategory()
        +viewCategory()
        +editCategory()
        +deleteCategory()
    }

    class Budget {
        -int budget_id
        -int user_id
        -int category_id
        -float budgetlimit
        -date startdate
        -date enddate
        -float spent_amount
        -string status
        +createBudget()
        +updateBudget()
        +checkBudgetStatus()
        +generateAlert()
    }

    class Goal {
        -int goal_id
        -int user_id
        -string goalname
        -float targetamount
        -float currentamount
        -date startdate
        -date targetdate
        -string status
        +createGoal()
        +updateGoalProgress()
        +checkGoalStatus()
        +completeGoal()
    }

    class Dashboard {
        -int dashboard_id
        -int user_id
        -float totalincome
        -float totalexpense
        -float netbalance
        -datetime last_updated
        +generateAnalytics()
        +getSummary()
        +getCharts()
        +refreshDashboard()
    }

    class Payment {
        -int payment_id
        -int user_id
        -string paymentmethod
        -string cardno
        -date expirydate
        -string cvv
        -string cardholder
        -string status
        +addPaymentMethod()
        +removePaymentMethod()
        +validatePayment()
        +processPayment()
    }

    class Notification {
        -int notification_id
        -int user_id
        -string notificationtype
        -string message
        -datetime createddate
        -boolean readstatus
        -string priority
        +sendNotification()
        +markAsRead()
        +deleteNotification()
        +getNotifications()
    }

    class AIInsight {
        -int insight_id
        -int user_id
        -string insighttype
        -string description
        -string recommendation
        -float confidencescore
        -datetime createddate
        +generateInsight()
        +analyzeSpending()
        +predictTrend()
        +getSuggestions()
    }

    class Report {
        -int report_id
        -int user_id
        -string reporttype
        -date startdate
        -date enddate
        -datetime generateddate
        -string fileformat
        -string status
        +generateReport()
        +exportReport()
        +viewReport()
        +downloadReport()
    }

    class UserProfile {
        -int profile_id
        -int user_id
        -string firstname
        -string lastname
        -string profilepic
        -string phoneno
        -string address
        -string city
        -string country
        -string pincode
        -string status
        +updateProfile()
        +uploadProfilePic()
        +viewProfile()
        +deleteAccount()
    }

    class Feedback {
        -int feedback_id
        -int user_id
        -string feedbacktype
        -string message
        -int rating
        -datetime createddate
        -string status
        +submitFeedback()
        +rateFeedback()
        +viewFeedback()
        +respondToFeedback()
    }

    User "1" -- "*" Account : owns
    User "1" -- "*" Transaction : creates
    User "1" -- "*" Budget : sets
    User "1" -- "*" Goal : creates
    User "1" -- "1" Dashboard : has
    User "1" -- "*" Payment : uses
    User "1" -- "*" Notification : receives
    User "1" -- "*" AIInsight : receives
    User "1" -- "*" Report : generates
    User "1" -- "1" UserProfile : maintains
    User "1" -- "*" Feedback : provides
    Account "1" -- "*" Transaction : contains
    Account "1" -- "*" Budget : linked_to
    Category "1" -- "*" Transaction : classifies
    Category "1" -- "*" Budget : applies_to
    Dashboard --> Transaction : displays
    Dashboard --> Account : shows
    Dashboard --> Budget : monitors
    Report --> Transaction : analyzes
    Report --> Account : summarizes
    Report --> Goal : tracks
