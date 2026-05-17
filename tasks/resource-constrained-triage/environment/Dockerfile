FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest && \
    mkdir -p /app/requests /app/responses

COPY requests/ /app/requests/

CMD ["/bin/bash"]
