# Flask Phone Market

## Quick Info

This project is created using **Flask**, an **SQLite** database, and **Bootstrap**. It makes full use of various Flask features such as database migrations, WTForms, token serialization, and Flask-Login.

Upon registering, each user receives \$1000 to spend on the Phone Market. Logged-in users can view product details, buy or sell devices, and manage a personal profile—including uploading a profile picture (all images are automatically resized to 125x125px). Additionally, users can participate in a forum where they can create, edit, or delete posts, and view posts from other users by clicking on their username or profile picture. Should a user forget their password, a reset email (requiring proper email configuration) is sent with a reset token.

## 📸 Screenshots
![phone-market](https://user-images.githubusercontent.com/16180711/129389815-949b6a92-bd07-446a-88cb-17de8c8d7cf5.png)

## Tech Stack

- Python
- Flask
- SQLite (with SQLAlchemy)
- Bootstrap
- WTForms
- Flask-Login
- Flask-Migrate
- Flask-Mail
- Python-dotenv

## Getting Started

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd flask-phone-market
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Select the interpreter**

   Use `venv/Scripts/python.exe` on Windows (adjust path for your OS).

4. **Activate the environment**

   ```bash
   source venv/Scripts/activate  # On Windows
   source venv/bin/activate      # On Unix/macOS
   ```

5. **Upgrade pip**

   ```bash
   python -m pip install --upgrade pip
   ```

6. **Install requirements**

   ```bash
   pip install -r requirements.txt
   ```

7. **Configure environment variables**

   - Create a `.env` file (refer to `.env_sample`)

   - Generate a secret key:

     ```python
     import os
     os.urandom(12).hex()
     ```

     Example:

     ```env
     SECRET_KEY=2421aae81f36aaf63d79facd
     EMAIL_USER=your_email@gmail.com
     EMAIL_PASS=your_password
     ```

8. **Run the app**

   ```bash
   python run.py
   ```

## Notes

- The SQLAlchemy database URI is hardcoded as `sqlite:///market.db` in `market/__init__.py` for testing purposes.
- Docker deployment configuration is included.
- Includes support for custom error pages, pagination, authentication, account management, forum posting, and more.
