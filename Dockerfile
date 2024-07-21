FROM python:3.9
WORKDIR /python

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /python
CMD ["python", "main/main.py"]
