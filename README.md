# Social Media API
This project is a backend API for a social media platform that supports user registration, 
authentication, profile management, following/unfollowing, post creation, 
and interactions such as likes and comments. Below is a detailed breakdown of the features 
and the development process.

## Features Implemented

### 1. **User Registration and Authentication**
- **Registration:** Users can register an account by providing their email and password. Validation ensures unique emails and strong passwords.
- **Login:** Users can log in with their credentials to receive an authentication token.

---

### 2. **User Profile Management**
- **Profile Creation and Updates:**
  - Users can create and update their profiles, including adding a profile picture, bio, and other personal details.
- **Profile Retrieval:**
  - Users can view their own profile and the profiles of other users.
- **Search Users:**
  - A search feature enables users to find others by firs_name or last_name.

---

### 3. **Follow/Unfollow Functionality**
- **Follow/Unfollow Users:**
  - Users can follow or unfollow other users to build a social network.
- **View Connections:**
  - Users can view the list of people they are following and those who follow them.

---

### 4. **Post Creation and Retrieval**
- **Post Creation:**
  - Users can create posts with text content. Optional media attachments, such as images, can also be added.
- **Retrieve Posts:**
  - Users can retrieve their own posts or posts from users they follow.
- **Hashtag Search:**
  - Posts can be filtered and retrieved using hashtags or specific search criteria.

---

### 5. **Likes and Comments (Optional)**
- **Like/Unlike Posts:**
  - Users can like and unlike posts. A list of liked posts is available for viewing.
- **Comment on Posts:**
  - Users can add comments to posts and view the comment threads.

---

### 6. **API Permissions and Security**
- **Action Restrictions:**
  - Only authenticated users can perform actions like creating posts, following users, liking posts, and commenting.
- **Ownership Control:**
  - Users can update or delete only their own posts, comments, and profiles.
- **Token-Based Authentication:**
  - Ensures secure access to API endpoints.

---

### 7. **API Documentation**
- **Comprehensive Documentation:**
  - The API is fully documented with clear instructions for each endpoint.

### Technical Requirements:
1. Django and Django REST framework to build the API.
2. Token-based authentication for user authentication.
3. Used serializers for data validation and representation.
4. Used views and viewsets for handling CRUD operations on models.
5. Used URL routing for different API endpoints.
6. Used default and custom permissions and authentication classes to implement API permissions.
7. Implemented design and documentation RESTful API by Swagger.


## Installation

Follow these steps to set up and run the project locally:

- Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/social-media-api.git
cd social-media-api
```
- Create a virtual environment for Python dependencies:
```bash
python -m venv venv
```
- Activate the virtual environment:
```bash
venv\Scripts\activate #for Windows
source venv/bin/activate #for macOS/Linux
```
- Install the required dependencies:
```bash
pip install -r requirements.txt
```
- Copy .env.sample > .env and populate with all required data
- run migrations
```bash
python manage.py migrate
```
- Create an admin account for the Django admin panel:
```bash
python manage.py createsuperuser
```
- Start the Django development server:
```bash
python manage.py runserver
```
