FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 base64 coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /server/bin && \
    chmod 111 /server

COPY server/lab_server /server/lab_server
COPY server/message_client /server/message_client
COPY server/lab_members.json /server/lab_members.json
COPY bin/lab_server /app/bin/lab_server
COPY bin/message_client /app/bin/message_client
COPY bin/lab_members.json /app/lab_members.json
COPY dataset /dataset

RUN chmod 111 /server/lab_server && \
    chmod 111 /server/message_client && \
    chmod 444 /server/lab_members.json && \
    chmod +x /app/bin/lab_server && \
    chmod +x /app/bin/message_client && \
    ln -sf /app/bin/lab_server /app/lab_server && \
    ln -sf /app/bin/message_client /app/message_client
