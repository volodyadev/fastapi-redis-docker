# Set args
ARG PYTHON_VERSION=3.11
ARG PYTHON_VERSION_SUFFIX=slim-buster

# -----------------------------------------------------------
# 'PYTHON-BASE' stage is used to creating a python base with shared environment variables
FROM python:${PYTHON_VERSION}-${PYTHON_VERSION_SUFFIX} AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DEPENDS="/usr/src/dependencies" \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    POETRY_VERSION=1.2.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Redis
# RUN apt-get update && \
#     apt-get install -y redis-server && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


# -----------------------------------------------------------
# 'PIP-POETRY-BASE' stage is used to install pip and poetry only
FROM python-base as pip-poetry-installation

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.4.0

# We copy our Poetry requirements here to cache them
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

# And create requirements.txt file for production mode
RUN poetry export --without-hashes  -f requirements.txt -o requirements.txt


# -----------------------------------------------------------
# 'POETRY-BASE' stage is used to build dependencies for development mode
FROM python-base as poetry-packages-installation

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR $PYSETUP_PATH
# Copying poetry and venv into image
COPY --from=pip-poetry-installation $POETRY_HOME $POETRY_HOME
COPY --from=pip-poetry-installation $PYSETUP_PATH $PYSETUP_PATH

# Install all deps using poetry
RUN poetry install


# -----------------------------------------------------------
# 'DEVELOPMENT' stage installs all dev deps and can be used to develop code.
FROM python-base as development
ENV FASTAPI_ENV=development \
    PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Copying poetry and venv into image
COPY --from=poetry-packages-installation $POETRY_HOME $POETRY_HOME
COPY --from=poetry-packages-installation $PYSETUP_PATH $PYSETUP_PATH

# Copying our entrypoint
COPY ./docker/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app
COPY . .