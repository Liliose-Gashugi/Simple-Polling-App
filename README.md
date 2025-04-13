# Simple Polling App
A web-based polling platform built with Django and Django REST Framework. Users can create polls, vote on choices, and view poll results through a clean API. The system allows creation, listing, and vote for polls and choices, along with real-time voting features.

---

## Features

- List all available polls
- View poll details with choices
- View voting results for each poll

---

## Technologies used
- Backend: Django + Django REST Framework
- Database: SQLite
- API Testing: Postman

---

## Installation
    # Prerequisites
Python 3.x
pip

---

## API Endpoints

# Polls
- GET /api/polls/ - List all polls
- POST /api/polls/ - Create a new poll with choices
- GET /api/polls/<int:pk>/ - Get details of a specific poll


# Voting
POST /polls/api/vote/<int:choice_id>/


# Results
GET /polls/api/questions/<int:poll_id>/


## Repository
https://github.com/Liliose-Gashugi/Simple-Polling-App.git