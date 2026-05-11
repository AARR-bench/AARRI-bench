FROM ubuntu:24.04
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY project_spec.md /app/project_spec.md
COPY ziqian/ /app/ziqian/
COPY sofia/ /app/sofia/
COPY arjun/ /app/arjun/
RUN mkdir -p /app/feedback
