FROM python:3.10.8
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "--host", "0.0.0.0", "--port", "8501"]
