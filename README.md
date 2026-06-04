# Online Learning Platform API

A robust RESTful API for an online learning platform, built with **Django REST Framework (DRF)** and fully containerized using **Docker**. This project features a modern hybrid architecture, handling user authentication, course enrollments, secure video access, and an anti-cheat quiz evaluation system.

## 🚀 Technologies Used
* **Backend:** Python, Django 4.2, Django REST Framework
* **Database & Caching:** PostgreSQL, Redis
* **Background Tasks:** Celery
* **Authentication:** JWT (JSON Web Tokens)
* **Documentation:** Swagger (drf-spectacular)
* **Infrastructure:** Docker & Docker Compose

## ✨ Key Features
* **Stateless Authentication:** Secure login and registration using JWT.
* **Course Management:** Advanced search, filtering, and caching (Redis) for course listings.
* **Secure Media Access:** Custom DRF permissions to protect premium video content from unauthorized downloads.
* **Interactive Quiz System:** Automated server-side grading, percentage calculation, and anti-cheat mechanisms.
* **Asynchronous Processing:** Background email delivery using Celery and Redis.
* **Automated Testing:** Comprehensive Unit and Integration tests (APITestCase).

---

## 🛠️ Getting Started (Docker Setup)

Since this project is fully Dockerized, you don't need to manually create virtual environments or install Python dependencies. Docker handles everything for you.


### 1. Clone the Repository
```bash
git clone [https://github.com/mohammadpy021/online-learning-platform.git](https://github.com/mohammadpy021/online-learning-platform.git)
cd online-learning-platform
```

### 2. Environment Variables
Create a `.env.dev` file in the root directory using the provided sample file:
#### On Linux/macOS
```bash
cp .env.dev.sample .env.dev
```
#### On Windows
```bash
copy .env.dev.sample .env.dev
```
*(Make sure to update the database passwords and secret keys inside the `.env-prod` file before running the project).*

### 3. Build and Run the Containers
Start the Web, Database, Redis, and Celery containers in the background:
```bash
docker-compose up -d --build
```

### 4. Apply Database Migrations
Create the necessary tables in the PostgreSQL database:
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser (Admin)
Create an admin account to access the Django admin panel:
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 📖 API Documentation (Swagger)
Once the containers are running, you can interact with the API endpoints directly through the auto-generated Swagger UI.

* **Swagger UI:** `http://localhost:8000/api/docs/`
* **Django Admin Panel:** `http://localhost:8000/admin/`
* **Home web page:** `http://localhost:8000/`

---

## 🧪 Running Tests
The project includes automated tests for both the `accounts` and `article` modules to ensure the stability of the core logic. To run the test suite, execute:

```bash
# Run all tests
docker-compose exec web python manage.py test
```

## 🛑 Stopping the Application
To stop the running containers without deleting your database volumes:
```bash
docker-compose stop
```
To stop and completely remove the containers and networks:
```bash
docker-compose down
```