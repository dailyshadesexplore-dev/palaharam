# Palaharam

A South-Indian breakfast ordering web app. Customers browse a menu, add items to a cart, and place an order for **delivery** or **pickup** as a guest. Orders are stored in a local SQLite database through a FastAPI backend.

The repository is a monorepo with two independent apps:

```
Palaharam/
├── palaharam_BE/          # Backend — Python / FastAPI / SQLAlchemy / SQLite
│   ├── main.py            # FastAPI app entry point (CORS + router registration)
│   ├── routes/
│   │   └── routes.py      # All API endpoints
│   ├── db/
│   │   ├── database.py    # SQLAlchemy engine, SessionLocal, Base
│   │   ├── models.py      # ORM models: User, Order, Guest
│   │   └── schema.py      # Pydantic request schemas
│   ├── dbConfig/
│   │   ├── config.py      # Builds the SQLite connection URL
│   │   └── Palaharam.db   # The ACTIVE SQLite database file
│   ├── sqlite/
│   │   ├── palaharam.db   # Old/scratch DB (not used by the app)
│   │   └── scripts.sql    # Hand-written SQL used during early development (reference only)
│   └── requirements.txt   # Currently empty — see "Backend setup" for actual deps
│
└── palaharam_FE/          # Frontend — Next.js 15 (App Router) / React 19 / Tailwind 4
    ├── public/
    │   ├── data/sample.json   # STATIC menu data (name, description, image, price)
    │   └── Images/            # All menu/UI images
    └── src/app/
        ├── page.js            # Home: animated splash screen → renders Menu
        ├── menu/page.js       # Menu list + cart (quantity counters)
        ├── checkOut/page.js   # Checkout form + order summary, POSTs to backend
        └── checkOutFormAct/Page.js  # Order-confirmation overlay
```

---

## Backend (`palaharam_BE`)

### How it works

- [main.py](palaharam_BE/main.py) creates the FastAPI app, registers the router from [routes/routes.py](palaharam_BE/routes/routes.py), and adds CORS middleware allowing `http://localhost:3000` / `http://127.0.0.1:3000` (the Next.js dev server) plus a placeholder production domain.
- Importing `routes.py` runs `models.Base.metadata.create_all(bind=database.engine)`, so **all tables are created automatically on startup** if they don't exist — no migration tool is used (no Alembic).
- Each request gets a DB session via the `get_db()` dependency (`Depends(get_db)`), which opens a `SessionLocal` and closes it after the response.
- Request bodies are validated with the Pydantic models in [db/schema.py](palaharam_BE/db/schema.py).

### API routes

All routes are defined in [routes/routes.py](palaharam_BE/routes/routes.py), mounted at the root (no `/api` prefix).

| Method | Path | Body schema | What it does |
|--------|------|-------------|--------------|
| GET | `/` | — | Health check, returns `{"status": "API is running"}` |
| POST | `/guest_address` | `schema.guest_Address` | **The main order endpoint used by the frontend.** Saves a guest checkout (name, address, contact, delivery/payment mode, cart JSON, total) as a row in the `guests` table. Returns `{"message": "Order placed successfully", "id": <guest id>}` |
| POST | `/users/` | `schema.UserDetails` | Creates a registered user (rejects duplicate emails). Not currently called by the frontend. |
| POST | `/orders/` | `schema.OrderDetails` | Creates an order linked to an existing user (looked up by email). Not currently called by the frontend. |
| POST | `/PickUp_Orders` | raw JSON | Legacy Firestore endpoint. The Firestore client is commented out, so it just echoes the payload back with a "Firestore not configured" message. |

Notes on `/guest_address`:
- `Mobile_Number` arrives as a string and is converted to `int`; if conversion fails it is stored as `NULL`.
- `order_Details` (the cart array) is serialized with `json.dumps()` and stored as a string.
- Any DB failure returns HTTP 400 with the error detail.

### Database — what and how it's configured

- **Engine:** SQLite, accessed through SQLAlchemy ORM.
- **Location:** [dbConfig/config.py](palaharam_BE/dbConfig/config.py) builds the URL as `sqlite:///<repo>/palaharam_BE/dbConfig/Palaharam.db` — so the live database file is **`palaharam_BE/dbConfig/Palaharam.db`**. (The file in `palaharam_BE/sqlite/` is an older scratch copy and is not read by the app.)
- **Engine setup:** [db/database.py](palaharam_BE/db/database.py) creates the engine with `check_same_thread=False` (required for SQLite + FastAPI's threaded request handling), a `sessionmaker`, and the declarative `Base`.
- **Tables** ([db/models.py](palaharam_BE/db/models.py)):
  - `users` — id, firstName, lastName, address, mobileNumber (unique), email (unique), password (plain text — see Known issues), state, zipCode, created_at
  - `orders` — id, userId (FK → users.id), order_details (JSON string), delivery_mode, total_amount, order_date. One-to-many relationship: `User.orders` ↔ `Order.user`.
  - `guests` — id, firstName, lastName, address, mobileNumber, email, state, zipCode, orderDetails (JSON string), deliveryMode, Payment_Mode, totalAmount, created_at. **This is the table guest checkouts from the frontend land in.**
- [sqlite/scripts.sql](palaharam_BE/sqlite/scripts.sql) contains the original hand-written CREATE/INSERT/SELECT statements from early development, including a handy query to list today's orders joined with user info. Reference only — the ORM owns the schema now.

### Environment variables

`palaharam_BE/.env` defines `GOOGLE_APPLICATION_CREDENTIALS` (path to a Firebase/Firestore service-account JSON). It is only relevant to the disabled `/PickUp_Orders` Firestore path — the app runs fine without it. **Never commit real credential files.**

### Backend setup & run

`requirements.txt` is currently empty; install the actual dependencies manually:

```bash
cd palaharam_BE
python3 -m venv venv
source venv/bin/activate
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic python-dotenv

# Run the server (the __main__ block in main.py uses reload, which needs the import-string form):
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API is now at `http://127.0.0.1:8000` (interactive docs at `http://127.0.0.1:8000/docs`). Tables are auto-created on first start.

---

## Frontend (`palaharam_FE`)

Next.js 15 App Router project. All pages are client components (`'use client'`). Styling is Tailwind CSS 4 plus custom [globals.css](palaharam_FE/src/app/globals.css) / [mobile.css](palaharam_FE/src/app/mobile.css). Animations use the AOS library. HTTP calls use axios.

### Page flow

1. **`/` — Splash + menu** ([src/app/page.js](palaharam_FE/src/app/page.js)): shows an animated splash screen (tea kettle + logo) for 5 seconds, then renders the Menu component in place.
2. **Menu** ([src/app/menu/page.js](palaharam_FE/src/app/menu/page.js)): lists the menu items with +/- quantity counters. Cart is plain React state — an array of `{ item, count, value }`. The floating Checkout button links to `/checkOut`, **passing the cart as a URL query parameter** (`?cart=<encoded JSON>`). There is no global state store or localStorage — the query string is the only way cart data reaches checkout.
3. **`/checkOut`** ([src/app/checkOut/page.js](palaharam_FE/src/app/checkOut/page.js)): reads the cart back out of `useSearchParams`, shows an order summary (items + ₹35 delivery charge + 5% GST), and a form that toggles between:
   - **Delivery** — full address form
   - **Pickup** — shows the store address/map link instead
   Submitting builds a `guest_Address`-shaped object and `POST`s it to `http://127.0.0.1:8000/guest_address` (**the backend URL is hardcoded here** — change it for other environments).
4. **Order confirmation** ([src/app/checkOutFormAct/Page.js](palaharam_FE/src/app/checkOutFormAct/Page.js)): on a successful response, a blurred overlay shows the success message and order ID, then auto-redirects to `/` after 5 seconds.

### Where the data comes from — static vs database

This is the key thing to understand as a developer:

- **Menu items are 100% static on the frontend.** The menu page fetches [public/data/sample.json](palaharam_FE/public/data/sample.json) (served by Next.js as a static file) via axios. Each item has `name`, `description`, `image` (path into `public/Images/`), and `values` (price in ₹). **Nothing on the menu comes from the database.** To add/edit a menu item, edit `sample.json` and drop the image into `public/Images/`.
- **The database is write-only from the frontend's perspective.** The only backend call the UI makes is the `POST /guest_address` at checkout, which persists the order into the `guests` table. No page reads data back from the DB (there are no GET endpoints for orders/menu yet).
- All images, the store address, delivery charge (₹35), and GST (5%) are hardcoded in the frontend.

### Frontend setup & run

```bash
cd palaharam_FE
npm install
npm run dev        # http://localhost:3000
```

Run the backend first (port 8000) or checkout submission will fail. `palaharam_FE/.env` exists but is currently empty.

---

## End-to-end order flow

```
Menu page                Checkout page                  FastAPI                    SQLite
─────────                ─────────────                  ───────                    ──────
load sample.json  ──►    cart via ?cart= query    ──►   POST /guest_address  ──►   INSERT INTO guests
(static file)            + address/payment form         (validate w/ Pydantic,     (JSON cart stored
                                                         json.dumps the cart)       as a string column)
                                                              │
                         confirmation overlay  ◄──  {message, id}
                         (redirects home in 5s)
```

## Known issues / notes for contributors

- `requirements.txt` is empty — keep it updated (`pip freeze > requirements.txt`) once you have a working venv.
- The backend URL (`http://127.0.0.1:8000`) is hardcoded in `checkOut/page.js`; move it to `NEXT_PUBLIC_API_URL` in `palaharam_FE/.env` when adding environments.
- User passwords in the `users` table are stored in plain text — hash them before this route is used for real.
- In `menu/page.js` the map callback is written `menu.map((index, it) => ...)` — `index` is actually the **item object** and `it` is the array index. It works, but the names are swapped; be careful when editing.
- `mobileNumber` is an `Integer` column, so leading zeros are lost and very long numbers can overflow — consider switching to `String`.
- `models.py` uses `default=datetime.now()` (evaluated once at import); use `default=datetime.now` for a per-row timestamp.
- The GST shown on checkout is added to the displayed total, but the `Total_Amount` sent to the backend is items + ₹35 only (no GST).
- Two `.db` files exist; only `palaharam_BE/dbConfig/Palaharam.db` is live.
- A Firebase service-account JSON sits in `palaharam_BE/` — it should be removed from the repo and rotated if it was ever committed with real keys.
