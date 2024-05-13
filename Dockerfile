# Use an official Python runtime as a parent image
FROM python:3.9.19-slim
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV SECRET_KEY AIzaSyDc0x59Hu9MA7AoQSlwDWzBX8EBjRT567k
EXPOSE 8080
CMD ["python", "app.py"]