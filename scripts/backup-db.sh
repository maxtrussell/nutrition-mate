#!/bin/bash

# DB backup script, NOTE: ensure your user has access to the mysql db 'nm'

# 1. backup db
/usr/bin/mysqldump nm | gzip -c > /opt/nutrition-mate/backups/$(date +%Y-%m-%d).gz

# 2. clean excess backups
# automatically removes oldest db backups after limit is reached
backups_dir="/opt/nutrition-mate/backups"
backups_limit=10
num_backups=$(ls $backups_dir | wc -l)

if [ $num_backups -ge $backups_limit ]; then
    let num_to_remove=$num_backups-$backups_limit
    rm $(ls $backups_dir | sort -r | tail -n $num_to_remove)
fi

# 3. sync backups with gcp bucket
gsutil rsync /opt/nutrition-mate/backups gs://nutrition-mate/
