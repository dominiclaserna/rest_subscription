Subscription API
A simple REST API built with Flask and Flask-RESTX for managing:

**Users**
**Products**
**Subscriptions**

Data is stored in SQLite.

------------------------------------------------------------
API Endpoints
**Users**
POST /api/v1/users
Create a new user

GET /api/v1/users
List all users

GET /api/v1/users/<id>
Get user by ID

PUT /api/v1/users/<id>
Update user

PUT /api/v1/users/<id>
Update user
------------------------------------------------------------
**Products**
POST /api/v1/products
Create a new product

GET /api/v1/products
List all products
------------------------------------------------------------
**Subscriptions**
POST /api/v1/subscriptions
Create a new subscription

Requires valid username and product_id

GET /api/v1/subscriptions
List all subscriptions

PUT /api/v1/subscriptions/<id>
Update subscription

DELETE /api/v1/subscriptions/<id>
Unsubscribe a user
