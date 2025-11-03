import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database Name
DB_Name = "Palaharam.db"
DB_Path = os.path.join(BASE_DIR, DB_Name)

# SQLAchemy Database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_Path}"