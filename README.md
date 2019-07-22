## OVERVIEW
A base Flask-RESTful API designed to receive specified HTTP requests from a variety of client applications (Web, Mobile, Desktop, etc) and return appropriate JSON responses or HTML template renders. Client Authentication and Login implemented using compact JSON Web Tokens 

## SETUP
Clone the Prometheus repository to your local development machine
In the respective 'Models' and 'Resources' directories: Create or edit the Model classes, Resources and associated relational database URIs or tables as you may require in order to achieve your API's response objectives to the respective HTTP request methods (GET, POST, PUT, DELETE)

NOTE: Make sure to modify 'app.py' to include each desired end point and associated resource as your web API may require. 



## INSTALLATION

``````````````
Requirements:
Python 3.7.3
Flask
Flask-RESTful
Flask-JWT
Flask-JWT-Extended
Flask-SQLAlchemy
uwsgi
Psycopg2 (for PostgreSQL DB implementation)
``````````````

#### Deployment (On Heroku)
>_ Sign In to Heroku Dashboard
>_ Create new Heroku app
>_ Go to the Heroku app 'Settings' tab: add Python to the Buildpack
>_ Go to the 'Deploy' tab and select GitHub or any other preferred deployment method
>_ Connect to the remote repository containing the modified source code 
>_ Select the desired deployment branch and Deploy Branch 



