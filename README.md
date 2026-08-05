# Clinic Manager (Flask)

A simple clinic management web app built with Python + Flask + SQLite.
It manages **Doctors**, **Patients**, and **Appointments**.

## Features
- Dashboard with quick stats and upcoming appointments
- Add / delete patients
- Add / delete doctors
- Book appointments (linking a patient + doctor + date/time)
- Mark appointments as Completed / Cancelled
- SQLite database (auto-created on first run, no setup needed)

## Project structure
```
clinic_app/
├── app.py                  # Main Flask app (routes + models)
├── requirements.txt
├── templates/               # HTML pages (Jinja2 + Bootstrap 5)
│   ├── base.html
│   ├── index.html
│   ├── patients.html
│   ├── add_patient.html
│   ├── doctors.html
│   ├── add_doctor.html
│   ├── appointments.html
│   └── add_appointment.html
└── static/
    └── style.css
```

## How to run

1. Open the `clinic_app` folder in PyCharm (or any editor), or `cd` into it in a terminal.

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python app.py
```

5. Open your browser at:
```
http://127.0.0.1:5000
```

The database file `clinic.db` will be created automatically in the project folder
the first time you run the app.

## Suggested next steps (if you want to extend it)
- Add login/authentication for staff
- Add search/filter for patients and appointments
- Add prescriptions or medical history per patient
- Deploy it (Render, Railway, PythonAnywhere) once you're happy with it locally
