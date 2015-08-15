#!/bin/bash

## This script will export heroku config environment variables from an app to your local shell.
## example:
##   $ source ./export_envs.sh my-app-name
## adding "local" as the final arg sets up your shell to connect to local db, redis, etc.:
##   $ source ./export_envs.sh my-app-name local

from_app="$1"
echo "reading from app $1"

skiplist="PYTHONHOME PYTHONPATH PATH LANG LD_LIBRARY_PATH LIBRARY_PATH APP_ENV HTTPS"

listcontains() {
  for word in $1; do
    [[ $word = $2 ]] && return 0
  done
  return 1
}

configs=$(heroku config --app "$from_app" | sed -e '1d')
while read key value;
do
    key=${key%%:}
    if listcontains "$skiplist" "$key"
    then
        echo "skipping $key"
    else
        echo "exporting $key"
        export ${key}=$value
    fi
done <<< "$configs"

if [[ $2 == "local" ]]
then
    echo "using LOCAL db and services..."
    export DATABASE_URL='postgres://localhost:5432/co_local'
    export BONSAI_URL='http://localhost:9200/'
    export REDISTOGO_URL='redis://127.0.0.1:6379/'
    export PAGE_CACHE_TIMEOUT='1'
fi
