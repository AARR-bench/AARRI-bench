FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && \
    (apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest python3-yaml \
        || (sleep 15 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest python3-yaml) \
        || (sleep 25 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest python3-yaml) \
        || (sleep 35 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest python3-yaml)) && \
    rm -rf /var/lib/apt/lists/*
COPY paper_methods.md /app/paper_methods.md
COPY experiments.yaml /app/experiments.yaml
