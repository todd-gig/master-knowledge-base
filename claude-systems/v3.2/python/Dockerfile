FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install pyyaml
EXPOSE 8004
CMD ["python3", "-m", "http.server", "8004"]
