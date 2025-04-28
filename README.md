# RoomMate

RoomMate is a web-based roommate matching platform developed for CPTS 322 – Software Engineering Principles.  
With an easy signup and preference selection, you can find a roommate who won't make you regret life — with ease!

Developed by:
- Josh Anthony Santiago
- Gaynay Doo
- Cayden Calo
---

## 🚀 Features

- **User Registration** — Create an account with a username, email, and password.
- **Profile Management** — Add age, gender, bio, and social media links (Instagram, Snapchat).
- **Preference Setting** — Define your preferences for smoking, pets, noise level, and sleep schedule.
- **Match Searching** — Automatically view a ranked list of roommate matches based on shared preferences.
- **Match Requests** — Send and confirm match requests between users.
- **Contact Sharing** — Only after mutual confirmation can users view each other's social media contact information.
- **Edit Preferences** — Users can update their profile and preferences at any time.
- **Authentication System** — Secure login and logout functionality using Django's auth system.

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, Bootstrap 5
- **Backend:** Django 4.2 (Python)
- **Database:** SQLite3 (default Django database)
- **Authentication:** Django's built-in auth system

---

## ⚙️ Project Setup Instructions
**Important: Please note that if using WSL or any Linux distro, you may have to use python3 instead of python in the command line.**

### 1. Clone the repository
```bash
git clone https://github.com/your-username/RoomMate.git
cd RoomMate
```

### 2. (Optional) Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

```
### 3. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the development server
```bash
python manage.py runserver
```

### 6. Access the application
Open your browser and go to:
```
http://127.0.0.1:8000/
```

---

## 📚 License
This project was developed for educational purposes for Washington State University, CPT_S 322 — Software Engineering Principles, instructed by Parteek Kumar.
All rights reserved to the developers.
