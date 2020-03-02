# Udacity Full Stack Development Nanodegree

This is the project for **Identity and Access Management** of Udacity's Full Stack Development Nanodegree

---

## Up & Running

### Build Images

The building of frontend would take some time because of npm install. Grab a coffee and have a break before you continue!

```bash
docker-compose build
```

### Initialize Database

#### Identify Backend Instance

First, identify backend instance by typing the following command. Select the one whose name contains **backend**

```bash
docker ps -a
```

<img src="doc/services.png" alt="Services"/>

#### Restore Database

Then, enter the instance and initialize DB data by typing:

```bash
# enter backend instance:
docker exec -it workspace_backend_1_ab7efdf943c8 bash
# init db:
flask init-db
```

### Check Host Ports

Make sure the following ports are not used on local host:
* **localhost:58100** This port will be used by frontend APP
* **localhost:50080** This port will be used by backend for easy debugging
* **localhost:58080** This port will be used by PG adminer for easy database administration

### Launch

Launch the system using docker-compose. Note: 

* The frontend and the backend will communicate using host network
* The backend will communicate with PGSQL DB using docker compose internal network

```bash
docker-compose up
```

---

## API Endpoints



---

## Testing

### Overview

All the 5 API endpoints are covered by test cases. For the drinks resource, the coverage rate is 86%. See [Python Unittest Testcases](workspace/backend/tests) and [POSTman Testcases](workspace/backend/tests/postman) for details.

### Python Unittest Up & Running

First, identify backend instance by typing the following command. Select the one whose name contains **backend**

```bash
docker ps -a
```

<img src="doc/services.png" alt="Services"/>

Then, enter the instance and execute the tests by typing:

```bash
# enter backend instance:
docker exec -it workspace_backend_1_ab7efdf943c8 bash
# run tests:
flask test
```

Test coverage analysis is also enabled. Use the following command to get the coverage analysis report:
```bash
# inside backend instance, type:
flask test --coverage=True
```

<img src="doc/test-coverage.png" alt="Test Coverage"/>

### POSTman Testcases Up & Running

The test runner and the results for the three roles(public, barista and manager) are all kept in [POSTman Testcases](workspace/backend/tests/postman)

---

## Review

### Flask Server Setup

#### The Complete Project Has Been Submitted as a Zip and Demonstrates the Ability to Share Code on git

The whole project is under version control of git.

#### The Project Demonstrates Coding Best Practices

The whole project follows the structure recommended by [Flask Mega Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)

#### The Project Demonstrates an Understanding of RESTful APIs

* GET /drinks
    [here](TBD)

* GET /drinks-detail
    [here](TBD)

* POST /drinks
    [here](TBD)

* PATCH /drinks/<id>
    [here](TBD)

* DELETE /drinks/<id>
    [here](TBD)

#### The Project Demonstrates the Ability to Build a Functional Backend

The APP is served by production ready uwsgi + nginx server in Docker. Ready for both functionality and production deployment.

### Secure a REST API for Applications

#### The Project Demonstrates an Understanding of Third-Party Authentication Systems

Test configuration of Auth0 is available at [here](TBD)

#### The Project Demonstrates an Understanding of JWTs and Role Based Authentication

The JWT based authentication and RBAC logics are implemented at [here](TBD)

#### The Project Demonstrates the Ability to Secure a System through an Understanding of Roles-Based Access Control (RBAC)

Below are the permissions assigned for the APP:

<img src="doc/auth0-permissions.png" alt="Permissions"/>

Below are the roles and their associations with permissions for the APP:

<img src="doc/auth0-roles-overview.png" alt="Roles"/>

<img src="doc/auth0-role-barista-details.png" alt="Role Barista"/>

<img src="doc/auth0-role-manager-details.png" alt="Role Manager"/>

Below are the users and their associations with roles for the APP:

<img src="doc/auth0-users-overview.png" alt="Roles"/>

<img src="doc/auth0-user-customer-details.png" alt="Role Barista"/>

<img src="doc/auth0-user-barista-details.png" alt="Role Manager"/>

<img src="doc/auth0-user-manager-details.png" alt="Role Manager"/>

POSTman test results are available at:

* [Public](workspace/backend/tests/postman/udacity-fsnd-udaspicelatte.postman_test_run_role_public.json)
* [Barista](workspace/backend/tests/postman/udacity-fsnd-udaspicelatte.postman_test_run_role_barista.json)
* [Manager](workspace/backend/tests/postman/udacity-fsnd-udaspicelatte.postman_test_run_role_manager.json)

### Frontend

#### The Project Demonstrates an Understanding of How to Loosely Uncouple Authentication and REST Services

The configuration of frontend is available at [Frontend Environment Config](workspace/frontend/src/environment/environment.ts)

#### The Project Demonstrates the Ability to Work across the Stack

The frontend can be run directly using docker-compose following the instructions in section Up & Running.
