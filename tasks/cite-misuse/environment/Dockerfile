FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY paper/manuscript.tex /app/paper/manuscript.tex
COPY reviews/reviewer_2.txt /app/reviews/reviewer_2.txt
COPY evidence/chen_2022_rs_sota.txt /app/evidence/chen_2022_rs_sota.txt
COPY evidence/li_2023_transunet.txt /app/evidence/li_2023_transunet.txt
COPY evidence/wang_2023_msa_rs.txt /app/evidence/wang_2023_msa_rs.txt
COPY evidence/yang_2022_vis.txt /app/evidence/yang_2022_vis.txt
COPY evidence/zhang_2024_aug_rs.txt /app/evidence/zhang_2024_aug_rs.txt