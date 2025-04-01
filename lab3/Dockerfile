FROM python:3.12-slim
EXPOSE 8503
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port", "8503"]
