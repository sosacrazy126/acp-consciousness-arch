FROM python:3.11-slim
WORKDIR /app
COPY observer/observer.py .
RUN pip install grpcio
CMD ["python", "observer.py"]
