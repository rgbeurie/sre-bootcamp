FROM python:3.9.6-alpine
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python ./api.py
