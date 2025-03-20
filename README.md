# Django-lrlms
This is a basic library management system.

📌 Brief Summary of What We Did & Changed Files
Here’s a structured summary of what we did to set up your Django Library Management System (LMS) and push it to GitHub.

🔹 1. Django Project & Database Setup
✅ Created a Django project (lms_project)
✅ Configured MySQL as the database
File Modified: lms_project/settings.py
Added DATABASES configuration for MySQL
Set AUTH_USER_MODEL = 'library.User'


🔹 2. Created & Updated Models
✅ Defined models for Users, Books, Issues, Reservations, Transactions
✅ Added Instructor role and different borrowing limits:
Students: 2 books for 2 weeks
Instructors: 5 books for 4 weeks
✅ Fixed AbstractUser conflicts (related_name added for groups & permissions)
File Modified: library/models.py

🔹 3. Fixed Migration Issues
✅ Reset migration history due to inconsistencies
Deleted old migrations: rm -rf library/migrations/
Deleted migration records in MySQL
Ran:
python manage.py makemigrations library
python manage.py migrate --fake-initial
File Modified: library/migrations/

🔹 4. GitHub Repository & Git Issues Fixed
✅ Removed old .git and reinitialized Git
rm -rf .git
git init
✅ Connected to the correct GitHub repository (Django-lms)
git remote add origin git@github.com:devanshuparmar/Django-lms.git
✅ Fixed issues with remote tracking and branch conflicts
Created WIP branch
Synced local & remote changes using:
git fetch origin
git pull origin WIP --rebase
git push -u origin WIP
No specific files changed, but Git tracking was reset.

📌 Flagged Files That Were Changed
File	Changes Made
lms_project/settings.py	Configured MySQL, set custom user model
library/models.py	Defined all models, added instructor role, fixed user model conflicts
library/migrations/	Old migrations deleted & re-applied
.gitignore (if exists)	May need to check if migrations were ignored
.git (not a file, but the entire Git tracking was reset)	Git repo was reinitialized and reconnected to GitHub

🚀 Next Steps
1️⃣ Confirm everything works with python manage.py runserver
2️⃣ Check if your GitHub repo (WIP branch) has all changes.
3️⃣ Would you like me to generate documentation (README.md) for your project? 🚀
