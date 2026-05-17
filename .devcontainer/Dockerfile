FROM ubuntu:24.04

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install pandas
RUN pip3 install --no-cache-dir --break-system-packages pandas wget pypdf

# Set Python 3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python
