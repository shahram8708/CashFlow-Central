# CashFlow Central

CashFlow Central is a Flask-based web application designed to help users manage their expenses, set budgets, and track savings goals. Users can register an account, log in securely, add expenses with details such as item, amount, and date, set monthly budgets, and specify savings goals. The application provides visual feedback through dynamically generated plots to visualize expense trends over time.

### Features

- **User Authentication and Authorization**
  - Users can register and log in securely.
  - Passwords are hashed using bcrypt for security.
  - Sessions are managed using Flask-Login for seamless user experience.

- **Expense Management**
  - Users can add expenses including item description, amount, and date.
  - Expenses are associated with each user to maintain privacy and personalized tracking.

- **Budgeting and Savings Goals**
  - Users can set a monthly budget and savings goal.
  - Real-time updates reflect changes in the budget and savings goals upon submission.

- **Visualization**
  - Expenses are plotted over time using Matplotlib.
  - Each user has their own personalized expense plot displayed in the dashboard.

### Technologies Used

- **Flask**: Micro web framework for Python.
- **Flask SQLAlchemy**: ORM for database operations.
- **Flask-Bcrypt**: Hashing utility for passwords.
- **Flask-Login**: Authentication management.
- **Flask-WTF**: Integration for web forms.
- **Matplotlib**: Plotting library for visualizing expense trends.
- **Bootstrap**: Front-end framework for responsive design.
- **SQLite**: Lightweight relational database for data storage.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd cashflow-central
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```
   The application will run on `http://localhost:5000`.

4. **Access the Application**
   Open a web browser and go to `http://localhost:5000` to use the application.

### Folder Structure

```
cashflow-central/
│
├── static/             (Static files like CSS and images)
├── templates/          (HTML templates)
├── app.py              (Main application script)
├── README.md           (Documentation)
└── requirements.txt    (Dependencies)
```

### Contributors

- [Shah Ram](https://github.com/shahram8708) - Developer

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
