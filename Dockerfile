FROM python:3.4-alpine3.7
ENV FLASK_APP src
WORKDIR /srv
COPY setup.py .
COPY . .
RUN pip install --no-cache-dir --requirement requirements.txt
EXPOSE 8080
CMD ["flask", "run"]
