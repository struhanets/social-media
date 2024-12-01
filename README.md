# Social Media API

### Requirements
## User Registration and Authentication:
1. Users should be able to register with their email and password to create an account.
2. Users should be able to login with their credentials and receive a token for authentication.
3. Users should be able to logout and invalidate their token.

### User Profile:
1. Users should be able to create and update their profile, including profile picture, bio, and other details.
2. Users should be able to retrieve their own profile and view profiles of other users.
3. Users should be able to search for users by username or other criteria

### Follow/Unfollow:
1. Users should be able to follow and unfollow other users.
2. Users should be able to view the list of users they are following and the list of users following them.

### Post Creation and Retrieval:
1. Users should be able to create new posts with text content and optional media attachments (e.g., images). 
(Adding images is optional task)
2. Users should be able to retrieve their own posts and posts of users they are following.
3. Users should be able to retrieve posts by hashtags or other criteria.

### Likes and Comments (Optional):
1. Users should be able to like and unlike posts. Users should be able to view the list of posts they have liked. 
2. Users should be able to add comments to posts and view comments on posts.

### Schedule Post creation using Celery (Optional):
1. Add possibility to schedule Post creation (you can select the time to create the Post before creating of it)

### API Permissions:
1. Only authenticated users should be able to perform actions such as creating posts, 
liking posts, and following/unfollowing users.
2. Users should only be able to update and delete their own posts and comments.
3. Users should only be able to update and delete their own profile.

### API Documentation:
1. The API should be well-documented with clear instructions on how to use each endpoint.
2. The documentation should include sample API requests and responses for different endpoints.

### Technical Requirements:
1. Use Django and Django REST framework to build the API.
2. Use token-based authentication for user authentication.
3. Use appropriate serializers for data validation and representation.
4. Use appropriate views and viewsets for handling CRUD operations on models.
5. Use appropriate URL routing for different API endpoints.
6. Use appropriate permissions and authentication classes to implement API permissions.
7. Follow best practices for RESTful API design and documentation.

Note: You are not required to implement a frontend interface for this task. 
Focus on building a well-structured and well-documented RESTful API using Django and Django REST framework. 
This task will test the junior DRF developer's skills in building RESTful APIs, 
handling authentication and permissions, working with models, serializers, views, and viewsets, 
and following best practices for API design and documentation.