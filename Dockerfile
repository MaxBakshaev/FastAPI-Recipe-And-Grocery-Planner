FROM python:3.12.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod 755 .

COPY wait-for-it.sh /app/wait-for-it.sh
RUN ls -l /app/app
RUN chmod +x /app/wait-for-it.sh

ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]

# docker build -t fastapi_planner_image .
# docker run -d --name fastapi_planner -p 8000:8000 fastapi_planner_image