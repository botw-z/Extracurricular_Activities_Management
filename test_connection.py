from config import db, app

with app.app_context():
    try:
        db.engine.connect()
        print("Successfully connected to the database!")
    except Exception as e:
        print(f"Error connecting to the database: {e}") 