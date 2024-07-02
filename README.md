
# Bitmorpher

Bitmorpher is a Django-based web application with JWT authentication using Django Rest Framework (DRF) and drf-spectacular for API schema generation and documentation.

## Table of Contents

- Installation
- Setup
- API Endpoints
- Swagger API Documentation
- Using Postman

## Installation

### Prerequisites

- Python 3.9+
- Django 4.2+
- Virtualenv

### Steps

1. Clone the repository:

```
git clone https://github.com/emoncse/Bitmorpher.git
cd Bitmorpher
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Apply the migrations:

```
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
```

5. Create a superuser:

```
python manage.py createsuperuser
```

6. Run the development server:

```
python manage.py runserver
```

## Setup

### Settings

Ensure the following settings are correctly configured in `settings.py`:

```
INSTALLED_APPS = [
    # other installed apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'user_panel',
    'log_space',
]

AUTH_USER_MODEL = 'user_panel.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Bitmorpher API',
    'DESCRIPTION': 'API documentation for Bitmorpher project',
    'VERSION': '1.0.0',
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'APPEND_COMPONENTS': {
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    'SECURITY': [
        {"Bearer": []}
    ],
}
```

## API Endpoints

### Authentication

- Obtain Token: `POST /api/token/`
- Refresh Token: `POST /api/token/refresh/`

### User Management

- Get All Users: `GET /API/users/`
- Create User: `POST /API/users/`
- Get User by Username: `GET /API/users/{username}/`
- Update User by Username: `PUT /API/users/{username}/`
      - must send authorization token in request body
- Partially Update User by Username: `PATCH /API/users/{username}/`
      - must send authorization token in request body
- Delete User by Username: `DELETE /API/users/{username}/`
        - must send authorization token in request body
- Get All Log: `GET /API/logs/`
- Get Log by id: `GET /API/logs/{id}`

## Swagger API Documentation

- Bitmorpher Task API Documentation
- Version: 1.0.0
- OAS: 3.0

### Swagger URL

- **Swagger**: `http://127.0.0.1:8000/v1/swagger/`
- **Bitmorpher API Documentation**

### User Management

- **GET** `/API/users/`
- **POST** `/API/users/`
- **GET** `/API/users/{username}/`
- **PUT** `/API/users/{username}/`
- **PATCH** `/API/users/{username}/`
- **DELETE** `/API/users/{username}/`

### API

- **POST** `/api/token/`
- **POST** `/api/token/refresh/`

## Using Postman

### Obtain Token

1. **URL**: `http://127.0.0.1:8000/api/token/`
2. **Method**: `POST`
3. **Body**: 
   ```
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

### Access Protected Endpoint

1. **URL**: `http://127.0.0.1:8000/api/protected/`
2. **Method**: `GET`
3. **Headers**:
   - Key: `Authorization`
   - Value: `Bearer <access_token>`

Replace `<access_token>` with the token obtained in the previous step.

### Refresh Token

1. **URL**: `http://127.0.0.1:8000/api/token/refresh/`
2. **Method**: `POST`
3. **Body**:
   ```
   {
       "refresh": "<refresh_token>"
   }
   ```

