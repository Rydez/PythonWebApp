# Currently unused as a module.
# Code has been placed in app.py to automate db making

from project import db
from project.models import UserPost

# Create the database and the db tables
db.create_all()

# Insert
db.session.add(UserPost('WTF?!', 'mer.'))

# Commit the changes
db.session.commit()