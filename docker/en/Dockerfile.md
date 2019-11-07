FROM jgontrum/spacyapi:base_v2

ENV languages "en_core_web_md"
RUN cd /app && env/bin/download_models
