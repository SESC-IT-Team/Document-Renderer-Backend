FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    gobject-introspection \
    py3-gobject3 \
    libffi \
    pango \
    cairo \
    librsvg \
    fontconfig \
    ttf-dejavu \
    bash \
    build-base \
    libpq \
    postgresql-dev \
    git \
    curl

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md uv.lock ./

RUN uv sync --no-dev --no-install-project --python /usr/local/bin/python

COPY . .

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:${PATH}"
