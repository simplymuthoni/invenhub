# Inventory Management System

This project is an Inventory Management System built with a React frontend and a Flask backend. It allows users to manage clothing items, including adding, updating, deleting, and viewing items in the inventory. There are also user authentication features for registering, logging in, and managing user accounts.

## Features

- User Registration and Login
- Admin Login and Registration
- Add, Edit, and Delete Inventory Items
- View Inventory Items
- Change Password
- Reset Password

## Technologies Used

- **Frontend**: React, Axios, React Router DOM
- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (or any other database supported by SQLAlchemy)
- **Styling**: CSS

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   
Navigate to the backend directory:

bash

cd inventory-management-system/backend

Create a virtual environment:

bash

python -m venv venv

Activate the virtual environment:

    On Windows:

    bash

venv\Scripts\activate

On MacOS/Linux:

bash

    source venv/bin/activate

Install the dependencies:

bash

pip install -r requirements.txt

Set up the database:

bash

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

Run the Flask server:

bash

    flask run

Frontend

    Navigate to the frontend directory:

    bash

cd ../frontend

Install the dependencies:

bash

npm install

Start the React development server:

bash

    npm start

Usage

    Open your web browser and navigate to http://localhost:3000 to access the React frontend.
    Use the registration and login features to create an account and log in.
    Navigate to the inventory management section to add, edit, delete, and view clothing items.

Project Structure

arduino

inventory-management-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   ├── migrations/
│   ├── venv/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   ├── api.js
│   │   ├── components/
│   │   │   ├── AdminLogin.js
│   │   │   ├── AdminRegister.js
│   │   │   ├── Register.js
│   │   │   ├── LoginPage.js
│   │   │   ├── InventoryList.js
│   │   │   ├── AddItem.js
│   │   │   ├── EditItem.js
│   │   │   ├── ItemForm.js
│   │   │   ├── ItemList.js
│   │   │   ├── Login.js
│   │   │   ├── Logout.js
│   │   │   ├── ChangePassword.js
│   │   │   ├── ResetPassword.js
│   │   ├── App.js
│   │   ├── index.js
│   ├── package.json
└── README.md

API Endpoints
Item Management

    GET /items
        Description: Retrieve all items.
        Response: JSON array of items.

    POST /items
        Description: Add a new item.
        Request Body: JSON object with item details.
        Response: JSON object of the created item.

    PUT /items/
        Description: Update an existing item.
        Request Body: JSON object with updated item details.
        Response: JSON object of the updated item.

    DELETE /items/
        Description: Delete an existing item.
        Response: No content.

Authentication

    POST /register
        Description: Register a new user.
        Request Body: JSON object with user details.
        Response: JSON object of the registered user.

    POST /login
        Description: Login a user.
        Request Body: JSON object with user credentials.
        Response: JSON object with authentication token.
