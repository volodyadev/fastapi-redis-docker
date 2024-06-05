#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate our virtual environment for `poetry` here.
if [[ $FASTAPI_ENV == 'development' ]]; then
  . /opt/pysetup/.venv/bin/activate
fi

# And run alembic migrations
# alembic upgrade head

exec "$@"
