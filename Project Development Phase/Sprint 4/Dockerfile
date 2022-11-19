FROM python:3.10.4
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV APP_KEY=sgk2303
ENV SENDGRID_API_KEY=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
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
