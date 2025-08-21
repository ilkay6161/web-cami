"""
Datenbank-Konfiguration für das professionelle Klassenbuch
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Datenbankinstanz erstellen
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialisiert die Datenbank mit der Flask-App"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Tabellen erstellen
    with app.app_context():
        db.create_all()