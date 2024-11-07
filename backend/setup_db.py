from backend import create_app, db


def setup_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables recreated successfully!")


if __name__ == "__main__":
    setup_database()
