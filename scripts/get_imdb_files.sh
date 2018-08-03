#!/bin/bash

set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

echo -e "Fetching Data from IMDB database \n"
echo "Fetching Actors"
curl -O -# ftp://ftp.fu-berlin.de/pub/misc/movies/database/frozendata/actors.list.gz
echo "Fetching Actresses"
curl -O -# ftp://ftp.fu-berlin.de/pub/misc/movies/database/frozendata/actresses.list.gz
echo "Fetching Genres"
curl -O -# ftp://ftp.fu-berlin.de/pub/misc/movies/database/frozendata/genres.list.gz
echo "Fetching Release Dates"
curl -O -# ftp://ftp.fu-berlin.de/pub/misc/movies/database/frozendata/release-dates.list.gz

echo -e "Building the csv file for UCSL ... "
python ./build_imdb.py
