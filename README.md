Here's the updated README file with the inclusion of instructions for setting up and using a virtual environment (.venv):
EduConnect
Overview

EduConnect is a Django-based API designed to connect schools and teachers by allowing schools to post teaching jobs that teachers can apply for. This project simplifies the recruitment process for schools and helps teachers find opportunities that match their qualifications and preferences.
Features

    User authentication and authorization (registration, login, logout, account deletion).
    Schools can post teaching jobs.
    Teachers can browse and apply for jobs.
    CRUD operations for job postings, applications, and user profiles.
    Search functionality using Django REST Framework's SearchFilter.
    Session-based authentication.

Technologies Used

    Backend Framework: Django, Django REST Framework
    Database: MySQL
    Search: Django REST Framework's SearchFilter
    Authentication: Session-based with Django's built-in login/logout
    Others: MySQL client for database management

Project Architecture

    Single app: API
    Models:
        CustomUser: One-to-one relationships with Schools and Teachers
        School: Manages job postings
        Teacher: Applies for jobs
        Job: Associated with a School
        Application: Associated with a Job and Teacher
    Endpoints:
        # /teachers/ – Retrieve and create teacher profiles
        # /teachers/<int:pk>/ – Retrieve a specific teacher profile
        # /teacher-profile/ – Retrieve the current logged-in teacher’s profile
        # /schools/ – Retrieve all schools
        # /schools/<int:pk>/ – Retrieve or update a specific school profile
        # /school-profile/ – Retrieve the current logged-in school’s profile
        # /all_jobs/ – Retrieve all job postings
        # /jobs/ – Create or retrieve job postings
        # /jobs/<int:pk>/ – Retrieve, delete or update a specific job posting
        # /applications/ – Create or retrieve applications
        # /applications/<int:pk>/ – Retrieve, delete or update a specific application
        # /all-applications/ – Retrieve all applications for administrative purposes
        # /school-applications/ – Retrieve applications for jobs posted by the current logged-in school
        # /jobs/search/ – Search for job postings
        # /job-postings/search/ – Advanced search for job postings
        # /applications/search/ – Search for applications

Installation and Setup

    Clone the repository

git clone <repository-url>  
cd educonnect  

Set up a virtual environment

python -m venv .venv  
source .venv/bin/activate  # On Windows: .venv\Scripts\activate  

Install dependencies

pip install -r requirements.txt  

Set up the database

python manage.py makemigrations  
python manage.py migrate  

Run the development server

    python manage.py runserver  

Examples:
register:
as school
    url: /api/register/
    data: {
        "username": "schoolUser22",
        "password": "schoolUser22pwd",
        "user_type": "school",
        "name": "bright academy",
        "locations": "Juba"
    }
    login:
url: /api/login/
    data: {
        "username": "schoolUser22",
        "password": "schoolUser22pwd"
    }
as school
    data: {
        "username": "teacherUser22",
        "password": "teacherUser22pwd",
        "user_type": "teacher",
        "subject_expertise": "math",
        "qualifications": "University graduate",
        "email": "teacherUser22@gmail.com"
    }

login:
url: /api/login/
    data: {
        "username": "teacherUser22",
        "password": "teacherUser22pwd"
    }


Development Highlights

Successes

    Implemented robust authentication and authorization.
    Developed a seamless user experience for schools and teachers.
    Completed CRUD operations for jobs, applications, and profiles.

Challenges

    Managing multiple user types with a single User model.
    Enhanced search functionality using SearchFilter.

Areas for Improvement

    Adding Elasticsearch for advanced search.
    Deployment and comprehensive testing are pending.

Lessons Learned

    Building an API from scratch.
    Mastery of Django and Django REST Framework.

Next Steps

    Deploy the API to a production environment.
    Develop a frontend interface for a complete user experience.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request with detailed notes.
