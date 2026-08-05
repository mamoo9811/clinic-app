from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-secret-key'

db = SQLAlchemy(app)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    notes = db.Column(db.Text)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled / Completed / Cancelled


# ---------------------------------------------------------------------------
# Home / Dashboard
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    today = date.today()
    today_appointments = Appointment.query.filter_by(appointment_date=today).count()
    upcoming = (Appointment.query
                .filter(Appointment.appointment_date >= today)
                .order_by(Appointment.appointment_date, Appointment.appointment_time)
                .limit(5).all())
    return render_template('index.html',
                            total_patients=total_patients,
                            total_doctors=total_doctors,
                            today_appointments=today_appointments,
                            upcoming=upcoming)


# ---------------------------------------------------------------------------
# Patients
# ---------------------------------------------------------------------------

@app.route('/patients')
def patients():
    all_patients = Patient.query.order_by(Patient.name).all()
    return render_template('patients.html', patients=all_patients)


@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = Patient(
            name=request.form['name'],
            age=request.form.get('age') or None,
            phone=request.form.get('phone'),
            notes=request.form.get('notes')
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully.', 'success')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')


@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted.', 'success')
    return redirect(url_for('patients'))


# ---------------------------------------------------------------------------
# Doctors
# ---------------------------------------------------------------------------

@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('doctors.html', doctors=all_doctors)


@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        doctor = Doctor(
            name=request.form['name'],
            specialty=request.form['specialty'],
            phone=request.form.get('phone')
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully.', 'success')
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html')


@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted.', 'success')
    return redirect(url_for('doctors'))


# ---------------------------------------------------------------------------
# Appointments
# ---------------------------------------------------------------------------

@app.route('/appointments')
def appointments():
    all_appointments = (Appointment.query
                         .order_by(Appointment.appointment_date, Appointment.appointment_time)
                         .all())
    return render_template('appointments.html', appointments=all_appointments)


@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    all_patients = Patient.query.order_by(Patient.name).all()
    all_doctors = Doctor.query.order_by(Doctor.name).all()

    if request.method == 'POST':
        appt_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        appointment = Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            appointment_date=appt_date,
            appointment_time=request.form['appointment_time'],
            reason=request.form.get('reason'),
            status='Scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully.', 'success')
        return redirect(url_for('appointments'))

    return render_template('add_appointment.html', patients=all_patients, doctors=all_doctors)


@app.route('/appointments/status/<int:appointment_id>/<string:new_status>', methods=['POST'])
def update_status(appointment_id, new_status):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = new_status
    db.session.commit()
    flash(f'Appointment marked as {new_status}.', 'success')
    return redirect(url_for('appointments'))


@app.route('/appointments/delete/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted.', 'success')
    return redirect(url_for('appointments'))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
