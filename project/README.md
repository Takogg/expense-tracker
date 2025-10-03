# Expense Tracker Web Application

**Video Demo:** https://youtu.be/UTShH5HZHaw
## Description

The Expense Tracker is a comprehensive full-stack web application designed to help users manage their personal finances effectively. Built as the final project for CS50x 2025, this application demonstrates proficiency in web development, database management, user authentication, and data visualization. The application allows users to register, log in securely, track their expenses, view detailed statistics, and visualize spending patterns through interactive charts.

This project solves a real-world problem by helping people become more financially aware and make better spending decisions. Unlike simple expense calculators, this application provides persistent data storage, secure user accounts, and meaningful visual analytics that transform raw financial data into actionable insights.

## Features

- **Secure User Authentication**: Registration and login system with password hashing using Werkzeug
- **Expense Management**: Add, view, and delete expenses with detailed categorization
- **Data Visualization**: Interactive doughnut charts showing expense distribution by category
- **Real-time Statistics**: Display total expenses and monthly spending summaries
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Persistent Storage**: SQLite database ensures data is saved between sessions

## Technology Stack

**Backend:**
- Flask (Python web framework)
- SQLite (database)
- Werkzeug (password security)

**Frontend:**
- HTML5, CSS3, JavaScript
- Chart.js (data visualization)
- Responsive design without frameworks

## Project Structure

expense-tracker/
├── app.py # Flask backend with all routes and logic
├── requirements.txt # Python dependencies
├── templates/ # HTML templates
│ ├── index.html # Login/Register page
│ ├── dashboard.html # Main dashboard
│ └── add_expense.html # Add expense form
└── static/ # Static assets
├── css/styles.css # Complete styling
└── js/
├── auth.js # Authentication logic
├── expenses.js # Expense management
└── charts.js # Chart visualization


## Key Files Explanation

### app.py (Backend Core)
The main Flask application containing approximately 200 lines of code that handles:
- Database initialization with proper table relationships
- RESTful API endpoints for authentication and expense management
- Session-based user authentication for security
- Data validation and error handling
- Statistics calculation for dashboard insights

**Design Decision:** I chose session-based authentication over JWT tokens for simplicity and security in a traditional web application context. This approach keeps sensitive data server-side and provides better protection against client-side attacks.

### templates/index.html
The landing page featuring a clean, tab-based interface for both login and registration. Key features include:
- Dynamic form switching without page reloads
- Client-side form validation
- Real-time feedback for user actions
- Responsive design for mobile compatibility

**Design Decision:** I implemented tab switching with vanilla JavaScript rather than heavy frameworks to maintain fast loading times and simplicity.

### templates/dashboard.html
The main application interface where users spend most of their time. Features include:
- Statistics cards displaying key financial metrics
- Interactive Chart.js visualization showing expense distribution
- Complete expense listing with management capabilities
- Intuitive navigation and user controls

### static/css/styles.css
Comprehensive styling (400+ lines) providing:
- Modern gradient backgrounds for visual appeal
- Card-based layouts with subtle shadows
- Fully responsive design for all screen sizes
- Consistent color scheme focusing on trust and professionalism
- Smooth hover effects and transitions

**Design Decision:** I chose a purple/blue gradient color palette (#667eea, #764ba2) to convey trust and professionalism—essential qualities for a financial application.

### JavaScript Files
**auth.js:** Handles authentication using the Fetch API for smooth user experience without page reloads. Includes password confirmation validation and automatic redirection after successful operations.

**expenses.js:** Manages expense operations including loading, creating, and deleting expenses. Dynamically updates the interface and refreshes statistics when data changes.

**charts.js:** Dedicated to data visualization using Chart.js. Creates responsive doughnut charts that update dynamically with new data and handle edge cases gracefully.

## Database Design

The SQLite database contains two main tables:
- **users**: Stores user credentials with hashed passwords for security
- **expenses**: Links to users via foreign key, storing amount, category, date, and optional notes

**Security Consideration:** Passwords are hashed using Werkzeug's secure hashing algorithm, ensuring that even database compromise wouldn't expose user passwords.

## Installation and Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Navigate to `http://localhost:5000`
4. Register a new account or login with existing credentials
5. Start tracking your expenses and viewing analytics

## Design Philosophy

Every aspect of this application was designed with user experience in mind. The interface provides immediate feedback for all actions, uses confirmation dialogs for destructive operations, and maintains consistent visual language throughout. The backend follows RESTful principles, making it easily extensible for future enhancements like mobile applications.

The choice of technologies prioritized simplicity and educational value while maintaining professional standards. Flask provides flexibility without unnecessary complexity, SQLite offers zero-configuration persistence, and vanilla JavaScript keeps the frontend lightweight and maintainable.

## Future Enhancements

- Budget setting with spending alerts
- Recurring expense automation
- Data export functionality
- Income tracking capabilities
- Enhanced reporting and analytics
- Multi-currency support

---

**Author:** [Your Name]
**GitHub:** Takogg
**edX Username:** [Your edX Username]
**Location:** [Your City, Country]
**Date:** October 3, 2025

This project represents a complete full-stack web application demonstrating modern web development practices, secure coding principles, and user-centered design philosophy.
