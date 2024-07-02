
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

5. Collect static files:

```
python manage.py collectstatic
```

6. Create a superuser:

```
python manage.py createsuperuser
```

7. Run the development server:

```
python manage.py runserver
```


## Docker Installation

### Prerequisites
1. Docker
2. Docker Compose
3. Git

### Steps
1. Clone the repository:
```sh 
git clone `https://github.com/emoncse/Bitmorpher.git`
````

2. Change directory to the project folder:
```sh
cd Bitmorpher
```

3. Build the Docker image and Run the Docker container:
```sh
docker compose up --build
```

4. Run the Docker container in the background:
```sh
docker compose up -d
```


## Setup

### Settings

Ensure the following settings are correctly configured in `settings.py`:

```
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-vwsopxdivfoe(3n_z%ewxojb-#mzknd+tvvzq2%$yee_*^4+jl'

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'external.paginated_response.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CUSTOM_INSTALLED_APPS = [
    'rest_framework',
    'drf_spectacular',
    'user_panel',
    'log_space',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *CUSTOM_INSTALLED_APPS,
]

AUTH_USER_MODEL = 'user_panel.CustomUser'

CUSTOM_MIDDLEWARE = [
    'external.middleware.LogRequestMiddleware.LogRequestMiddleware',
    'external.middleware.UserTypeCheckMiddleware.UserTypeCheckMiddleware',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    *CUSTOM_MIDDLEWARE,
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'SIGNING_KEY': SECRET_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Bitmorpher API Documentation',
    'DESCRIPTION': 'Bitmorpher API Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/request.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
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

