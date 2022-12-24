# Base image
FROM python:3.10.8
# Creation of a working directory app
WORKDIR /app
# Copy all the files of this project inside the container
COPY . .
# Installation of code dependencies
RUN pip install -r requirements.txt
# Command to be executed when the container is launched
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#last version Entrypoint instead of CMD
