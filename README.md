SkinSense — AI-Powered Skin Analysis & Recommendation API

SkinSense is a REST API that lets users upload a facial image and receive an AI-generated skin analysis along with tailored skincare recommendations. It combines Google Vision API for image analysis and the Gemini API for generating structured, personalized care plans.

Live API: https://skinsense-cb78.onrender.com/ (Hosted on Render's free tier — the instance spins down after inactivity, so the first request after idle time may take 30-50 seconds to respond.)

Tech Stack
Backend: Python, Django, Django REST Framework
Database: PostgreSQL
Authentication: JWT (djangorestframework-simplejwt)
AI Integration: Google Vision API, Gemini API
Image Handling: Pillow
Deployment: Render
Prerequisites

Before running this project locally, you'll need:

Python 3.x installed
PostgreSQL installed and running locally
A Google Cloud account with the Cloud Vision API enabled, and an API key
A Gemini API key (via Google AI Studio)
Setup (Local Development)
Clone the repository:
bash
   git clone https://github.com/PoonamBanga/SkinSense.git
   cd SkinSense
Create and activate a virtual environment:
bash
   python -m venv venv
   venv\Scripts\activate   # Windows
Install dependencies:
bash
   pip install -r requirements.txt
Create a .env file in the project root with the following:
   GEMINI_API_KEY=your_gemini_key_here
   VISION_API_KEY=your_vision_key_here
   DB_NAME=skinsense_db
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
Create the PostgreSQL database:
sql
   CREATE DATABASE skinsense_db;
Run migrations:
bash
   python manage.py migrate
Create a superuser (for testing authenticated endpoints):
bash
   python manage.py createsuperuser
Start the development server:
bash
   python manage.py runserver
API Endpoints
Method	Endpoint	Description	Auth Required
GET	/	API welcome message and endpoint map	No
POST	/api/register/	Create a new user account	No
POST	/api/token/	Obtain JWT access & refresh tokens	No
POST	/api/token/refresh/	Refresh an expired access token	No
POST	/api/scan/	Upload an image and receive skin analysis	Yes
GET	/api/scans/	Retrieve the logged-in user's scan history	Yes
Example: Register a new user
POST /api/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "yourpassword"
}
Example: Upload a scan
POST /api/scan/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

Body: image=<file>

Response:

json
{
  "id": 1,
  "user": 1,
  "image": "/media/scans/example.jpg",
  "vision_output": { "labels": ["skin", "face", "..."] },
  "recommendation": { "text": "..." },
  "created_at": "2026-07-28T22:20:00Z"
}
Testing

Endpoints were tested using Postman, given the project's API-only structure (no frontend). A typical test flow: register a user via /api/register/, obtain a JWT via /api/token/, then use that token to authenticate a POST request to /api/scan/ with an image attached as form-data.

The live deployment on Render was also tested end-to-end via Postman against the production URL.

Notes on the AI Integration
Gemini API is fully integrated and live — it generates the structured skincare recommendations (severity assessment, care plan, red flags) based on detected image labels.
Vision API integration is fully implemented using ImageAnnotatorClient, but currently runs against mocked label data during development, pending Google Cloud billing account activation. The code path is identical to a live call — swapping in real credentials requires no changes downstream.
Status

Core functionality is complete and deployed: user registration, JWT authentication, image upload with validation, AI-generated analysis and recommendations, persisted scan history per user, and a live production deployment on Render. Planned next: activate live Vision API billing, migrate from the deprecated google-generativeai package to google-genai, and expand automated test coverage.
