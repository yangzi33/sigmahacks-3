# Main application module
from app import app, db
from app.models import User, Post

# Pre-imports modules for `flask shell`
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}