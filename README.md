# 🛒 SabzShop

**A Django-based E-commerce Web Application**

SabzShop is a full-featured e-commerce web application developed with Python and Django as a backend portfolio project.

The project focuses on implementing common e-commerce workflows, including product management, shopping cart, order processing, user authentication, discount management, and wallet transactions.

## ✨ Features

### 🛍️ Product Management
- Product listing and detailed product pages
- Product categories and inventory management
- Product search and filtering
- Price-based sorting
- Latest, best-selling, cheapest, and discounted products
- Product reviews and ratings
- Save and manage favorite products

### 🛒 Shopping Cart
- Session-based shopping cart
- Add and remove products
- Update product quantities
- Automatic cart total calculation
- Shipping cost calculation based on product weight

### 👤 User Management
- Custom Django user model
- User registration and authentication
- Login and logout
- Password change and reset
- User address management

### 📦 Order Management
- Order creation and order history
- Order details and status tracking
- Inventory updates during order processing
- Order return requests
- PDF invoice generation

### 💳 Wallet System
- Individual wallet for each user
- Wallet recharge functionality
- Wallet balance management
- Wallet transaction history
- Purchasing with wallet balance

### 🎟️ Discount Management
- Discount code creation and validation
- Percentage-based discounts
- Discount usage tracking
- Restrictions on repeated discount usage

### ⭐ Reviews and Ratings
- Product comments
- User-based product ratings
- Average product rating calculation
- One review per user for each product
- Admin-controlled comment approval

### ⚙️ Administration
- Customized Django Admin
- Product and category management
- Order and return request management
- User and wallet management
- Discount code management
- Order data export

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Backend programming |
| Django 6.1 | Web framework |
| PostgreSQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side interactions |
| ReportLab | PDF invoice generation |
| Pillow | Image processing |
| django-jalali | Jalali date support |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
sabzshop/
│
├── account/              # User accounts and wallet
│
├── cart/                 # Shopping cart functionality
│
├── orders/               # Orders, payments and returns
│
├── shop/                 # Products, reviews and discounts
│
├── sabzshop/             # Main Django configuration
│
├── images/               # Uploaded product images
│
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AmirHossein-1385/shop.git
cd shop
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the example file.

On Windows:

```bash
copy .env.example .env
```

Update the `.env` file with your own configuration, including:

- Django secret key
- PostgreSQL database credentials
- Email credentials

### 5. Configure PostgreSQL

Create a PostgreSQL database and configure its credentials in your `.env` file.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## 🔐 Environment Variables

The application uses environment variables to manage sensitive configuration.

The `.env.example` file contains the required variable names and example values.

Never commit your actual `.env` file or sensitive credentials to version control.

## ⚠️ Project Notes

- This project is developed for educational and portfolio purposes.
- The payment workflow uses a sandbox/demo implementation and does not process real payments.
- SMS verification is not connected to a live SMS provider.
- PostgreSQL must be configured locally before running the application.
- External services require their own credentials and configuration.

## 👨‍💻 Developer

**AmirHossein Taghipour**

Junior Python Backend Developer

[GitHub Profile](https://github.com/AmirHossein-1385)

---
