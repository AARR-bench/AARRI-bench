FROM python:3.11-slim

WORKDIR /app

COPY literature/ /app/literature/
COPY siyuan/ /app/siyuan/
COPY priya/ /app/priya/
COPY feedback/ /app/feedback/

RUN mkdir -p /logs/verifier

CMD ["/bin/bash"]
