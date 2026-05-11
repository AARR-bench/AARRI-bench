FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/requests /app/preliminary_responses /app/followups /app/responses

COPY requests/ /app/requests/
COPY preliminary_responses/ /app/preliminary_responses/
COPY followups/ /app/followups/

CMD ["/bin/bash"]
