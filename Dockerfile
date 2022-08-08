FROM python:3.8
LABEL maintainer="gontrum@me.com"
LABEL version="3.0"
LABEL description="Base image, containing no language models."

# Copy and set up the app
COPY . /app
WORKDIR /app

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN python setup.py develop

ENV PORT 80
CMD ["bash", "/app/config/start.sh"]
