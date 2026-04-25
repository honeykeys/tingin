FROM python:3.11-slim

WORKDIR /app

COPY requirements-env.txt .
RUN pip install --no-cache-dir -r requirements-env.txt

COPY nursingfloor/ nursingfloor/
COPY tingin_env/ tingin_env/
COPY server.py .

EXPOSE 8080

CMD ["python", "server.py"]
