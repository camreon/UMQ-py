#! /usr/bin/env bash

pip install --upgrade youtube-dl

# Let the DB start
sleep 5;

alembic upgrade head