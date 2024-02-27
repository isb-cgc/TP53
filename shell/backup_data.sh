#!/usr/bin/env bash
## backup_data.sh
# A script to back up BQ table data, view scripts downloadable files, list files into a backup bucket for TP53


# PROD
DEST_PROJ=isb-cgc-tp53
DEST_BUCKET=tp53-data-backup
SRC_STATIC_BUCKET=tp53-static-files

# retrieve BQ table names to backup
tables=$(bq ls ${DEST_PROJ}:P53_data | grep -i TABLE | awk '{print $1}' | tail +3)
views=$(bq ls ${DEST_PROJ}:P53_data | grep -i VIEW | awk '{print $1}' | tail +3)
# create a backup folder with today's date
gsutil cp $(date +%Y%m%d) gs://${DEST_PROJ}/

### TABLES
# copy all tables from src to dest
for table in $tables
do
    bq extract \
    --compression=GZIP \
    --destination_format "CSV" \
    --field_delimiter '\t' \
    --print_header=false \
    P53_data.${table} \
    gs://${DEST_BUCKET}/$(date +%Y%m%d)/tables/$table.zip
done

### VIEWS
# extract all Views view scripts from BQ Views and copy into the bucket as SQL files
for view in $views
do
  echo $(bq show --view=true P53_data.${view} | tail -n +6 | gsutil cp - gs://${DEST_BUCKET}/$(date +%Y%m%d)/views/$view.view.sql)
done


### LIST files
gsutil cp -r gs://${SRC_STATIC_BUCKET}/list-files gs://${DEST_BUCKET}/$(date +%Y%m%d)/list-files
### CSV (downloadable) data files
gsutil cp -r gs://${SRC_STATIC_BUCKET}/data gs://${DEST_BUCKET}/$(date +%Y%m%d)/data
