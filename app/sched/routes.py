# app>sched>routes.py
from app import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.sched import appointment
from app.sched.models import Appointment
from app.sched.forms import AppointmentForm


@appointment.route('/appointment/')
@login_required
def appointment_list():
    appts = Appointment.query.filter_by(
        user_id=current_user.id).order_by(Appointment.start.asc()).all()
    if not appts:
        flash('You don\' have any appointments. Please create one!')
        return redirect(url_for('appointment.create_appointment'))
    return render_template('sched.html', appts=appts, user_id=current_user.id, user_name=current_user.user_name.title())


@appointment.route('/appointment/create/', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentForm()

    if form.validate_on_submit():
        appointment = Appointment(
            title=form.title.data,
            start=form.start.data,
            end=form.end.data,
            allday=form.allday.data,
            location=form.location.data,
            description=form.description.data,
            user_id=current_user.id)

        db.session.add(appointment)
        db.session.commit()

        flash('Appointment added successfully!')

        return(redirect(url_for('appointment.appointment_list')))
    return render_template('create_appt.html', form=form)


@appointment.route('/appointment/edit/<appt_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    form = AppointmentForm(obj=appt)
    if form.validate_on_submit():
        appt.title = form.title.data
        appt.start = form.start.data
        appt.end = form.end.data
        appt.allday = form.allday.data
        appt.location = form.location.data
        appt.description = form.description.data

        db.session.add(appt)
        db.session.commit()

        flash('Apointment edited successfully!')
        return(redirect(url_for('appointment.appointment_list')))
    return render_template('edit_appt.html', form=form)


@appointment.route('/appointment/delete/<appt_id>', methods=['GET', 'POST'])
@login_required
def delete_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if request.method == 'POST':
        db.session.delete(appt)
        db.session.commit()
        flash("Appointment deleted successfully!")
        return redirect(url_for('appointment.appointment_list'))

    return render_template('delete_appt.html', appt=appt)
