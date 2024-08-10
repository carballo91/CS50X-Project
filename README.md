# Clinica Web Application

## Overview
This web application is designed to manage patient information, consultations, prescriptions, sends real time notifications to fill out new consultation form as well as prescription form for patients. It also generates a pdf file with the medicines prescribed and it keeps a report of the medicines prescribed. This web application has an administrator panel where you can add new users with two roles: admin or user. This application is meant to be used in a local environment.

## Project Structure

The project is organized into several key files and directories, each serving a specific purpose within the application:

### 1. `app/`
The core of the Clinica application resides in the `app/` directory, which is structured as follows:

- **`__init__.py`**: This file initializes the Flask application, setting up configurations, registering blueprints, and managing application context. It is the entry point for the app's various components, ensuring they work together seamlessly.

- **`blueprints/`**: The `blueprints/` directory organizes the application's different functional areas into separate modules. Each blueprint corresponds to a specific application section, such as patient management, consultations, login, and reports. The application maintains a modular structure by using blueprints, making it easier to manage and extend.

- **`forms/`**: This directory contains the Flask-WTF forms for handling user inputs. Each form corresponds to a specific function, such as adding a new patient, searching for a patient, creating prescriptions, and consultations. These forms ensure that user inputs are validated and securely processed.

- **`models.py`**: This file defines the application's data models, representing the underlying database structure. Using SQLAlchemy ORM, `models.py` maps Python objects to database tables, facilitating CRUD (Create, Read, Update, Delete) operations. Models include classes like `PatientData`, `ConsultationData`, `Prescription`, and more, reflecting the core data used by the application.

- **`static/`**: The `static/` directory holds all the static files, including CSS, JavaScript, and images. These assets are used by the front end of the application to style the user interface, add interactivity, and provide visual elements like logos or icons.

- **`templates/`**: The `templates/` directory contains the templates used to render HTML pages.

### 2. `config.py`
The `config.py` file stores configuration settings for the Flask application. This includes important parameters like the secret key, database URI, and other environment-specific settings. By centralizing these configurations, `config.py` allows for easy adjustment of application settings based on the deployment environment (e.g., development, testing, production).

### 3. `errors.py`
The `errors.py` file handles custom error pages and error-handling logic within the application. When an error occurs (such as a 404 Not Found or 500 Internal Server Error), `errors.py` defines how the application responds, ensuring users receive informative and user-friendly error messages.

### 4. `requirements.txt`
The `requirements.txt` file lists all the Python packages and dependencies needed to run the Clinica application. These dependencies include Flask, SQLAlchemy, Flask-WTF, and any other libraries the application relies on. By including a `requirements.txt` file, the environment can be easily replicated by installing the necessary packages using `pip`.

### 5. `run.py`
The `run.py` file is the entry point for starting the Flask application. Running this file launches the web server and initializes the application, making it accessible through a web browser. It typically includes commands to set up the environment and run the Flask app in debug or production mode.

## Design Choices

During the development of the Clinica application, several design decisions were made to ensure the application is robust, maintainable, and secure:

### Modular Structure with Blueprints
The decision to use Flask blueprints was driven by the need to keep the application modular and organized. By separating different functionalities into distinct blueprints, the application is easier to maintain, extend, and debug. This structure also allows for the independent development of each module, promoting better code organization.

### Form Handling with Flask-WTF
Flask-WTF was chosen for form handling due to its powerful validation and security features. By using Flask-WTF, the application ensures that all user inputs are thoroughly validated before processing, reducing the risk of malicious inputs and improving the system's overall security.

## Installation

To set up and run the Clinica web application on your local machine, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/carballo91/CS50X-Project.git
cd CS50X-Project
```

### Step 2: Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Create and activate a virtual environment using the following commands:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install the required dependencies using the requirements.txt file:

```bash 
pip install -r requirements.txt
```
### Step 4: Configure the Application

You may need to modify the database URI, Secret Key, Admin Password and other settings to match your local setup.

### Step 5: Initialize the Database

Before running the application, ensure the database is set up correctly. If you are using SQLAlchemy, you may need to create the database and apply migrations:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### Step 6: Run the Application

Finally, start the Flask application using the following command:

```bash
python run.py
```

The application should now be running at http://127.0.0.1:5000/.