FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && \
    (apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest \
        || (sleep 15 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest) \
        || (sleep 25 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest) \
        || (sleep 35 && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest)) && \
    rm -rf /var/lib/apt/lists/*
COPY paper_methods.md /app/paper_methods.md
COPY results_table.md /app/results_table.md
RUN mkdir -p /app/configs
COPY configs/das_bert_config.yaml /app/configs/das_bert_config.yaml
COPY configs/adam_config.yaml /app/configs/adam_config.yaml
COPY configs/sgd_config.yaml /app/configs/sgd_config.yaml
