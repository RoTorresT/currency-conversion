# Currency conversion
## Introduction
This FastAPI project is a tool for currency conversion, based on the mid-market rate (data is extracted/updated from xe.com). It allows users to convert between different currencies and view historical conversion data.

The project exposes four endpoints that can be accessed via HTTP requests:

- /convert: Endpoint for converting between currencies.
- /currencies: Endpoint for retrieving a list of available currencies.
- /history: Endpoint for retrieving historical conversion data.
- /login: Endpoint for authenticating users.

Por more in-depth documentation, check out the FastAPI documentation after running the application.

## Getting Started
### System requirements
Python 3.10 or higher
### Secrets (.env)
This application requires three secrets to work correctly. The template for the .env file is in example.env. The strings (ID, PASSWORD) that are set up in the .env file are necessary for logging in and authenticating users.

Example of .env file:

```bash
    ID=admin123
    PASSWORD=admin123
    SECRET_KEY=secret_key_123
```

## requirements.txt

It's recommended to create and activate a virtual environment before installing the requirements.

```bash
    pip install -r requirements.txt
```

## Local Deployment
Use uvicorn to run the application with the following configurations:

- Reloads the app when there is any change in the code, disable this flag in production environment.
- Sets the application to run on port 5000. Ensure the port is free or change the port accordingly.

```bash
    uvicorn main:app --reload --port 5000
```

## API Documentation
As this is a FastAPI project, the documentation for the endpoints can be found at localhost:5000/docs after running the application.

## Error Handling
Errors are managed by the middleware. The project follows the HTTP status code conventions for error handling.