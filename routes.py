# routes.py (partial)
from flask import render_template, url_for, flash, redirect, request
from .forms import FacultyForm # You'd create this form with WTForms
from . import app, db
from .models import Faculty
from flask_login import current_user, login_required

@app.route("/admin/add_faculty", methods=['GET', 'POST'])
@login_required # Assume you have an admin login system
def add_faculty():
    # Only allow admin to access this page
    if not isinstance(current_user, Admin):
        return redirect(url_for('login')) # Redirect to a generic login page

    form = FacultyForm()
    if form.validate_on_submit():
        # Hash the password before saving
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        faculty = Faculty(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(faculty)
        db.session.commit()
        flash('Faculty added successfully!', 'success')
        return redirect(url_for('view_faculties'))
    return render_template('admin/add_faculty.html', form=form)