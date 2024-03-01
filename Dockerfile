FROM python:3.12-slim 

# Set the working directory in the container
WORKDIR /app

COPY app.py /app

# Install the required packages
RUN pip3 install fastapi requests uvicorn

# Expose the port 80
EXPOSE 80

# Command to run the application
CMD ["python3", "app.py"]