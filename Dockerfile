FROM python:3.7-slim-buster

# Set working directory as /app.
WORKDIR /app

# Copy main.py to /app/main.py
COPY main.py main.py
# Copy requirements.txt to /app/requirements.txt
COPY requirements.txt requirements.txt

# Install requirements.
RUN pip3 install -r requirements.txt

# Set run command.
CMD [ "python3", "/app/main.py", "run" ]