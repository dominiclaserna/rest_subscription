REST Subscription API

Activity Summary
Objective: Create a RESTful API using Python Flask that handles subscription-based logic for business products. This includes CRUD operations for both Products and Subscriptions.

API Responsibilities

Product

POST /products – Add a new product

GET /products – View all available products

Subscription

POST /subscriptions – Record a new user subscription

PUT /subscriptions/<id> – Update/renew a subscription

Updates status to Subscribed on renewal

GET /subscriptions – View all user subscriptions

DELETE /subscriptions/<id> – Unsubscribe a user

[View Testing Documentation](./TESTING.pdf)
