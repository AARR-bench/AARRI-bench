#!/bin/bash
set -euo pipefail

cd /app/repo

git config user.name "Researcher"
git config user.email "researcher@example.com"

if ! grep -q "^.env$" .gitignore 2>/dev/null; then
  echo ".env" >> .gitignore
fi

if ! grep -q "^logs/$" .gitignore 2>/dev/null; then
  echo "logs/" >> .gitignore
fi

if [ -f logs/run.log ]; then
  sed -i 's/sk-[A-Za-z0-9]\{16,\}/sk-REDACTED/g' logs/run.log
fi

git add .gitignore call_llm.py logs/run.log
git commit -m "security: remove hardcoded secrets, ignore .env and logs"