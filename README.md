Task Manager API

This is a Django REST Framework project with JWT authentication and role-based access (Admin and User).
Users can manage their own tasks, and Admin can view all tasks.

Setup

Clone the project
git clone <repo-url>

Create virtual environment
python3 -m venv env_task
source env_task/bin/activate (Linux / Mac)
env_task\Scripts\activate (Windows)

cd task_manager

Install dependencies
pip install -r requirements.txt

Run migrations
python3 manage.py migrate (No Need as i have attched sqlite file containing data)

Start server
python3 manage.py runserver

URL with swagger : http://127.0.0.1:8000/swagger

Authentication

Credentials : 
Admin : 
email : admin@gmail.com
password : Password@123

Users : 
email : user1@gmail.com
email : user2@gmail.com
email : user3@gmail.com

password : Password@123

Login to get JWT token and send it in header:

Authorization: Bearer <token>

Main APIs

User APIs
POST /users_registration/ -> create user
GET /users_registration/ -> list users
GET /users_registration/{id}/ -> get user
POST /admin_login/ -> admin login
POST /user_login/ -> user login



Task APIs (User role)
POST /tasks_management/ → create task
GET /tasks_management/ → list own tasks
GET /tasks_management/{id}/ → get task
PUT /tasks_management/{id}/ → update task
DELETE /tasks_management/{id}/ → delete task

Admin API
GET /task_list_admin/ → list all tasks



Run Tests

Run all tests
pytest -v

Run specific file
pytest accounts/tests.py -v

Run single test
pytest accounts/tests.py::test_user_registration_success -v

When tests run, a temporary test database is created and deleted automatically.

Roles
Admin → can view all tasks
User → can manage only their own tasks
