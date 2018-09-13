FROM python:3.6-alpine3.6
ENV FLASK_APP src
WORKDIR /srv
COPY setup.py .
COPY . .
RUN pip install --no-cache-dir --requirement requirements.txt
EXPOSE 4567
CMD ["flask", "run"]
