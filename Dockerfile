FROM python:3.6
LABEL maintainer="gontrum@me.com"
LABEL version="0.2"
LABEL description="Base image, containing no language models."

# Install the required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    supervisor \
    curl \
    nginx \
    vim-tiny &&\
    apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin

# Install node for the frontend
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - && \
  apt-get install -y nodejs &&\
  apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin

# Copy and set up the app
COPY . /app
RUN cd /app && make clean && make && cd /app/frontend && make clean && make

# Configure nginx & supervisor
RUN mv /app/config/nginx.conf /etc/nginx/sites-available/default &&\
  echo "daemon off;" >> /etc/nginx/nginx.conf && \
  mv /app/config/supervisor.conf /etc/supervisor/conf.d/

ENV PORT 80
EXPOSE 80
CMD ["bash", "/app/start.sh"]
