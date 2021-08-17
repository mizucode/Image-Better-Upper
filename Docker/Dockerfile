FROM python:3.8.8-slim-buster
COPY requirements.txt ./requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app
CMD ["python", "app.py", "--host=0.0.0.0"]