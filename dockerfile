# Use an official Python image as the base image
FROM ubuntu:latest


RUN apt update
RUN apt install python3 -y

# Set the working directory in the container
WORKDIR /usr/app/src


COPY main.py ./

# Run the command to start the app
CMD ["python3", "./main.py"]
