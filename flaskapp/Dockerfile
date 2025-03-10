FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install prerequisites
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    uuid-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Python PPA for modern Python versions
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.11 python3.11-venv python3.11-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python3.11 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --set python3 /usr/bin/python3.11

# Optional: Install pip and essential Python packages
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Verify installation
RUN python3 --version && pip3 --version

RUN mkdir -p /app
COPY requirements.txt /app
WORKDIR /app

# This is just due to install issues
RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000

# Perform rudimentary check that app can run
RUN python3 app.py --dry-run

CMD python3 app.py
