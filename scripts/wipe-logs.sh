#!/bin/bash


RUNTIME_PATH="$(pwd)"
LOGS_PATH="$(realpath $(find . -type d -name 'logs' | head -n 1))"
echo "Clearing logs in $LOGS_PATH"
cd "$LOGS_PATH" || exit 1
rm -rf ./*
cd -