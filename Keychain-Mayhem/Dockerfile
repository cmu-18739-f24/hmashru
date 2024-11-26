# Use Ubuntu as the base image
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and SQLite3
RUN apt-get update && apt-get install -y python3 python3-pip sqlite3 vim gnupg

COPY toberndo_private.key /root/private.key
COPY toberndo_public.key /root/public.key
COPY flag.txt /root/flag.txt

# Install Flask
RUN pip3 install flask 

RUN pip3 install python-gnupg

# Set the working directory
WORKDIR /app

# Copy the entire application directory to the container
COPY ./app .

RUN gpg --import /root/private.key && \
    gpg --import /root/public.key

# Only root can see. Needed for picoctf, and how it knows the right flag.
RUN mkdir /challenge && chmod 700 /challenge
RUN echo "{\"flag\":\"$(cat /root/flag.txt)\"}" > /challenge/metadata.json

# Expose port
EXPOSE 5000
# PUBLISH 5000 AS port

# Initialize the database and run the application
#RUN sqlite3 users.db "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL); INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'p@@5w0rd!');" & python3 app.py&

RUN echo '#!/bin/bash\n\
sqlite3 users.db "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL); INSERT OR IGNORE INTO users (username, password) VALUES ('"'"'admin'"'"', '"'"'p@@5w0rd!'"'"');" && \
python3 app.py\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/bin/bash", "/app/start.sh"]