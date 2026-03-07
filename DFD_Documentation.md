# DATA FLOW DIAGRAMS - CROWN FINANCE

## • Data Flow Diagram:

A data flow diagram is a graphical representation of the flow of data through an information system. A data flow diagram can also be used for the visualization of the data processing. It is common practice for a designer to draw a context level DFD. It shows the interaction between the Crown Finance system and external entities such as users, administrators, AI recommendation engine, and database server. This context level DFD is then exploded to show more detail of the system being modelled.

A DFD represents flow of data through the Crown Finance system. Data flow diagrams are commonly used during problem analysis. It views the system as a function that transforms financial inputs (user registration, transaction entries, budget goals) into the desired output (dashboard analytics, AI insights, financial reports). A DFD shows movement of data through different transformations or processes in the Crown Finance system such as authentication, transaction tracking, budget calculation, expense analysis, and AI-based recommendation generation.

Data Flow diagrams can be used to provide the end users with a physical idea of where the data they input ultimately has an effect upon the structure of the whole system—from user registration to transaction logging, from expense categorization to budget monitoring, from goal tracking to AI insight generation. How the Crown Finance system is developed can be determined through data flow diagram. The appropriate financial records are saved in the database (SQLite/MongoDB) and maintained by appropriate authorities (Admin users). User transaction data flows through validation processes, gets stored securely, and is then retrieved for analytics, visualization, and AI-powered financial recommendations, ensuring seamless financial management experience.

---

## • DFD LEVEL-0 (Context Level Diagram):

**Image Reference:** `image/dfd_level_0.png`

DFD Level-0 represents the highest level of abstraction for the Crown Finance system. It shows the entire system as a single process bubble (Process 0) and illustrates its interactions with external entities.

**External Entities:**
- **User:** Primary actor who interacts with the system to manage personal finances
- **Admin:** System administrator responsible for management and monitoring
- **AI/ML Engine:** External analytical component providing intelligent insights

**Process:**
- **Process 0 - Crown Finance System:** The complete financial management application

**Data Store:**
- **D1 - Financial Database:** Central repository storing all user data, transactions, budgets, and goals

**Data Flows:**
1. User → System: User requests (login, add transactions, view reports, set budgets)
2. System → User: Reports and insights (dashboard, analytics, recommendations)
3. Admin → System: Admin commands (user management, system configuration)
4. System → Admin: System reports (activity logs, performance metrics)
5. AI/ML Engine → System: AI predictions (spending patterns, recommendations)
6. System → AI/ML Engine: Data for analysis (transaction history, user behavior)
7. System ↔ Financial Database: Store and retrieve financial data

---

## • DFD LEVEL-1 (System Decomposition):

**Image Reference:** `image/dfd_level_1.png`

DFD Level-1 breaks down the Crown Finance system (Process 0) into its major subsystems or modules. Each process represents a major functional component of the application.

**External Entities:**
- **User:** End user accessing the financial management features
- **Admin:** Administrator managing the system

**Major Processes:**
- **Process 1 - User Authentication:** Handles user login, signup, and session management
- **Process 2 - Transaction Management:** Manages income and expense transactions
- **Process 3 - Budget & Goals:** Handles budget planning and financial goal tracking
- **Process 4 - Analytics Engine:** Processes data to generate reports and visualizations
- **Process 5 - AI Insight Generator:** Produces personalized financial recommendations

**Data Stores:**
- **D1 - User Accounts:** Stores user credentials, profiles, and authentication tokens
- **D2 - Transactions:** Repository of all financial transactions (income/expense)
- **D3 - Budgets/Goals:** Stores budget limits and financial goal targets
- **D4 - Analytics Data:** Processed data for dashboard and reporting

**Key Data Flows:**
1. User → Process 1: Login/Signup requests
2. Process 1 → Process 2: Authentication token for authorized transactions
3. Process 2 ↔ D2: Store and retrieve transaction records
4. Process 3 ↔ D3: Manage budget and goal data
5. Process 4 → D4: Store computed analytics
6. Process 2 → Process 5: Transaction data for AI analysis
7. Process 5 → User: AI-generated financial insights
8. Admin → Multiple Processes: Administrative access and monitoring

---

## • DFD LEVEL-2.1 (User Authentication Module):

**Image Reference:** `image/dfd_level_2_1.png`

DFD Level-2.1 provides detailed decomposition of the User Authentication module (Process 1 from Level-1).

**External Entity:**
- **User:** Person attempting to access the Crown Finance system

**Sub-Processes:**
- **Process 1.1 - Validate Credentials:** Verifies username and password against stored records
- **Process 1.2 - Generate JWT Token:** Creates secure authentication tokens for valid users
- **Process 1.3 - Create New Account:** Registers new users in the system
- **Process 1.4 - Update Profile:** Allows users to modify their account information

**Data Store:**
- **D1 - User Database:** Stores all user account information including credentials and profiles

**Data Flows:**
1. User → Process 1.1: Login request with credentials
2. Process 1.1 ↔ D1: Read user data for validation
3. Process 1.1 → Process 1.2: Valid user confirmation
4. Process 1.2 → User: JWT authentication token
5. User → Process 1.3: Signup data (new registration)
6. Process 1.3 → D1: Store new user account details
7. User → Process 1.4: Profile update request
8. Process 1.4 ↔ D1: Read and update user information

**Process Description:**
When a user attempts to log in, their credentials are validated against the User Database. Upon successful validation, a JWT token is generated and returned to the user for subsequent authenticated requests. New users can register through the Create New Account process, which stores their information securely. Existing users can update their profile information, which is then reflected in the User Database.

---

## • DFD LEVEL-2.2 (Transaction Management Module):

**Image Reference:** `image/dfd_level_2_2.png`

DFD Level-2.2 details the Transaction Management module (Process 2 from Level-1), which handles all financial transaction operations.

**External Entity:**
- **User:** The person managing their financial transactions

**Sub-Processes:**
- **Process 2.1 - Add/Edit Transaction:** Enables users to create or modify transaction records
- **Process 2.2 - Categorize Expense:** Automatically or manually assigns categories to transactions
- **Process 2.3 - Calculate Totals:** Computes summaries (daily, weekly, monthly totals)
- **Process 2.4 - Filter & Search:** Allows users to query and filter transaction history
- **Process 2.5 - Export Data:** Generates downloadable reports in various formats

**Data Stores:**
- **D2 - Transaction Database:** Primary storage for all transaction records
- **D5 - Category Master:** Reference table containing expense/income categories

**Data Flows:**
1. User → Process 2.1: New transaction details or edit request
2. Process 2.1 → Process 2.2: Raw transaction data
3. Process 2.2 ↔ D5: Retrieve available categories
4. Process 2.2 → D2: Store categorized transaction
5. Process 2.3 ↔ D2: Read transactions for calculation
6. Process 2.3 → User: Summary reports (totals, averages)
7. User → Process 2.4: Search/filter criteria
8. Process 2.4 ↔ D2: Query transaction records
9. Process 2.4 → Process 2.5: Filtered data for export
10. Process 2.5 → User: Exported transaction report

**Process Description:**
Users add transactions which are then categorized (e.g., Food, Transport, Salary, etc.) using predefined categories from the Category Master. The system calculates running totals and provides summary analytics. Users can search their transaction history using various filters and export the data for external use or record-keeping.

---

## • DFD LEVEL-2.3 (Budget & Goals Management Module):

**Image Reference:** `image/dfd_level_2_3.png`

DFD Level-2.3 details the Budget & Goals module (Process 3 from Level-1), focusing on financial planning and goal tracking features.

**External Entity:**
- **User:** Individual setting financial budgets and goals

**Sub-Processes:**
- **Process 3.1 - Set Budget Limits:** Allows users to define spending limits for categories
- **Process 3.2 - Track Spending:** Monitors actual spending against budget limits
- **Process 3.3 - Calculate Progress:** Computes budget utilization and goal achievement percentages
- **Process 3.4 - Set Financial Goals:** Enables users to define savings or financial targets
- **Process 3.5 - Monitor Goals:** Tracks progress toward achieving financial goals

**Data Stores:**
- **D3 - Budget Database:** Stores budget limits and configurations
- **D6 - Goals Database:** Contains user-defined financial goals and targets
- **D2 - Transaction Data:** Reference to actual spending data

**Data Flows:**
1. User → Process 3.1: Budget limit inputs (monthly/category-wise)
2. Process 3.1 → D3: Store budget configurations
3. Process 3.2 ↔ D3: Read budget limits
4. Process 3.2 ↔ D2: Read actual transaction/spending data
5. Process 3.3 → Process 3.2: Spending analysis request
6. Process 3.3 → User: Budget alerts and reports (overspending warnings)
7. User → Process 3.4: Goal details (target amount, timeline)
8. Process 3.4 → D6: Store goal information
9. Process 3.5 ↔ D6: Read goal targets
10. Process 3.5 ↔ D2: Read savings/income data
11. Process 3.5 → User: Goal progress reports and achievement status

**Process Description:**
Users define budget limits for various expense categories. The system continuously tracks actual spending by referencing the Transaction Database and comparing it against set budgets. When spending approaches or exceeds limits, alerts are generated. Similarly, users can set financial goals (e.g., "Save $5000 in 6 months"), and the system monitors progress by analyzing income, expenses, and savings patterns, providing regular updates and motivation.

---

## Summary of DFD Hierarchy:

- **Level-0:** Overall system context showing Crown Finance as a single process
- **Level-1:** Decomposition into 5 major modules (Authentication, Transactions, Budget/Goals, Analytics, AI Insights)
- **Level-2.1:** Detailed view of Authentication (Login, Token Generation, Registration, Profile Update)
- **Level-2.2:** Detailed view of Transaction Management (CRUD operations, Categorization, Reporting)
- **Level-2.3:** Detailed view of Budget & Goals (Budget Setting, Spending Tracking, Goal Monitoring)

Each level progressively reveals more implementation details while maintaining logical consistency across all diagrams.

---

**All diagram images are available in the `image/` folder.**
