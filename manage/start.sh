#!/usr/bin/env bash

set -e

cd ..

case "$1" in
--dev)
  echo "The development containers are running ..."
  set -a
  source "$PWD"/.env
  set +a
  docker-compose -f docker/docker-compose.dev.yml up --build --remove-orphans --force-recreate
  ;;
esac