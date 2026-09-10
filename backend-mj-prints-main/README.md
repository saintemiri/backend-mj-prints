# MJ Prints Sales Tracking

Integrated React + Vite frontend and Django REST backend for the MJ Prints sales
tracking system. Customer application data is stored in MongoDB. Django SQLite
data is still used for authentication tokens, admin, and Django migrations.

## Requirements

- Windows PowerShell
- Node.js and npm
- Python 3.12 recommended
- MongoDB Atlas database and database user

## Project folders

Run commands from the project root:

```text
C:\Users\pc2\Downloads\backend-mj-prints-main\backend-mj-prints-main
```

Important folders:

- `src/` - React customer, admin, and employee frontend
- `backend/` - Django REST API
- `.env` - local MongoDB configuration; never commit this file

## First-time setup

### 1. Create the Python environment

Open PowerShell in the project root:

```powershell
cd C:\Users\pc2\Downloads\backend-mj-prints-main\backend-mj-prints-main
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

If `python` points to the wrong installation, use the Python executable that has
Django installed, or install Python 3.12 and recreate `.venv`.

### 2. Configure MongoDB

Create a file named `.env` in the project root:

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@YOUR-CLUSTER.mongodb.net/?retryWrites=true&w=majority&authSource=admin
MONGO_DB_NAME=salestrackingsystem
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1your-twilio-number
```

Replace `USERNAME`, `PASSWORD`, and `YOUR-CLUSTER` with the values from MongoDB
Atlas. URL-encode special password characters such as `@`, `#`, `/`, or `:`.

In MongoDB Atlas, also check:

- Database Access contains the user and the password is correct.
- The user has read/write access to `salestrackingsystem`.
- Network Access allows your current IP address.

Do not commit `.env` or share its contents. If a password was exposed, rotate it
in MongoDB Atlas before using it again.

Customer login uses SMS verification when a new browser or device is detected.
Create a Twilio account and use a Twilio phone number for the three `TWILIO_*`
values above. The customer phone number must include its country code, such as
`+63...`.

### 3. Run Django migrations

```powershell
.\.venv\Scripts\python.exe backend\manage.py migrate
```

## Run the application

Use two terminals, both opened at the project root.

### Terminal 1: Django backend

```powershell
cd C:\Users\pc2\Downloads\backend-mj-prints-main\backend-mj-prints-main
.\.venv\Scripts\python.exe backend\manage.py check
.\.venv\Scripts\python.exe backend\manage.py runserver
```

Backend URL: `http://127.0.0.1:8000`

### Terminal 2: React frontend

```powershell
cd C:\Users\pc2\Downloads\backend-mj-prints-main\backend-mj-prints-main
npm.cmd install
npm.cmd run dev
```

Frontend URL: `http://localhost:5173`

The Vite development server proxies `/api` requests to Django on port 8000.

## Customer flow

1. Open `http://localhost:5173/customer/signup`.
2. Create a customer account.
3. Sign in after registration if needed.
4. Products and services are loaded from MongoDB `printingServices`.
5. New orders are saved to MongoDB `orders`.
6. Successful orders create records in `notifications_customers`.
7. Customer orders and notifications are filtered to the signed-in customer.
8. A new device requires a 4-digit SMS code. The code can be resent from the login screen.

## MongoDB collections

- `users` - customer accounts created through signup
- `customer_address` - saved delivery addresses for each customer
- `printingServices` - products and printing service items
- `orders` - customer order documents
- `notifications_customers` - customer order notifications
- `branches` - branch data when available
- `products` - currently unused by the customer printing-services flow

## Useful checks

```powershell
# Django configuration check
.\.venv\Scripts\python.exe backend\manage.py check

# Frontend production build
npm.cmd run build
```

## Troubleshooting

### `No module named django`

Use the project virtual environment explicitly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe backend\manage.py check
```

### `Request failed` on signup or order submission

Make sure both servers are running and restart Vite after changing
`vite.config.js`. The frontend uses Django at `http://127.0.0.1:8000` through the
Vite `/api` proxy.

### MongoDB authentication or DNS error

Check the URI in `.env`, reset the Atlas database-user password, allow your IP in
Atlas Network Access, and restart Django after editing `.env`.

### Old data is still visible

Clear the browser session and reload:

```js
localStorage.clear()
location.reload()
```

Para i-run
.\.venv\Scripts\python.exe backend\manage.py runserver