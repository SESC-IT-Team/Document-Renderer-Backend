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
    git \
    curl

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev


COPY . .
