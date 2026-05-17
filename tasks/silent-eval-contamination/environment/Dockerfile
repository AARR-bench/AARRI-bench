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
COPY evaluate.py /app/evaluate.py
COPY run_eval_log.txt /app/run_eval_log.txt
