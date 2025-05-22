FROM python:3.12-slim
WORKDIR /app

RUN useradd -m player

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "-c", "python3 ModuleGame.py $STAGES"]
