#!/bin/bash
#BACKUP_DIR="/mnt/backups"
#DATE=$(date +%F)
#DB_NAME="moto_db"
#DB_USER="moto_user"
#DB_PASS="moto_password"
#mkdir -p $BACKUP_DIR
#mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/moto_db_$DATE.sql
#find $BACKUP_DIR -type f -mtime +7 -delete

#!/bin/bash

BACKUP_DIR="/mnt/backups"
DATE=$(date +%F)
DB_NAME="moto_db"
DB_USER="moto_user"
DB_PASS="moto_password"

mkdir -p $BACKUP_DIR

# Run the mysqldump (make sure mysqldump is installed)
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/moto_db_$DATE.sql
# Clean backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
