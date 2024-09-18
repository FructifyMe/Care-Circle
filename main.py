from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Recreate all tables with the updated schema
    app.run(host='0.0.0.0', port=5000)
