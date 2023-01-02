FROM python:3.9

# Set the working directory to /app
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run the command to start the Django server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
