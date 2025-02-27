import os
import sys
from flask_migrate import Migrate, upgrade

# Add the current directory to Python's path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import your app
from app import createapp, db
from app.models import User, UserPreferences, UserProgram, Courses, UserTermPlanning, RefreshTokens

if __name__ == "__main__":
    try:
        app = createapp()
        
        with app.app_context():
            print("Starting database upgrade...")
            # Make sure migrations directory exists
            if not os.path.exists("migrations"):
                print("Initializing migrations directory...")
                from flask_migrate import init
                init()
            
            # Create migration if needed
            from flask_migrate import migrate
            print("Creating migration...")
            migrate(message="Initial migration")
            
            # Apply migration
            print("Applying migration...")
            upgrade()
            
            print("Database setup completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())