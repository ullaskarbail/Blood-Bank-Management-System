# Production-Level Blood Bank Management System

A robust, full-stack Blood Bank Management System built with Python Flask, MySQL, and Bootstrap 5. 

## Features
- **Flask App Factory & Blueprints**: Modular route definitions (`auth`, `donors`, `inventory`, `requests`, `hospitals`).
- **Dashboard**: Real-time stats and dynamic Chart.js inventory graphs.
- **Donor Management**: 90-day eligibility validation.
- **Inventory Logs**: Automatic transaction logging when stock is added/removed or requests approved.
- **Responsive UI**: Bootstrap 5 + Bootstrap Icons.
- **Dockerized**: Fully containerized with a MySQL 8 backend.
- **CI/CD pipeline**: Automated testing and deployment with Jenkins.

## Setup Instructions (Local / Docker)

1. Ensure Docker and Docker Compose are installed.
2. In the project root, start the application:
   ```bash
   docker-compose up --build -d
   ```
3. The app will be available at `http://localhost:5001`.
4. Admin login:
   - Username: `superadmin`
   - Password: `admin123`

## Running Tests
Tests are built with `pytest` and `pytest-mock`.
```bash
docker run --rm -it blood-bank-system-web pytest tests/
```

## CI/CD Deployment
Configure Jenkins with `dockerhub-credentials` and load the included `Jenkinsfile` to build, test, and push the image to Docker Hub before local compose deployment.
