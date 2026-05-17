FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest

RUN mkdir -p /app/weekly_reports /app/feedback

COPY weekly_reports/ /app/weekly_reports/

CMD ["/bin/bash"]
