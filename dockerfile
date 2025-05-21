FROM python:3.12-slim
WORKDIR /gateway
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./uvicorn.sh
ENV PYTHONPATH=/gateway/app
CMD ["/bin/bash", "./uvicorn.sh"]
