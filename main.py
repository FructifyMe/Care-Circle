import os
from app import create_app, db
from app.models import User

app = create_app()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Recreate all tables with the updated schema
    app.run(host='0.0.0.0', port=5000)
