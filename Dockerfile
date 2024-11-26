FROM python:3.13-slim

ADD /src /code
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "/code/main.py"]