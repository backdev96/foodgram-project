# Project Title

Application "Grocery Assistant" is a site where users can publish their recipes, subscribe to other authors, add their recipes to favourites. Service "Shopping List" allows users to create a list of products required to cook selected meals.

![foodgram-project workflow](https://github.com/backdev96/foodgram-project/workflows/foodgram/badge.svg)(https://github.com/backdev96/foodgram-project/actions)

Site

    to be added

## Getting Started

These instructions will get you a copy of the project and run it on your local machine for development and testing purposes. 

### Installing

Things you need to install the software and how to install them:

- clone the repository:

    git clone https://github.com/backdev96/foodgram-project

- activate the virtual environment and install all required packages.
    
    source venv/bin/activate

    pip3 install -r requirements.txt

### Installing

Activate the virtual environment and install all required packages using the following commands:
```
pip install -r requirements.txt.
```

## Running the tests

The project uses a workflow file yamdb_workflow.yaml for automated testing after the git push command.


## Deployment

Make sure you are in the same directory where you saved the dockerfile and start building the image. In the command, specify the name of the image: 
```
docker build -t name .
```
The dot at the end of the command is the path to the dockerfile from which to build.
When the build is complete, run the container: 
```
docker run -it -p 8000: 8000 foodgram-project
```
Now you can go in your browser to localhost: 8000, where is your application.

## Built With

* [Django Rest Framework](https://www.django-rest-framework.org/) - Web framework
* [Docker](https://www.docker.com/) - Software for deploying and managing applications in containerized environments.

## Author

* **Efremov Stanislav** - stasefremovx@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

