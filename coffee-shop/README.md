# Coffee Shop Full Stack

This project is for Udacity Fullstack Develoer Nanodegree. Completing this project will demonstrate the ability to implement Identity and Access Management. It will cover authentication and authorization using Auth0.

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Getting Started

### Installing Dependencies

#### Frontend Dependencies
This project uses ionic as frontend framework. Also, it uses npm to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. Make sure you have Nodejs which includes npm. After cloning, install Ionic CLI from the link [Ionic Framework Docs](https://ionicframework.com/docs/installation/cliopen) your terminal and run:

```bash
npm install
```
Update environments.ts file with all required configurations.

Then run:
```bash
ionic serve
```


#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend/src` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

You might need to update teh requirements.txt file with newer version for some dependencies.

From within the `backend/src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
flask run --reload
```

### Testing
Besides testing using the frontend application, the test can be conducted using the attached Postman collection.