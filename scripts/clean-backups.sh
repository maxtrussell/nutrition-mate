#!/bin/bash

# automatically removes oldest db backups after limit is reached
backups_dir="/opt/nutrition-mate/backups"
backups_limit=10
num_backups=$(ls $backups_dir | wc -l)

if [ $num_backups -ge $backups_limit ]; then
    let num_to_remove=$num_backups-$backups_limit
    rm $(ls $backups_dir | sort -r | tail -n $num_to_remove)
fi

