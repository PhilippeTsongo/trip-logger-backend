# ELD Trip Logger API

## Overview
This Django REST Framework (DRF) project provides an API for logging and managing Electronic Logging Device (ELD) trip data. The application takes trip details as inputs, calculates optimal routes, and generates ELD logs for compliance tracking.

## Features
- Accepts trip details as inputs:
  - Current location
  - Pickup location
  - Dropoff location
  - Current cycle hours used
- Generates outputs including:
  - Map showing route, stops, and rest periods (utilizing a free map API)
  - Daily log sheets with visual ELD log representation

---

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Mapping API:** (openrouteservice)

---

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/eld-trip-logger.git
cd eld-trip-logger
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following variables:

```ini
# .env file
DATABASE_NAME=dbname
DB_USERNAME=postgres
DB_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY='app key'
DEBUG=True
OPENROUTESERVICE_API_KEY=open route service api key
OPENROUTERSERVICE_URL=open router service url
```

To generate a Django `SECRET_KEY`, you can use:
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Set Up the Database
Run migrations to set up the database schema:
```sh
python manage.py migrate
```

### 6. Run the Development Server
```sh
python manage.py runserver
```
Access the API at: [http://127.0.0.1:8000]

---

## API Endpoints

### Trip Management
- `POST /api/trip` - Create a new trip
- `GET /api/trip` - get a list of trips
- `GET /api/trip/{tripId}/` - Retrieve trip details

---

## Contact
For any inquiries, contact **[PHILIPPE TSONGO TAHAKAVA]** at **philippetsongo90@gmail.com**.

---
