# Sales Order Management System

A full-stack web application for managing sales orders, customers, and items with automatic tax calculations.

## Screenshots

### Home Page - Orders List
![Home Page](screenshots/ss1.png)

### Sales Order Form
![Sales Order Form](screenshots/ss2.png)

### Order Details
![Order Details](screenshots/ss3.png)

## Tech Stack

**Frontend:**
- React 19
- Redux Toolkit (State Management)
- React Router (Navigation)
- Tailwind CSS (Styling)
- Axios (API Communication)

**Backend:**
- Python 3.13
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- SQL Server (Database)
- Uvicorn (ASGI Server)

## Features

- Customer management with address details
- Item catalog with pricing
- Sales order creation and editing
- Automatic calculation of amounts (Excl, Tax, Incl)
- Sortable order listing
- Line item management with dual dropdowns (Item Code & Description)
- Print functionality

## Project Structure

```
sales-order-management/
├── backend/
│   ├── API/
│   │   ├── Controllers/      # REST API endpoints
│   │   └── Models/           # Pydantic DTOs
│   ├── Application/
│   │   ├── Interfaces/       # Repository interfaces
│   │   └── Services/         # Business logic
│   ├── Domain/
│   │   └── Entities/         # SQLAlchemy models
│   ├── Infrastructure/
│   │   ├── Data/             # Database connection
│   │   └── Repositories/     # Data access layer
│   ├── main.py
│   └── requirements.txt
└── frontend/
    └── src/
        ├── components/       # Reusable UI components
        ├── hooks/            # Custom React hooks
        ├── pages/            # Page components
        ├── redux/            # Redux store & slices
        ├── services/         # API communication
        └── utils/            # Helper functions
```

## Prerequisites

- Python 3.13+
- Node.js 18+
- SQL Server (Express or LocalDB)
- Git

## Database Setup

1. Open SQL Server Management Studio (SSMS)

2. Create database:
```sql
CREATE DATABASE SalesOrderDB;
```

3. Enable mixed mode authentication and create user:
```sql
CREATE LOGIN salesapp WITH PASSWORD = 'Password123';
USE SalesOrderDB;
CREATE USER salesapp FOR LOGIN salesapp;
ALTER ROLE db_owner ADD MEMBER salesapp;
```

4. Tables will be created automatically on first run

## Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Update connection string in `Infrastructure/Data/database.py` if needed:
```python
DATABASE_URL = "mssql+pyodbc://salesapp:Password123@localhost\\SQLEXPRESS/SalesOrderDB?driver=ODBC+Driver+17+for+SQL+Server"
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

API Documentation: `http://127.0.0.1:8000/docs`

### Start Frontend

```bash
cd frontend
npm start
```

Frontend runs on `http://localhost:3000`

## Usage

1. Navigate to `http://localhost:3000`
2. View existing sales orders on the home page
3. Click "Add New Order" to create a new order
4. Select customer from dropdown (addresses auto-fill)
5. Add line items:
   - Select item by Code or Description
   - Enter quantity and tax rate
   - Amounts calculate automatically
6. Click "Create Order" to save
7. Double-click any order to edit
8. Use "Print" button for printable view

## API Endpoints

**Customers:**
- `GET /api/customers/` - List all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers/` - Create customer

**Items:**
- `GET /api/items/` - List all items
- `GET /api/items/{id}` - Get item by ID
- `POST /api/items/` - Create item

**Orders:**
- `GET /api/orders/` - List all orders (with customer names)
- `GET /api/orders/{id}` - Get order with line items
- `POST /api/orders/` - Create order with calculations
- `PUT /api/orders/{id}` - Update order
- `DELETE /api/orders/{id}` - Delete order

## Calculations

Automatic calculations for each line item:
- **Excl Amount** = Quantity × Price
- **Tax Amount** = Excl Amount × (Tax Rate / 100)
- **Incl Amount** = Excl Amount + Tax Amount

Order totals are sum of all line items.

## Database Schema

**customers**
- id (PK), name, address1, address2, address3, suburb, state, post_code, created_at

**items**
- id (PK), item_code, description, price, created_at

**sales_orders**
- id (PK), invoice_no, invoice_date, customer_id (FK), reference_no, note
- total_excl, total_tax, total_incl, created_at, updated_at

**order_line_items**
- id (PK), order_id (FK), item_id (FK), quantity, price, tax_rate, note
- excl_amount, tax_amount, incl_amount

## Author

Developed for SPIL Labs Internship Assignment

## License

MIT
