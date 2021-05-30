# Flask-phone-market
## Quick Info

This project is created using Flask, SQLite database and Boostrap (connected with SQLAlchemy).

Many Flask features have been used there (including db migrations, wtforms, token serializer, flask login, etc.).

---

Upon registering, a user is given 1000$ that they can spend on a Phone Market.

As logged in, the user is not only able to check info about product but also to buy or sell it.

If the user buys an item, they own it therefore no one else can have it.

They have their own profile where they can upload their profile picture and change their account data.

Every image the user uploads is converted into 125x125px to save more space.

The user can post on a forum, edit their own post as well as delete it.

They can also see any other user's posts by clicking on their username or profile picture.

If the user forgets their password, it can be reset by sending an email to them with a reset token

(You have to provide email credentials for this to work).

Just check it out!


## Getting Started

1) Git clone

2) Create a virtual environment
`python -m venv venv`

3) Python: select interpreter
at `venv/Scripts/python.exe`

4) Activate the virtual environment
`source venv/Scripts/activate`

5) Upgrade pip
`python -m pip install --upgrade pip`

6) Install required modules
`pip install -r requirements.txt`

7) Create `/.env` and configure it (as in `/.env_sample`)

   - 7.1 Generate your secret key
   
   ```python
   python
   >>> import os
   >>> os.urandom(12).hex()
   '2421aae81f36aaf63d79facd'
   ```
   `SECRET_KEY=2421aae81f36aaf63d79facd`
   
   7.2 Insert your email credentials
   
      - "Reset your password" email will be sent using them.
   
   `EMAIL_USER=yoursamplemail@gmail.com`
   
   `EMAIL_PASS=yourpassword122`

8) Everything is set up! 
```
python run.py
```

## Note:

SQLAlchemy URI database is hard-coded inside market/__init__.py as `sqlite:///market.db` for testing purposes.
