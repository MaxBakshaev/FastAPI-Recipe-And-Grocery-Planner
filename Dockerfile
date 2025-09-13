FROM python:3.12.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod 755 .
RUN chmod +x /wait-for-it.sh
ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]

# docker build -t fastapi_planner_image .
# docker run -d --name fastapi_planner -p 8000:8000 fastapi_planner_image