FROM python:3.11-slim
WORKDIR /app
COPY src/ /app
RUN pip install flask
CMD ["python", "app.py"]

