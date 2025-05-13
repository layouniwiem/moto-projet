#!/bin/bash
BACKUP_DIR="/mnt/backups"
DATE=$(date +%F)
DB_NAME="moto_db"
DB_USER="moto_user"
DB_PASS="moto_password"
mkdir -p $BACKUP_DIR
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/moto_db_$DATE.sql
find $BACKUP_DIR -type f -mtime +7 -delete
tests/test_home.py
from app import create_app

def test_homepage():
    app = create_app()
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Motos" in response.data
