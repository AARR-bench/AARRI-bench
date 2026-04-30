FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    base64 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY server/ /server/
COPY bin/ /app/bin/
COPY dataset/ /dataset/

RUN chmod +x /server/message_client /server/lab_server /app/bin/message_client /app/bin/lab_server

ENV PATH="/app/bin:${PATH}"

CMD ["/bin/bash"]
