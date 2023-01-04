# **Shortener Url Project**

**Project Purpose**
The purpose of this project is to create a shortened version of a given original link by making a POST request. This project was implemented using Django REST framework and a PostgresSQL database.

**Running the Program Locally**

1. install requirements.txt by the command 'pip install -r requirements.txt' in terminal from short_urls_learn folder.
2. Copy the .env and docker.env files from the email provided to short_urls_learn_main folder.
3. Paste these files into the short_urls_learn directory.
4. To run the application and the database in Docker containers, use the command docker-compose up in the terminal and that's use docker.env.
   - Alternatively, to run the application locally, first use the command docker-compose up db in the terminal to create the database in a Docker container 
    (now we use .env file for configuration) 
     Then, use the commands python manage.py makemigrations and python manage.py migrate in the terminal to migrate the new database according to the application. 
     Finally, use the command python manage.py runserver to run the local server.
   
**Creating a New Tiny URL**

   To create a new tiny URL, make a POST request to shorturls/create with the following JSON:
   {
    "original_link": "https://www.examplelink.com"
   }
Upon completion, a new Url object model will be created in the urls_table with the following fields:

id: serial id
original_url: the original URL
tiny_url: a random hexadecimal slug generated using uuid
click_counter: this value increments by 1 every time the tiny URL is redirected to the original URL

The returned value will be the full tiny URL.


**Running the tests**

To run the tests for this project, use the following command in the terminal:
	'python manage.py test manage_urls.tests'
This will run the test suite for the manage_urls app and display the results in the terminal.
The tests are located in the manage_urls/tests.py file and are designed to test the functionality of the views, models, and serializers in the project.

The test suite includes tests for creating new tiny URLs, retrieving and redirecting existing tiny URLs, and handling invalid URLs or requests.
These tests ensure that the application is functioning correctly and responding appropriately to different types of requests.