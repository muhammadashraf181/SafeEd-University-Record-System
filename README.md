# SafeEd - Secure University Record System

## Introduction
SafeEd is a secure university record system developed as a console-based application using Python. The main purpose of this project is to protect student academic information and control user access.

## Key Features
* **Secure Authentication:** Teachers and students log in using secure credentials. Passwords are not stored in plain text; instead, they are converted into hashed form using the SHA-256 algorithm.
* **Role-Based Access Control:** Students are allowed to view only their own records, while teachers can view and update records of assigned students only.
* **Security Logging:** The system maintains a security log file to record login, logout, and data update activities for monitoring purposes.

## Tech Stack
* **Language:** Python
* **Security:** SHA-256 Hashing

## How to Run
1. Ensure you have Python installed on your system.
2. Download the `SafeED Complete Project.py` file.
3. Open your terminal or command prompt.
4. Run the application using the command: `python SafeED_Complete_Project.py`
