FROM python:3.11-slim

WORKDIR /app

COPY literature/ /app/literature/
COPY siyuan/ /app/siyuan/
COPY priya/ /app/priya/
COPY marcus/ /app/marcus/

RUN mkdir -p /app/feedback
RUN mkdir -p /logs/verifier

CMD ["/bin/bash"]
