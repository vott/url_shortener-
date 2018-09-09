#!/bin/bash
export  PGPASSWORD=$POSTGRES_PASSWORD


# make sure pg is ready to accept connections
until pg_isready -h postgres -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB
do
  echo "Waiting for postgres at"
  sleep 2;
done

if [ "$DEV"="true" ]
then
    sh ./dev.sh
else
    sh ./run.sh
fi