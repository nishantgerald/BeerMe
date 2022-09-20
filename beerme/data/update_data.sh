#!/usr/bin/env bash
# PULLING LATEST DATA FROM openbrewerydb REPO
echo "Pulling latest data from repo and extracting"
git clone https://github.com/openbrewerydb/openbrewerydb.git
# CREATING COMBINED FILE WITH HEADERS AND ALL DATA
echo "Concatenating all data into single file"
head -1 openbrewerydb/data/england/east-sussex.csv > brewery.csv && tail -n +2 -q openbrewerydb/data/*/*.csv >> brewery.csv
# REMOVING REPO DATA
echo "Cleaning up"
rm -rf openbrewerydb
echo "Data update complete"