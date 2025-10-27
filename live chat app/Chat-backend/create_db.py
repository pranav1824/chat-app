# create_db.py
from app import create_app, db
from app.models import User
app = create_app()
app.app_context().push()

db.create_all()

# create a default admin (only if not exists)
if not User.query.filter_by(username="admin").first():
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")   # change in production
    db.session.add(admin)
    db.session.commit()
    print("Created admin user with username=admin password=admin123")
else:
    print("Admin exists")
