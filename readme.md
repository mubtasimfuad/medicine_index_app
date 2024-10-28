# Medicine Index Application

Welcome to the Medicine Index Application, a web-based platform developed to enable users to view, search, and manage medicine information. This application supports both public and admin roles, with features for listing, searching, and CRUD operations on medicine data.

![Project Logo](https://via.placeholder.com/100x100?text=Logo)

---

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

---

## Features

1. **Medicine Listing**  
   - Users can view a list of all medicines, including details like name, generic name, manufacturer, description, price, and batch number.
   
2. **Search Functionality**  
   - Users can search for medicines by name or generic name.
   - Search results highlight matching keywords for improved user experience.

3. **User Roles and Permissions**  
   - **Public Users**: Can view and search for medicines.
   - **Admins**: Can perform full CRUD (Create, Read, Update, Delete) operations on medicines.

---

## Technology Stack

| ![Django](https://static.djangoproject.com/img/logos/django-logo-negative.png) | ![React](https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg) | ![Redis](https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Redis_Logo.svg/800px-Redis_Logo.svg.png) | ![MySQL](https://upload.wikimedia.org/wikipedia/en/thumb/d/dd/MySQL_logo.svg/1200px-MySQL_logo.svg.png) | ![Gunicorn](https://gunicorn.org/images/gunicorn-logo.png) |
|:------------------------------------------------------------:|:--------------------------------------------------:|:-------------------------------------------------------------:|:-------------------------------------------------------------:|:------------------------------------------------------------:|
| Django                                                       | React + TypeScript                                 | Redis                                                          | MySQL                                                          | Gunicorn                                                     |

### Key Libraries and Tools
- **Backend**: Django, Django REST Framework, Redis, MySQL
- **Frontend**: React (TypeScript), Axios
- **Deployment**: Docker, Gunicorn

---

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.11+**
- **Node.js** and **npm**
- **Docker** and **Docker Compose**

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mubtasimfuad/medicine_index_app.git
    cd medicine_index_app
    ```

2. **Backend Setup**:
    - Create and activate a virtual environment:
      ```bash
      python3 -m venv venv
      source venv/bin/activate  # For Unix
      # or `venv\Scripts\activate` on Windows
      ```
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

3. **Frontend Setup** (React):
    - Navigate to the frontend directory and install dependencies:
      ```bash
      cd frontend
      npm install
      ```
  
4. **Environment Variables**:  
   Rename `.env.example` to `.env` and configure the required environment variables (details below).

---

## Environment Variables

Configure the `.env` file with the following keys:

```plaintext
DEBUG=1
SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1
DB_HOST=host.docker.internal  # Use MySQL container host or IP
DB_PORT=3306
DB_NAME=medicine_index_db
DB_USER=db_user
DB_PASSWORD=db_password
REDIS_HOST=redis://redis:6379
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

---

## Running the Application

### Using Docker Compose (Recommended for Production)

To start the application with Docker Compose, ensure the Dockerfile and docker-compose.yml files are correctly set up as shown, then run:

```bash
docker-compose up --build
```

This will start:
- Django app (`web`) with Gunicorn on port `8000`
- Redis cache (`redis`) on port `6379`

### Running Locally for Development

1. **Start Backend Server**:
    ```bash
    python manage.py runserver
    ```

2. **Start Frontend Server**:
    ```bash
    cd frontend
    npm start
    ```

The frontend will run on `http://localhost:3000` by default, and backend APIs will be available at `http://localhost:8000`.

---

## Using the Application

- **Public Access**: View and search for medicines.
- **Admin Access**:
  - Login to the admin dashboard at `/admin`
  - Full CRUD operations on medicine data are accessible from the dashboard.

### API Endpoints (Swagger Documentation)
- Swagger documentation is available at `http://localhost:8000/swagger/` for detailed API usage.

---

## Screenshots

### 1. Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### 2. Medicine List
![Medicine List](https://via.placeholder.com/800x400?text=Medicine+List+Screenshot)

### 3. Search Functionality
![Search Results](https://via.placeholder.com/800x400?text=Search+Results+Screenshot)

---

## Deployment

The application is Docker-ready for easy deployment in production. Gunicorn is used as the WSGI server to serve Django, and Docker Compose manages Redis and other services for optimized performance.

---

## Project Structure

```plaintext
medicine_index_app/
├── core/                # Main Django application
├── inventory/           # Medicine management app
├── authentication/      # User authentication and permissions
├── frontend/            # React frontend
├── utils/               # Utility functions and Redis cache management
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Contributing

Feel free to fork this repository and submit pull requests. All contributions are welcome!

## License

This project is licensed under the MIT License.

For the complete codebase, visit the GitHub repository at [medicine_index_app](https://github.com/mubtasimfuad/medicine_index_app). 

