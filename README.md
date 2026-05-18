Since your **Online Job Portal (EasyJob)** is one of your main projects and you want it to look strong on GitHub/resume, here’s a **professional README.md** with a clean structure, good wording, and features matching your actual project (resume screening, aptitude test, HR approval, offer letter, etc.).

You can directly copy-paste this into `README.md`.

````md
# EasyJob – Smart Online Job Portal

## Overview

EasyJob is an intelligent web-based job portal developed to simplify the recruitment process for both candidates and HR professionals. The platform enables candidates to search and apply for jobs, upload resumes, attempt aptitude assessments, and track application status.

For recruiters, EasyJob provides tools to post job openings, review applications, analyze resume-job skill matching, conduct screening tests, and manage candidate selection efficiently.

The platform integrates resume parsing, skill matching, automated aptitude testing, and offer letter generation to create a complete hiring ecosystem.

---

## Key Features

### Candidate Module
- User registration and secure login
- Browse available job opportunities
- Apply for jobs with resume upload
- Resume skill extraction and matching
- Track application status
- Online aptitude assessment
- View test progress and outcomes

### HR Module
- HR registration and admin approval system
- Post new job openings
- Edit or delete job listings
- View candidate applications
- Resume screening and analysis
- Skill matching percentage
- Approve or reject applicants
- Final candidate selection

### Admin Module
- Manage HR approvals
- View registered candidates
- Remove users
- System-level access and management

### Smart Resume Analysis
- PDF resume parsing
- Automatic skill extraction
- Resume-job skill comparison
- Matching percentage calculation
- Resume summary generation

### Online Assessment
- Aptitude-based MCQ examination
- Multiple sections:
  - Logical Reasoning
  - General Knowledge
  - English
  - Mathematics
  - Technical Questions
- Randomized questions
- Score calculation

### Offer Letter Generation
- Automatic PDF offer letter creation
- Candidate name inclusion
- Company name
- Job role/title
- Stipend and CTC details
- Email delivery with attachment

### Email Notification System
- Selection emails
- Rejection emails
- Offer letter attachment
- Automated communication

---

## Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Logic |
| Flask | Web Framework |
| SQLite | Database |
| HTML | Frontend Structure |
| CSS | Styling |
| JavaScript | Interactivity |
| PDFMiner | Resume Text Extraction |
| ReportLab | PDF Offer Letter Generation |
| SMTP | Email Services |

---

## System Architecture

The EasyJob platform follows a role-based workflow:

### Candidate Workflow
1. Register/Login
2. Browse available jobs
3. Upload resume
4. Resume skill analysis
5. HR screening
6. Aptitude test
7. Result evaluation
8. Final selection/rejection

### HR Workflow
1. Register as HR
2. Wait for admin approval
3. Post jobs
4. Review applications
5. Analyze skill matching
6. Approve candidates
7. Conduct assessment
8. Final candidate selection

### Admin Workflow
1. Login to admin panel
2. Approve or reject HR accounts
3. Manage users

---

## Project Screenshots

Add screenshots here after uploading them.

### Home Page
![Home Page](screenshots/home.png)

### Candidate Dashboard
![Candidate Dashboard](screenshots/candidate.png)

### HR Dashboard
![HR Dashboard](screenshots/hr.png)

### Resume Analysis
![Resume Analysis](screenshots/resume.png)

---

## Folder Structure

```text
EasyJob/
│── static/
│   ├── images/
│   ├── resumes/
│   ├── offers/
│   └── style.css
│
│── templates/
│   ├── home.html
│   ├── admin.html
│   ├── hr.html
│   ├── candidate.html
│   ├── applications.html
│   ├── job_details.html
│   ├── test.html
│   └── resume_details.html
│
│── easyjob.db
│── app.py
│── requirements.txt
│── README.md
````

---

## Installation Guide

### Clone Repository

```bash
git clone https://github.com/yourusername/easyjob.git
```

### Navigate to Project

```bash
cd easyjob
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask
pip install pdfminer.six
pip install reportlab
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Default Admin Credentials

```text
Email: admin@easyjob.com
Password: admin123
```

---

## Security Features

* Password hashing using SHA-256
* Session-based authentication
* Role-based access control
* Duplicate job application prevention
* Strong password validation during registration
* Gmail format validation

---

## Future Enhancements

The following improvements can be added in future versions:

* AI-powered resume ranking
* Video interview integration
* Real-time interview scheduling
* Email OTP verification
* Chat system between HR and candidates
* Job recommendation system
* Admin analytics dashboard
* Mobile responsive UI
* Cloud database integration

---

## Advantages

* Simplifies recruitment workflow
* Reduces manual screening effort
* Improves hiring efficiency
* Faster candidate filtering
* Transparent recruitment process
* Better candidate experience

---

## Conclusion

EasyJob provides a modern and intelligent approach to online recruitment by combining resume screening, skill matching, aptitude assessment, and automated hiring workflows into a single platform. The system improves efficiency for recruiters while giving candidates a smooth and transparent hiring experience.

---

## Author

**Hruthik R Salian**
Bachelor of Technology – Computer Science and Engineering

---

## License

This project is developed for educational and academic purposes.

```

This README will look **professional on GitHub**, especially for placements and portfolio. It feels like a real software product instead of a college mini-project.
```
