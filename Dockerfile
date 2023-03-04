FROM python:3.9

# Prepare runtime environment
ENV PYTHONUNBUFFERED 1
ENV WORKERS 2

ARG PRODUCTION=0
ENV PRODUCTION ${PRODUCTION:-0}

ARG CONFIG_DIR
ENV CONFIG_DIR ${CONFIG_DIR}

# Create non-root user
ENV USER worker
RUN addgroup --gid 1001 $USER && adduser -u 1001 --gid 1001 --shell /bin/sh --disabled-password --gecos "" $USER
WORKDIR /home/$USER

# Build
ENV PATH="/home/$USER/.local/bin:${PATH}"
COPY --chown=$USER:$USER requirements.txt .
RUN apt-get -q update \
        && apt-get -qqy --no-install-recommends install libc6-dev libpq-dev gcc git \
        && rm -rf /var/lib/apt/lists/* \
        && pip --disable-pip-version-check install -U pip \
        && runuser $USER -c 'pip --disable-pip-version-check install --user --no-cache-dir -r requirements.txt' \
        && apt-get -qqy remove libc6-dev gcc git \
        && apt-get -qqy autoremove

EXPOSE 8000

USER $USER

# Copy source
COPY --chown=$USER:$USER . .
