from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, flash, jsonify, make_response
from database import *
from sqlalchemy.exc import IntegrityError
import json
import argon2
import os
from functools import wraps
from datetime import datetime
from EncryptDecrypt import EnDecrypt
from sms import send_message, send_email
import random


STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
SUBJECT_FILES_DIR = os.path.join(STATIC_DIR, 'subject_files')
key_path = os.path.join('static', 'keys', 'keys.json')
en_decrypt = EnDecrypt(key_path)

app = Flask(__name__)
app.secret_key = '__secret_key__'
app.config['UPLOAD_FOLDER'] = "static/subject_files"
ph = argon2.PasswordHasher()


def load_keys_from_json():
    with open(key_path, 'r') as f:
        admin_detail = json.load(f)
        email = admin_detail['admin']
        password = admin_detail['password']
    return email, password


def change_password_in_json(new_password):
    with open(key_path, 'r+') as f:
        admin_detail = json.load(f)
        admin_detail['password'] = new_password
        f.seek(0)
        json.dump(admin_detail, f, indent=4)
        f.truncate()


admin_email, admin_password = load_keys_from_json()
ROLES = {
    'student': ['home', 'notes', 'attendance', 'grades', 'placement'],
    'parent': ['get_student', 'home', 'notes', 'attendance', 'grades'],
    'teacher': ['teacher_index', 'notes', 'get_subjects_route', 'upload', 'grades', 'enter_grades', 'attendance',
                'enter_attendance', 'my_class', 'edit_student', 'remove_student'],
    'hod': ['hod_index', 'add_student', 'add_subject', 'update_subject', 'save'],
    'admin': ['admin_index', 'change_hod']
}


# Helper function to check if the user is logged in
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'data' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


# Helper function to check role-based access
def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            user_data = session.get('data')
            if user_data is None or 'user' not in user_data or user_data['user'] not in allowed_roles:
                return render_template('access_rejected.html'), 403  # Render access rejected page
            return func(*args, **kwargs)
        return decorated_function
    return decorator


@app.errorhandler(403)
def forbidden(error):
    return render_template('access_rejected.html'), 403


@app.route("/", methods=['GET', 'POST'])
def login():
    # Assuming session is a dictionary-like object
    if request.method == 'GET':
        session.clear()
        return render_template("login.html")
    else:
        data = request.form
        if data['user_type'] == 'student':
            register_number = data['register_number']
            department = data['department']
            password = data['password']
            # remember_me = data.get('remember_me')
            dept = get_department(department)
            student_detail = get_student_by_register_number(register_number, dept)
            if student_detail is None:
                flash("You do not have an account, Kindly Register!")
                return render_template('login.html')
            else:
                # if password == student_detail.password:
                try:
                    # Some data to send
                    ph.verify(student_detail.password, password)
                    data = {'register_number': register_number, 'department': department, 'user': 'student'}
                    # Store data in session
                    session['data'] = data
                    return redirect(url_for('home'))
                except argon2.exceptions.VerifyMismatchError:
                    flash('Password is wrong')
                    return render_template('login.html')
        elif data['user_type'] == 'parent':
            email = data['parent_email']
            password = data['password']
            phone_number = data['phone_number']
            parent_detail = get_parent_by_email(email)
            if parent_detail is None:
                flash("You do not have an account, Kindly Register!")
                return render_template('login.html')
            try:
                # Some data to send
                ph.verify(parent_detail.password, password)
                data = {'phone_number': phone_number, 'user': 'parent'}
                # Store data in session
                session['data'] = data
                return redirect(url_for('get_student'))
            except argon2.exceptions.VerifyMismatchError:
                flash('Password is wrong')
                return render_template('login.html')
        elif data['user_type'] == 'teacher':
            email = data['teacher_email']
            password = data['password']
            teacher_id = data['teacher_id']
            teacher_detail = get_teacher_by_email(email)
            if teacher_detail is None:
                flash("You do not have an account, Kindly Register!")
                return render_template('login.html')
            elif teacher_detail.teacher_id != teacher_id:
                flash("Your Teacher ID is wrong!")
                return render_template('login.html')
            else:
                try:
                    # Some data to send
                    ph.verify(teacher_detail.password, password)
                    data = {'teacher_id': teacher_id, 'user': 'teacher'}
                    # Store data in session
                    session['data'] = data
                    return redirect(url_for('teacher_index'))
                except argon2.exceptions.VerifyMismatchError:
                    flash('Password is wrong')
                    return render_template('login.html')
        elif data['user_type'] == 'admin':
            email = data['admin_email']
            password = data['password']
            if email == admin_email:
                try:
                    # Some data to send
                    ph.verify(admin_password, password)
                    data = {'user': 'admin'}
                    # Store data in session
                    session['data'] = data
                    return redirect(url_for('admin_index'))
                except argon2.exceptions.VerifyMismatchError:
                    flash('Password is wrong')
                    return render_template('login.html')
            else:
                flash('You are not the admin!')
                return render_template('login.html')
        else:
            teacher_id = data['hod_id']
            email = data['hod_email']
            password = data['password']
            hod_detail = get_hod_by_teacher_id(teacher_id)
            teacher_detail = get_teacher_by_email(email)
            if teacher_detail is None:
                flash("You do not have an Teacher account, Kindly Register!")
                return render_template('login.html')
            elif hod_detail is None:
                flash("You are not hod refrain yourself!")
                return render_template('login.html')
            else:
                try:
                    # Some data to send
                    ph.verify(teacher_detail.password, password)
                    data = {'teacher_id': teacher_id, 'user': 'hod', 'department': hod_detail.department}
                    # Store data in session
                    session['data'] = data
                    return redirect(url_for('hod_index'))
                except argon2.exceptions.VerifyMismatchError:
                    flash('Password is wrong')
                    return render_template('login.html')


@app.route("/forget_password/<user>", methods=['GET', 'POST'])
def forgot(user):
    if request.method == 'GET':
        session.clear()
    six_digit_number = random.randint(100000, 999999)
    if user == 'student':
        if request.method == 'POST':
            data = request.form
            dept = get_department(data['department'])
            student_detail = get_student_by_register_number(data['register_number'], dept)
            if student_detail is None:
                flash('No student has that register number.')
                return render_template('stu_forget.html')
            else:
                send_email(student_detail.email, six_digit_number)
                data = {'register_number': data['register_number'], 'department': data['department'], 'code_num':
                    str(six_digit_number), 'user': 'student'}
                # Store data in session
                session['code'] = data
                return render_template('code.html')
        return render_template('stu_forget.html')
    elif user == 'parent':
        if request.method == 'POST':
            data = request.form
            email = data['email']
            record = get_record_by_email(ParentUser, email)
            if record is None:
                flash('Your email is not registered.')
            else:
                send_email(email, six_digit_number)
                data = {'email': email, 'code_num': str(six_digit_number), 'user': 'parent'}
                # Store data in session
                session['code'] = data
                return render_template('code.html')
        return render_template('par_forget.html')
    elif user == 'teacher':
        if request.method == 'POST':
            data = request.form
            email = data['email']
            record = get_record_by_email(TeacherUser, email)
            if record is None:
                flash('Your email is not registered.')
            else:
                send_email(email, six_digit_number)
                data = {'email': email, 'code_num': str(six_digit_number), 'user': 'teacher'}
                # Store data in session
                session['code'] = data
                return render_template('code.html')
        return render_template('tec_forget.html')
    elif user == 'admin':
        if request.method == 'POST':
            data = request.form
            email = data['email']
            if admin_email == email:
                send_email(email, six_digit_number)
                data = {'email': email, 'code_num': str(six_digit_number), 'user': 'admin'}
                # Store data in session
                session['code'] = data
                return render_template('code.html')
            else:
                flash('You are not the admin.')
        return render_template('ad_forget.html')


@app.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        data = session.get('code')
        actual_code = data['code_num']
        given_code = request.form['code']
        if given_code == actual_code:
            return render_template('change_password.html')
        else:
            flash('You gave wrong code')
            return redirect(url_for('forgot', user=data['user']))


@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        data = session.get('code')
        user = data['user']
        password = request.form['password']
        hashed_password = ph.hash(password)
        if user == 'student':
            dept = get_department(data['department'])
            reg = data['register_number']
            update_password_by_register(dept, reg, hashed_password)
        elif user == 'parent':
            email = data['email']
            update_password_by_email(ParentUser, email, hashed_password)
        elif user == 'teacher':
            email = data['email']
            update_password_by_email(TeacherUser, email, hashed_password)
        elif user == 'admin':
            change_password_in_json(hashed_password)
        return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        data = request.form
        name = data['name']
        register_number = data['register_number']
        dob = data['dob']
        department = data['department']
        phone_number = en_decrypt.encrypt_data(data['phone_number'])
        parents_phone_number = data['parents_phone_number']
        email = data['email']
        address = en_decrypt.encrypt_data(data['address'])
        password = data['password']
        hashed_password = ph.hash(password)
        gender = data['gender']
        dept = get_department(department)
        with app.app_context():
            try:
                add_student_to_department(dept, name, register_number, hashed_password, dob, gender, email,
                                          phone_number, parents_phone_number, address)
                return render_template("login.html")
            except IntegrityError:
                print("error")
                flash('you already have an account')
                return render_template("login.html")


@app.route('/get student', methods=['GET', 'POST'])
@role_required(['parent'])
def get_student():
    session_data = session.get('data')
    phone_number = session_data['phone_number']
    if request.method == 'GET':
        return render_template('get_student.html')
    else:
        data = request.form
        dept = get_department(data['department'])
        student_detail = get_student_by_register_number(data['register_number'], dept)
        # field = 'parents_phone_number'
        # encrypted_value = getattr(student_detail, field,
        #                           None)  # Get the value or None if the attribute doesn't exist
        # if encrypted_value:
        #     try:
        #         decrypted_value = en_decrypt.decrypt_data(encrypted_value)
        #         setattr(student_detail, field, decrypted_value)  # get_studentSet the decrypted value to the attribute
        #     except Exception as e:
        #         # Handle decryption errors gracefully
        #         print(f"Error decrypting {field}: {e}")
        #     print(phone_number, student_detail.parents_phone_number)
        try:
            if phone_number == student_detail.parents_phone_number:
                data = {'register_number': data['register_number'], 'department': data['department'], 'user': 'parent'}
                # Store data in session
                session['data'] = data
                return redirect(url_for('home'))
            else:
                flash("The register number given doesn't belong to your child")
                return render_template('get_student.html')
        except AttributeError:
            flash("Student Info Wrong")
            return render_template('get_student.html')


@app.route('/parent register', methods=['GET', 'POST'])
def parent_register():
    if request.method == 'GET':
        return render_template("parent_register.html")
    else:
        data = request.form
        name = data['name']
        phone_number = en_decrypt.encrypt_data(data['phone_number'])
        email = data['email']
        password = data['password']
        hashed_password = ph.hash(password)
        with app.app_context():
            try:
                add_parent_to_parent_user(name, phone_number, hashed_password, email)
                return render_template("login.html")
            except IntegrityError:
                print("error")
                flash('you already have an account')
                return render_template("login.html")


@app.route('/teacher register', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'GET':
        return render_template("teacher_register.html")
    else:
        data = request.form
        name = data['name']
        teacher_id = data['teacher_id']
        email = data['email']
        password = data['password']
        department = data['department']
        hashed_password = ph.hash(password)
        with app.app_context():
            try:
                add_teacher_to_teacher_user(name, teacher_id, hashed_password, email, department)
                return render_template("login.html")
            except IntegrityError:
                print("error")
                flash('you already have an account')
                return render_template("login.html")


@app.route('/home')
@login_required
@role_required(['student', 'parent'])
def home():
    # Retrieve data from session
    try:
        data = session.get('data')
        dept = get_department(data['department'])
        student_detail = get_student_by_register_number(data['register_number'], dept)
        encrypted_fields = ['phone_number', 'address']
        for field in encrypted_fields:
            encrypted_value = getattr(student_detail, field,
                                      None)  # Get the value or None if the attribute doesn't exist
            if encrypted_value:
                try:
                    decrypted_value = en_decrypt.decrypt_data(encrypted_value)
                    setattr(student_detail, field, decrypted_value)  # Set the decrypted value to the attribute
                except Exception as e:
                    # Handle decryption errors gracefully
                    print(f"Error decrypting {field}: {e}")
        complaints = Complaint.query.filter_by(register_number=data['register_number']).all()
        if data['user'] == 'parent':
            return render_template("student.html", students_info=student_detail, complaints=complaints)
        return render_template("index.html", students_info=student_detail,  complaints=complaints)
    except TypeError:
        return redirect(url_for('login'))


@app.route('/notes')
@role_required(['student', 'teacher'])
def notes():
    # subject_names_for_cse = ['Operating System', 'Computer Networks', '', 'Data Structures',
    #                          'Database Management System']
    # update_or_add_subject(subject_names_for_cse, 'cse')
    data = session.get('data')
    if data['user'] == 'student':
        subjects = retrieve_column_values(data['department'])
        return render_template("notes.html", subjects=subjects)
    elif data['user'] == 'teacher':
        return render_template('tech_notes.html')


@app.route('/subject notes')
@role_required(['student'])
def sub_notes():
    subject = request.args.get('subject')
    subject_folder = os.path.join(SUBJECT_FILES_DIR, subject)
    print(subject_folder)
    # Ensure the subject folder exists
    if not os.path.exists(subject_folder):
        return 'Subject folder does not exist'

    # Return a list of files in the subject folder for the user to download
    files = os.listdir(subject_folder)
    return render_template('sub_notes.html', subject=subject, files=files)


@app.route('/sub_notes/download')
@role_required(['student'])
def download_file():
    try:
        subject = request.args.get('subject')
        filename = request.args.get('filename')

        # Construct the path to the file
        file_path = os.path.join(SUBJECT_FILES_DIR, subject, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            return 'File not found'

        # Serve the file
        return send_from_directory(os.path.join(SUBJECT_FILES_DIR, subject), filename)
    except TypeError:
        return render_template('access_rejected.html')


@app.route('/attendance', methods=['GET', 'POST'])
@role_required(['student', 'parent', 'teacher'])
def attendance():
    if request.method == 'POST':
        year = request.form.get('year')
        branch = request.form.get('branch')
        section = request.form.get('section')
        subject = request.form.get('subject')
        class_name = branch + section + year
        attendance_table = f'attendance{year}'
        attendance_col = branch + section
        table_name = 'A' + class_name + subject.replace(" ", "")
        create_subject_attendance_table(table_name, class_name, attendance_table, attendance_col)
        class_name_full = f'{year} year {full_form(branch)} {section}'
        session['table'] = {'class': class_name_full, 'sub_table': table_name, 'branch': branch, 'subject': subject}
        return redirect(url_for('enter_attendance'))
    data = session.get('data')
    if data['user'] == 'parent' or data['user'] == 'student':
        register_number = data['register_number']
        department = data['department']
        class_table_list = [f'{department}A1', f'{department}B1', f'{department}A2', f'{department}B2',
                            f'{department}A3', f'{department}B3', f'{department}A4', f'{department}B4']
        class_name = find_table_with_register_number(register_number, class_table_list)
        if class_name is not None:
            year = class_name[-1]
            attendance_table_name = f'attendance{year}'
            attendance_col = class_name[:-1]
            attendance_table_list = get_grade_col_data(attendance_table_name, attendance_col)
            dept_subjects = retrieve_column_values(department)
            dept_len = len(department) + 3
            subjects = split_subject(dept_len, dept_subjects, attendance_table_list)
            column_names = get_column_names(attendance_table_list)
            dates = get_dates_only(column_names)
            attendance_data = get_records_for_register_number(attendance_table_list, register_number)
            print(dates)
            print(attendance_data)
            zipped_lists = zip(dates, subjects, attendance_data)
        else:
            zipped_lists = []
        if data['user'] == 'parent':
            return render_template("stu_attend.html", zipped_lists=zipped_lists)
        return render_template("attendance.html", zipped_lists=zipped_lists)
    if data['user'] == 'teacher':
        return render_template("tec_attendance.html")


@app.route('/grades', methods=['GET', 'POST'])
@role_required(['student', 'parent', 'teacher'])
def grades():
    if request.method == 'POST':
        year = request.form.get('year')
        branch = request.form.get('branch')
        section = request.form.get('section')
        subject = request.form.get('subject')
        class_name = branch + section + year
        grade_table = f'grade{year}'
        grade_col = branch + section
        table_name = class_name + subject.replace(" ", "")
        create_subject_grade_table(table_name, class_name, grade_table, grade_col)
        class_name_full = f'{year} year {full_form(branch)} {section}'
        session['table'] = {'class': class_name_full, 'sub_table': table_name, 'branch': branch, 'subject': subject}
        return redirect(url_for('enter_grades'))
    data = session.get('data')
    if data['user'] == 'parent' or data['user'] == 'student':
        register_number = data['register_number']
        department = data['department']
        class_table_list = [f'{department}A1', f'{department}B1', f'{department}A2', f'{department}B2',
                            f'{department}A3', f'{department}B3', f'{department}A4', f'{department}B4']
        class_name = find_table_with_register_number(register_number, class_table_list)
        if class_name is not None:
            year = class_name[-1]
            grade_table_name = f'grade{year}'
            grade_col = class_name[:-1]
            grade_table_list = get_grade_col_data(grade_table_name, grade_col)
            dept_subjects = retrieve_column_values(department)
            dept_len = len(department) + 2
            subjects = split_subject(dept_len, dept_subjects, grade_table_list)
            grades_data = get_records_for_register_number(grade_table_list, register_number)
        else:
            grades_data = []
            subjects = []
        if data['user'] == 'parent':
            return render_template("stu_grade.html", grades_data=grades_data, subjects=subjects)
        return render_template("grades.html", grades_data=grades_data, subjects=subjects)
    if data['user'] == 'teacher':
        return render_template("tec_grades.html")


@app.route('/placement')
@role_required(['student'])
def placement():
    return render_template("placement.html")


@app.route('/teacher_index', methods=['GET', 'POST'])
@role_required(['teacher'])
def teacher_index():
    if request.method == 'POST':
        register_number = request.json.get('register_number')
        complaint_message = request.json.get('complaint_message')
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        response = add_complaint(register_number, complaint_message, current_time)
        if response:
            send_message(name=response.name, phone=response.parents_phone_number, content=complaint_message,
                         time=current_time)
        return jsonify({'status': 'done'})
    session_data = session.get('data')
    teacher_id = session_data['teacher_id']
    teacher_details = get_teacher_by_teacher_id(teacher_id)
    setattr(teacher_details, 'department', full_form(teacher_details.department))
    return render_template('tec_index.html', teacher_details=teacher_details)


@app.route('/get_subjects', methods=['POST'])
@role_required(['teacher'])
def get_subjects_route():
    branch = request.form.get('branch')
    if branch:
        subjects = retrieve_column_values(branch)
        return jsonify({'subjects': subjects})
    else:
        return jsonify({'error': 'Branch parameter is missing'})


@app.route('/upload', methods=['POST'])
@role_required(['teacher'])
def upload():
    if request.method == 'POST':
        subject = request.form['subject']
        branch = request.form['branch']
        if 'upload_PDF' not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        upload_pdf = request.files['upload_PDF']
        if upload_pdf.filename == '':
            flash("No selected file", "danger")
            return redirect(request.url)
        branch_folder = os.path.join(app.config['UPLOAD_FOLDER'], subject)
        if not os.path.exists(branch_folder):
            os.makedirs(branch_folder)
        filepath = os.path.join(branch_folder, upload_pdf.filename)  # Include branch folder in file path
        upload_pdf.save(filepath)
        flash('File uploaded successfully', 'success')
        add_file(upload_pdf.filename, branch, subject)
        return redirect(url_for('notes'))


@app.route('/admin')
@role_required(['admin'])
def admin_index():
    teachers, hods, teachers_by_department = retrieve_all_teacher_and_hod()
    hod_teachers = []
    non_hod_teachers = []
    for teacher in teachers:
        if teacher.teacher_id == hods.get(teacher.department):
            hod_teachers.append(teacher)
        else:
            non_hod_teachers.append(teacher)
    return render_template('ad_index.html', hod_teachers=hod_teachers,
                           non_hod_teachers=non_hod_teachers,
                           teachers_by_department=teachers_by_department)


@app.route('/change_hod', methods=['POST'])
@role_required(['admin'])
def change_hod():
    if request.method == 'POST':
        department = request.form.get('department')
        new_hod_teacher_id = request.form.get('new_hod')
        change_hod_in_table(department, new_hod_teacher_id)
        return redirect(url_for('admin_index'))


@app.route('/hod_index', methods=['POST', 'GET'])
@role_required(['hod'])
def hod_index():
    session_data = session.get('data')
    department = session_data['department']
    hod = session_data['teacher_id']
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        if hod != teacher_id:
            delete_teacher_by_id(teacher_id=teacher_id)
    teachers = get_department_teachers(department)
    classes = [f'{department}A1', f'{department}B1', f'{department}A2', f'{department}B2', f'{department}A3',
               f'{department}B3', f'{department}A4', f'{department}B4']
    class_records = get_class_records(classes)
    session['class'] = {'classes': classes}
    return render_template('hod_index.html', department_teachers=teachers,
                           department=full_form(department), class_records=class_records)


@app.route('/save', methods=['POST', 'GET'])
@role_required(['hod'])
def save_class_teacher_id():
    if request.method == 'POST':
        table = session.get('class')
        classes = table['classes']
        teacher_ids = request.form.getlist('class_teacher_id')
        update_teacher_ids(classes, teacher_ids)
        print(teacher_ids)
        return redirect(url_for('hod_index'))


@app.route('/add_students', methods=['POST', 'GET'])
@role_required(['hod'])
def add_student():
    session_data = session.get('data')
    department = full_form(session_data['department'])
    if request.method == 'POST':
        year = request.form['year']
        section = request.form['section']
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        table_name = f'{session_data["department"]}{section}{year}'
        convert_to_sqlite(file_path, table_name=table_name, app=app)
        return jsonify({'message': f'{year} year {department} {section} students added'})
    return render_template('students.html', department=department)


@app.route('/enter_grades', methods=['POST', 'GET'])
@role_required(['teacher'])
def enter_grades():
    table = session.get('table')
    table_name = table['sub_table']
    class_name = table['class']
    subject = table['subject']
    department = table['branch']
    if request.method == 'POST':
        stu_grades = {}
        for key, value in request.form.items():
            if key.startswith('grades'):
                _, reg_num, index = key.split('[')
                reg_num = reg_num.rstrip(']')
                index = int(index.rstrip(']'))
                if reg_num not in stu_grades:
                    stu_grades[reg_num] = [None, None, None, None]
                    # Assuming there are 3 internal assessments + 1 for the semester grade
                stu_grades[reg_num][index] = value
        # Now you have a dictionary 'grades' containing the grades for each student
        print(stu_grades)
        update_table_with_grades(grades=stu_grades, table_name=table_name)
        preprocess_grades(stu_grades, subject, department)
        return redirect(url_for('grades'))
    table_data = fetch_table_data(table_name)
    return render_template('enter_grades.html', table_data=table_data, class_name=class_name,
                           subject=subject)


@app.route('/enter_attendance', methods=['POST', 'GET'])
@role_required(['teacher'])
def enter_attendance():
    table = session.get('table')
    table_name = table['sub_table']
    class_name = table['class']
    subject = table['subject']
    department = table['branch']
    if request.method == 'POST':
        attendance_data = request.form.getlist('attendance')
        register_numbers = request.form.getlist('register_number')
        update_attendance_for_today(table_name, attendance_data)
        preprocess_attendance(register_numbers, subject, department)
        return redirect(url_for('attendance'))
    table_data = fetch_table_data(table_name)
    return render_template('enter_attendance.html', table_data=table_data, class_name=class_name,
                           subject=subject)


@app.route('/add_subject', methods=['POST', 'GET'])
@role_required(['hod'])
def add_subject():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            try:
                data = read_excel_column(file)
                print(data)
                session_data = session.get('data')
                department = session_data['department']
                delete_column_data('subjects', department)
                update_or_add_subject(data, department)
                return jsonify({'data': data})
            except Exception as e:
                return jsonify({'error': str(e)})
    return render_template('add_subject.html')


@app.route('/update_subject', methods=['POST', 'GET'])
@role_required(['hod'])
def update_subject():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            try:
                data = read_excel_column(file)
                print(data)
                session_data = session.get('data')
                department = session_data['department']
                update_or_add_subject(data, department)
                return jsonify({'data': data})
            except Exception as e:
                return jsonify({'error': str(e)})
    return render_template('add_subject.html')


@app.route('/class', methods=['POST', 'GET'])
@role_required(['teacher'])
def my_class():
    data = session.get('data')
    teacher_id = data['teacher_id']
    dept = get_department_by_teacher_id(teacher_id)
    if request.method == 'POST':
        register_number = request.form.get('register_number')
        department = dept[:-2]
        deptt = get_department(department)
        student_detail = get_student_by_register_number(register_number, deptt)
        encrypted_fields = ['phone_number', 'address']
        for field in encrypted_fields:
            encrypted_value = getattr(student_detail, field,
                                      None)  # Get the value or None if the attribute doesn't exist
            if encrypted_value:
                try:
                    decrypted_value = en_decrypt.decrypt_data(encrypted_value)
                    setattr(student_detail, field, decrypted_value)  # Set the decrypted value to the attribute
                except Exception as e:
                    # Handle decryption errors gracefully
                    print(f"Error decrypting {field}: {e}")
        return render_template('student_detail.html', students_info=student_detail)
    if dept is not None:
        students = fetch_table_data(dept)
    else:
        students = []
    return render_template('class.html', students=students)


@app.route('/edit', methods=['POST', 'GET'])
@role_required(['teacher'])
def edit_student():
    if request.method == 'POST':
        data = session.get('data')
        teacher_id = data['teacher_id']
        dept = get_department_by_teacher_id(teacher_id)
        department = dept[:-2]
        deptt = get_department(department)
        data = request.form
        register_number = data['register_number']
        new_data = {
            "name": data['name'],
            "date_of_birth": data['dob'],
            "gender": data['gender'],
            "email": data['email'],
            "phone_number": en_decrypt.encrypt_data(data['phone_number']),
            "parents_phone_number": data['parents_phone_number'],
            "address": en_decrypt.encrypt_data(data['address'])  # Added closing parenthesis
        }
        update_cse(register_number, new_data, deptt)
        return redirect(url_for('my_class'))


@app.route('/remove_stu', methods=['POST', 'GET'])
@role_required(['teacher'])
def remove_student():
    if request.method == 'POST':
        data = session.get('data')
        teacher_id = data['teacher_id']
        dept = get_department_by_teacher_id(teacher_id)
        # department = dept[:-2]
        # deptt = get_department(department)
        data = request.form
        register_number = data['register_number']
        delete_record(dept, register_number)
        return redirect(url_for('my_class'))


if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)
