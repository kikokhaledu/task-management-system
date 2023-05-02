# Task Management API

This project is a simple task management system implemented using Flask, SQLAlchemy, and SQLite. It provides a RESTful API for managing tasks, including creating, reading, updating, and deleting tasks.

## Getting Started
### Prerequisites
To set up the development environment, you will need to have the following software installed:
* Python 3.8 or higher
* pip (Python package installer)

## Setting up the development environment

* Clone the repository to your local machine:

```bash
git clone https://github.com/kikokhaledu/task-management-system.git
```
* Change to the project directory:

```bash
cd task-management-system
```
* Create a virtual environment:

```bash
python3 -m venv venv
```
* Activate the virtual environment On macOS and Linux:

```bash
source venv/bin/activate
```
* On Windows:

```bash
.\venv\Scripts\activate
```
in case  you face any issues running on windows run the following command 

```bash 
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
``` 

* Install the required packages:

```bash
pip install -r requirements.txt
```
## Running the API server
To start the development server, run the following command:

```bash
python app.py
```
The API server will start on http://127.0.0.1:5000/.

## Running the unit tests
To execute the unit tests, run the following command:

```bash
python -m unittest test_app.py
```
## API Endpoints
The following API endpoints are available for managing tasks:

* GET /tasks: Retrieve a list of all tasks, optionally filtered by status and/or priority.
* POST /tasks: Create a new task with the provided data.
* GET /tasks/<task_id>: Retrieve a single task by its ID.
* PUT /tasks/<task_id>: Update an existing task with the provided data.
* DELETE /tasks/<task_id>: Delete a task by its ID.

## Design Choices and Challenges

The task management system was implemented using Flask due to its simplicity and ease of use for small-scale projects. SQLAlchemy was chosen as the ORM for its versatility and support for various databases.

The main design challenge was handling the filtering of tasks by status and priority, as well as ensuring that only valid statuses and priorities are accepted. To address this, the constants.py module contains the allowed statuses and priorities, which are used in various functions to validate the input.

Another challenge was designing the Task model and handling various fields, such as status, priority, and due_date. The due_date field required special handling to parse the date string into a datetime object.

The unit tests in test_app.py cover the main functionalities of the API, ensuring that the CRUD operations work as expected. These tests help to catch potential issues in the application's logic.

Overall, the project demonstrates a basic task management system with a RESTful API, providing a foundation for further development and enhancement.