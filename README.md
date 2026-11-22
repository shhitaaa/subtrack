# SubTrack

A Flask + MySQL subscription management application developed in four iterations (four completed so far).

## Setup (Windows)

1. Install Python 3.11+ and MySQL Server.
2. Open a terminal in this folder:
   ```bash
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a MySQL database:
   ```sql
   CREATE DATABASE subtrack;
   ```
4. Copy `.env.example` to `.env` and enter your MySQL credentials.
5. Run the schema:
   ```bash
   mysql -u root -p subtrack < schema.sql
   ```
6. Start the app:
   ```bash
   python app.py
   ```
7. Open http://127.0.0.1:5000

## Iterations

- `iterations/sprint1.py`: authentication, subscription CRUD, basic dashboard.
- `iterations/sprint2.py`: billing cycle logic, renewal calculations and reminders.
- `iterations/sprint3.py`: budgets, analytics, savings simulation, price history and shared groups.
- `iterations/sprint4.py`: overlap detection, notifications and settlement helpers.

The main application imports these modules. This keeps the sprint implementations separate while producing one integrated application.

## Notes

- This project tracks subscriptions entered by the user. It does not connect to Netflix, Spotify, banks or payment gateways.
- Reminders are displayed in the application; email/SMS delivery is not configured.
- Savings suggestions are simulations. The app does not cancel subscriptions.
- Shared-cost settlement records who owes what; it does not transfer money.
- For a classroom project, use test accounts and do not store real payment credentials.
- Never commit your `.env` file. Copy `.env.example` and fill in your own values locally.