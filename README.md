# SabzShop 🛒

A Django-based e-commerce web application developed as a backend portfolio project.

SabzShop provides essential online shopping features, including product management, shopping cart, order processing, user accounts, discount codes, and wallet management.

## ✨ Features

### 🛍️ Product Management
- Product listing and detail pages
- Product categories
- Product search and filtering
- Product sorting
- Latest, best-selling, cheapest, and discounted products
- Product reviews and ratings
- Saved products

### 🛒 Shopping Cart
- Session-based shopping cart
- Add and remove products
- Update product quantities
- Automatic price calculation
- Shipping cost calculation based on product weight

### 👤 User Accounts
- Custom user model
- User registration and authentication
- Login and logout
- Password change and reset
- User address management

### 📦 Order Management
- Order creation and order history
- Order status tracking
- Order details
- PDF invoice generation
- Return request management
- Inventory management

### 💳 Wallet System
- Individual wallet for each user
- Wallet recharge
- Wallet transactions
- Payment using wallet balance

### 🎟️ Discount System
- Discount codes
- Discount validation
- Discount usage tracking
- User-specific discount usage restrictions

### ⚙️ Administration
- Customized Django Admin
- Product and category management
- Order management
- User and wallet management
- Discount code management
- Return request management

## 🧰 Tech Stack

- **Language:** Python
- **Framework:** Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS
- **PDF Generation:** ReportLab
- **Image Processing:** Pillow
- **Version Control:** Git & GitHub

## 📁 Project Structure

```text
sabzshop/
│
├── account/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
│
├── cart/
│   ├── cart.py
│   ├── views.py
│   └── ...
│
├── orders/
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── views.py
│   └── ...
│
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── filters.py
│   ├── signals.py
│   └── ...
│
├── sabzshop/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── images/
├── manage.py
├── requirements.txt
└── .env.example
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/AmirHossein-1385/shop.git
cd shop
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Set your Django secret key, database credentials, and email configuration.

### 5. Configure PostgreSQL

Create a PostgreSQL database and update the database settings in your `.env` file.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## ⚠️ Important Notes

- This project is developed for educational and portfolio purposes.
- The payment workflow currently uses a sandbox/demo implementation and does not process real payments.
- External services such as email require valid configuration.
- Do not commit your `.env` file or other sensitive credentials to GitHub.

## 👨‍💻 Developer

**AmirHossein Taghipour**

Junior Python Backend Developer

GitHub: [AmirHossein-1385](https://github.com/AmirHossein-1385)
