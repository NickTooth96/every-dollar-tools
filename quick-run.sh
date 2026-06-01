#!/bin/bash

BUDGET_PATH="${1}"
if [ -z "$1" ]; then
    echo "Usage: $0 <budget-file-path> [checking-balance]"
    exit 1
fi

if [ ! -f "/Users/nicktoothaker/Downloads/${BUDGET_PATH}" ]; then
    echo "Error: Budget file not found at /Users/nicktoothaker/Downloads/${BUDGET_PATH}"
    exit 2
fi

CHECKING_BALANCE=""
if [ -z "$2" ]; then
    CHECKING_BALANCE="0"
else
    CHECKING_BALANCE="$2"
fi

docker build -t every-dollar-tools -f .devcontainer/Dockerfile .
clear
docker run --rm -v /Users/nicktoothaker/projects/every-dollar-tools:/workspace -v /Users/nicktoothaker/Downloads/"${BUDGET_PATH}":/downloads/budget.pdf -w /workspace every-dollar-tools python every-dollar-tools.py --budget-file /downloads/budget.pdf --plan-transfers --checking-balance "${CHECKING_BALANCE}" 