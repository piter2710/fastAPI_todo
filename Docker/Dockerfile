
FROM python:3.9-slim
WORKDIR /app
COPY ./Docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./TodoApp /app/TodoApp
EXPOSE 8000
CMD ["uvicorn", "TodoApp.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
