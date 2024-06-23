from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect, MetaData, Table, Column, Integer, String, select, literal_column
import pandas as pd
import sqlite3
from sms import send_message
from datetime import datetime
db = SQLAlchemy()


class CSE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class ECE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class EEE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class Civil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class Mechanical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class IT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    register_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    parents_phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cse = db.Column(db.String)
    it = db.Column(db.String)
    mech = db.Column(db.String)
    eee = db.Column(db.String)
    ece = db.Column(db.String)
    civil = db.Column(db.String)


class ParentUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)


class TeacherUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    teacher_id = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    department = db.Column(db.String)


class MyFile(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    branch = db.Column(db.String)
    subject = db.Column(db.String)


class HOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String)
    teacher_id = db.Column(db.String)


class CLASS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String)
    teacher_id = db.Column(db.String)


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_number = db.Column(db.String, nullable=False)
    complaint_message = db.Column(db.Text)
    complaint_date = db.Column(db.String)


# class Record(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     register_number = db.Column(db.String)


def create_tables(table_name_first_part):
    metadata = MetaData()
    for grade in range(1, 5):
        table_name = f'{table_name_first_part}{grade}'
        if not inspect(db.engine).has_table(table_name):
            table = Table(
                table_name,
                metadata,
                Column('id', Integer, primary_key=True),
                Column('cseA', String(100)),
                Column('cseB', String(100)),
                Column('itA', String(100)),
                Column('itB', String(100)),
                Column('eceA', String(100)),
                Column('eceB', String(100)),
                Column('mechA', String(100)),
                Column('mechB', String(100)),
                Column('eeeA', String(100)),
                Column('eeeB', String(100)),
                Column('civilA', String(100)),
                Column('civilB', String(100))
            )
            table.create(bind=db.engine)


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
    db.init_app(app)
    with app.app_context():
        create_tables('grade')
        create_tables('attendance')
        db.create_all()
        if HOD.query.count() == 0:
            add_department_to_hod()
        if CLASS.query.count() == 0:
            add_class_to_class()


def add_student_to_department(department, name, register_number, password, date_of_birth, gender, email, phone_number,
                              parents_phone_number, address):
    student = department(name=name, register_number=register_number, password=password, date_of_birth=date_of_birth,
                         gender=gender, email=email, phone_number=phone_number,
                         parents_phone_number=parents_phone_number,
                         address=address)
    db.session.add(student)
    db.session.commit()


def add_parent_to_parent_user(name, phone_number, password, email):
    parent = ParentUser(name=name, phone_number=phone_number, password=password, email=email)
    db.session.add(parent)
    db.session.commit()


def add_teacher_to_teacher_user(name, teacher_id, password, email, department):
    teacher = TeacherUser(name=name, teacher_id=teacher_id,
                          password=password, email=email, department=department)
    db.session.add(teacher)
    db.session.commit()


def add_department_to_hod():
    department = ['cse', 'it', 'ece', 'eee', 'civil', 'mech']
    for dept in department:
        depart = HOD(department=dept)
        db.session.add(depart)
    db.session.commit()


def update_teacher_ids(department_names, new_teacher_ids):
    # Iterate through department names and new teacher IDs
    for department_name, new_teacher_id in zip(department_names, new_teacher_ids):
        # Retrieve the record to update
        hod_record = CLASS.query.filter_by(department=department_name).first()

        if hod_record:
            # Update the teacher_id field
            hod_record.teacher_id = new_teacher_id
            # Commit the changes to the database
            db.session.commit()


def add_class_to_class():
    department = ['cseA1', 'cseB1', 'cseA2', 'cseB2', 'cseA3', 'cseB3', 'cseA4', 'cseB4',
                  'itA1', 'itB1', 'itA2', 'itB2', 'itA3', 'itB3', 'itA4', 'itB4',
                  'eceA1', 'eceB1', 'eceA2', 'eceB2', 'eceA3', 'eceB3', 'eceA4', 'eceB4',
                  'eeeA1', 'eeeB1', 'eeeA2', 'eeeB2', 'eeeA3', 'eeeB3', 'eeeA4', 'eeeB4',
                  'civilA1', 'civilB1', 'civilA2', 'civilB2', 'civilA3', 'civilB3', 'civilA4', 'civilB4',
                  'mechA1', 'mechB1', 'mechA2', 'mechB2', 'mechA3', 'mechB3', 'mechA4', 'mechB4']
    for dept in department:
        depart = CLASS(department=dept)
        db.session.add(depart)
    db.session.commit()


def add_file(file_name, branch, subject):
    new_file = MyFile(file_name=file_name, branch=branch, subject=subject)
    db.session.add(new_file)
    db.session.commit()


def get_student_by_register_number(register_number, department):
    student = department.query.filter_by(register_number=register_number).first()
    return student


def get_parent_by_email(email):
    parent = ParentUser.query.filter_by(email=email).first()
    return parent


def get_teacher_by_email(email):
    teacher = TeacherUser.query.filter_by(email=email).first()
    return teacher


def get_teacher_by_teacher_id(teacher_id):
    teacher = TeacherUser.query.filter_by(teacher_id=teacher_id).first()
    return teacher


def get_class_records(department_names):
    # Retrieve records based on department names
    hod_records = CLASS.query.filter(CLASS.department.in_(department_names)).all()
    print(hod_records[0].department)
    return hod_records


def get_hod_by_teacher_id(teacher_id):
    teacher = HOD.query.filter_by(teacher_id=teacher_id).first()
    return teacher


def get_department(department):
    if department == 'cse':
        return CSE
    elif department == 'eee':
        return EEE
    elif department == 'ece':
        return ECE
    elif department == 'civil':
        return Civil
    elif department == 'it':
        return IT
    else:
        return Mechanical


def find_empty_column_id_in_department(department):
    empty_column_id = None

    # Query for the first row with an empty value in the specified department column
    first_empty_row = Subjects.query.filter(getattr(Subjects, department).is_(None)).first()

    if first_empty_row:
        empty_column_id = first_empty_row.id

    return empty_column_id


def update_or_add_subject(subjects, department):
    for subject in subjects:
        empty_column_id = find_empty_column_id_in_department(department)

        if empty_column_id is not None:
            # Update the column if an empty column is found
            setattr(Subjects.query.get(empty_column_id), department, subject)
            db.session.commit()
            print(f"Subject '{subject}' updated in column '{department}' for row with ID {empty_column_id}.")
        else:
            # Add new column value if all columns are filled
            new_subject = Subjects(**{department: subject})
            db.session.add(new_subject)
            db.session.commit()


def retrieve_column_values(column_name):

    # Query the database to retrieve all values from the specified column
    column_values = Subjects.query.with_entities(getattr(Subjects, column_name)).all()

    # Extract values from the result
    column_values = [value[0] for value in column_values if value[0] is not None]

    return column_values


def full_form(department):
    if department == 'cse':
        return 'Computer Science and Engineering'
    elif department == 'it':
        return 'Information Technology'
    elif department == 'eee':
        return 'Electrical and Electronics Engineering'
    elif department == 'civil':
        return 'Civil Engineering'
    elif department == 'mech':
        return 'Mechanical Engineering'
    else:
        return 'Electrical and Communication Engineering'


def retrieve_all_teacher_and_hod():
    all_teachers = TeacherUser.query.all()
    teachers_by_department = {}
    for teacher in all_teachers:
        if teacher.department not in teachers_by_department:
            teachers_by_department[teacher.department] = []
        teachers_by_department[teacher.department].append(teacher)
    hods = HOD.query.all()
    hod_by_department = {hod.department: hod.teacher_id for hod in hods}
    return all_teachers, hod_by_department, teachers_by_department


def change_hod_in_table(department, new_hod_teacher_id):
    existing_hod = HOD.query.filter_by(department=department).first()
    if existing_hod:
        existing_hod.teacher_id = new_hod_teacher_id
    else:
        new_hod = HOD(department=department, teacher_id=new_hod_teacher_id)
        db.session.add(new_hod)

    db.session.commit()


def get_department_teachers(department):
    teachers = TeacherUser.query.filter_by(department=department).all()
    return teachers


def delete_teacher_by_id(teacher_id):
    # Query the database for the teacher with the provided teacher ID
    teacher = TeacherUser.query.filter_by(teacher_id=teacher_id).first()

    if teacher:
        # If the teacher exists, delete the record from the database
        db.session.delete(teacher)
        db.session.commit()


def add_complaint(register_number, complaint_message, complaint_date):
    try:
        # Check if the register number exists in any of the department models
        department_models = [CSE, ECE, EEE, Civil, Mechanical, IT]
        existing_record = None
        for model in department_models:
            existing_record = model.query.filter_by(register_number=register_number).first()
            if existing_record:
                break

        if not existing_record:
            return None  # Register number does not exist in any department

        # Create a new complaint record
        new_complaint = Complaint(register_number=register_number, complaint_message=complaint_message,
                                  complaint_date=complaint_date)
        db.session.add(new_complaint)
        db.session.commit()
        return existing_record  # Complaint added successfully
    except Exception as e:
        print(f"Error adding complaint: {e}")
        db.session.rollback()
        return None


def convert_to_sqlite(input_file, table_name, app):
    # Read the input file into a pandas DataFrame
    with app.app_context():
        df = pd.read_excel(input_file) if input_file.endswith('.xlsx') else pd.read_csv(input_file, header=None)

        # Assuming the DataFrame has two columns: name and register_number
        df.columns = ['name', 'register_number']

        # Check if table exists
        inspector = inspect(db.engine)
        if inspector.has_table(table_name):
            # If the table exists, drop it
            db.session.execute(text(f"DROP TABLE {table_name}"))

        # Create table
        create_table_query = text(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, name VARCHAR, "
                                  f"register_number VARCHAR)")
        db.session.execute(create_table_query)

        # Insert data into the table
        insert_query = text(f"INSERT INTO {table_name} (name, register_number) VALUES (:name, :register_number)")
        for index, row in df.iterrows():
            db.session.execute(insert_query, {'name': row['name'], 'register_number': row['register_number']})

        # Commit changes
        db.session.commit()


def create_subject_grade_table(table_name, class_name, grade_table_name, grade_col):
    metadata = MetaData()
    # Check if the target table exists
    if not inspect(db.engine).has_table(table_name):
        # Define the target table

        table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('register_number', String),
            Column('internal1', String),
            Column('internal2', String),
            Column('internal3', String),
            Column('semester', String(5))  # Assuming grades are represented with a maximum of 2 characters
        )
        # Create the target table
        table.create(bind=db.engine)
        update_or_add_table_name(table_name, grade_table_name, grade_col)
        # Check if the source table exists
        if inspect(db.engine).has_table(class_name):
            # Connect to the SQLite database
            conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your database file

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            try:
                # Execute a query to fetch data from the source table
                cursor.execute(f"SELECT id, name, register_number FROM {class_name}")

                # Fetch all rows from the result
                rows = cursor.fetchall()

                # Insert fetched data into the destination table with additional columns
                for row in rows:
                    # Prepare the insert query with placeholders for the values
                    insert_query = (f"INSERT INTO {table_name} (id, name, register_number, internal1, internal2, "
                                    f"internal3, semester) VALUES (?, ?, ?, ?, ?, ?, ?)")
                    # Insert data into the destination table
                    cursor.execute(insert_query, (row[0], row[1], row[2], None, None, None, None))

                # Commit the changes to the database
                conn.commit()
                print("Data copied successfully!")

            except sqlite3.Error as e:
                print("Error copying data from the source table:", e)

            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

            print('successfully completed')
            return True  # Table created successfully and data transferred
    else:
        print('table already exists')
        return False  # Source table does not exist


def fetch_table_data(table_name):
    # Connect to your database
    conn = sqlite3.connect('instance/college.db')
    cursor = conn.cursor()

    # Fetch data from the specified table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the fetched data into list of lists format
    table_data = [list(row) for row in rows]

    return table_data


def update_table_with_grades(grades, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/college.db')
    cursor = conn.cursor()

    # Loop through the grades dictionary
    for reg_num, grade_list in grades.items():
        # Update the table with the grades for each register number
        cursor.execute(f'''
            UPDATE {table_name}
            SET internal1 = ?,
                internal2 = ?,
                internal3 = ?,
                semester = ?
            WHERE register_number = ?
        ''', (*grade_list, reg_num))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def preprocess_grades(grades, subject, department):
    for reg_num, grade_list in grades.items():
        grade = grade_list[-1]
        if grade == 'RA' or grade == 'SA' or grade == 'W':
            message = f'Subject: {subject}\nGrade: {grade}\nStatus: Fail'
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
            dept = get_department(department)
            response = get_student_by_register_number(register_number=reg_num, department=dept)
            if response is not None:
                send_message(name=response.name, phone=response.parents_phone_number, content=message,
                             time=current_time)


def preprocess_attendance(register_numbers, subject, department):
    for register_number in register_numbers:
        message = f'Subject: {subject}\nAttendance: A\nStatus: Absent'
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        dept = get_department(department)
        response = get_student_by_register_number(register_number=register_number, department=dept)
        if response is not None:
            send_message(name=response.name, phone=response.parents_phone_number, content=message,
                         time=current_time)


def update_or_add_table_name(table_name, grade_table_name, grade_col):
    conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your database file
    cursor = conn.cursor()

    # Check if the grade table exists, if not, create it
    # cursor.execute(f"CREATE TABLE IF NOT EXISTS {grade_table_name} (id INTEGER PRIMARY KEY, {grade_col} TEXT)")

    # Check if there is an empty column in the specified grade_col of the grade_table
    empty_column_id = find_empty_column_id_in_grade_table(cursor, grade_table_name, grade_col)

    if empty_column_id is not None:
        # Update the column if an empty column is found
        update_grade_table_column(cursor, grade_table_name, grade_col, table_name, empty_column_id)
    else:
        # Add new row with the table_name if all columns are filled
        add_row_to_grade_table(cursor, grade_table_name, grade_col, table_name)

    conn.commit()
    conn.close()


def find_empty_column_id_in_grade_table(cursor, grade_table_name, grade_col):
    # Query for the first row with an empty value in the specified grade_col
    cursor.execute(f"SELECT id FROM {grade_table_name} WHERE {grade_col} IS NULL LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def update_grade_table_column(cursor, grade_table_name, grade_col, table_name, column_id):
    # Update the specified grade_col with the table_name
    cursor.execute(f"UPDATE {grade_table_name} SET {grade_col} = ? WHERE id = ?", (table_name, column_id))
    print(f"Table name '{table_name}' updated in column '{grade_col}' for row with ID {column_id}.")


def add_row_to_grade_table(cursor, grade_table_name, grade_col, table_name):
    # Add new row with the table_name
    cursor.execute(f"INSERT INTO {grade_table_name} ({grade_col}) VALUES (?)", (table_name,))
    print(f"New row added with table name '{table_name}' in column '{grade_col}'.")


def get_grade_col_data(grade_table_name, grade_col):
    conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your database file
    cursor = conn.cursor()

    # Query to retrieve all data from the specified grade_col
    cursor.execute(f"SELECT {grade_col} FROM {grade_table_name}")
    data = cursor.fetchall()

    conn.close()

    # Extract the grade_col data from the result and return as a list
    grade_col_data = [row[0] for row in data]
    return grade_col_data


def find_table_with_register_number(register_number, tables_list):
    conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your SQLite database file
    cursor = conn.cursor()

    for table_name in tables_list:
        try:
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name.strip()} WHERE register_number = ?)",
                           (register_number,))
        except sqlite3.OperationalError:
            continue  # Table doesn't exist, move to the next table
        exists_in_table = cursor.fetchone()[0]
        if exists_in_table:
            conn.close()
            return table_name.strip()

    conn.close()
    return None


def get_records_for_register_number(table_names, register_number):
    records = []

    # Connect to the SQLite database
    conn = sqlite3.connect('instance/college.db')
    c = conn.cursor()

    try:
        # Iterate over each table name
        for table_name in table_names:
            # Query the table for records with the provided register number
            c.execute(f"SELECT * FROM {table_name} WHERE register_number=?", (register_number,))
            table_records = c.fetchall()

            # Append the records to the list
            records.extend(table_records)

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        # Close the connection
        conn.close()

    return records


def split_subject(length, subjects, table_name):
    splitted_name = [name[length:] for name in table_name]
    new_list = []

    for value in splitted_name:
        for subject in subjects:
            # Remove spaces from the subject
            subject_without_spaces = subject.replace(" ", "")

            # Check if the modified subject matches the current math_subject
            if value == subject_without_spaces:
                new_list.append(subject)
                break  # Break out of the inner loop once a match is found
    return new_list


def create_subject_attendance_table(table_name, class_name, grade_table_name, grade_col):
    metadata = MetaData()
    # Check if the target table exists
    if not inspect(db.engine).has_table(table_name):
        # Define the target table

        table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('register_number', String),
        )
        # Create the target table
        table.create(bind=db.engine)
        update_or_add_table_name(table_name, grade_table_name, grade_col)
        # Check if the source table exists
        if inspect(db.engine).has_table(class_name):
            # Connect to the SQLite database
            conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your database file

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            try:
                # Execute a query to fetch data from the source table
                cursor.execute(f"SELECT id, name, register_number FROM {class_name}")

                # Fetch all rows from the result
                rows = cursor.fetchall()

                # Insert fetched data into the destination table with additional columns
                for row in rows:
                    # Prepare the insert query with placeholders for the values
                    insert_query = f"INSERT INTO {table_name} (id, name, register_number) VALUES (?, ?, ?)"
                    # Insert data into the destination table
                    cursor.execute(insert_query, (row[0], row[1], row[2]))

                # Commit the changes to the database
                conn.commit()
                print("Data copied successfully!")

            except sqlite3.Error as e:
                print("Error copying data from the source table:", e)

            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

            print('successfully completed')
            return True  # Table created successfully and data transferred
    else:
        print('table already exists')
        return False  # Source table does not exist


def update_attendance_for_today(table_name, attendance_data):
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect('instance/college.db')
    cursor = conn.cursor()

    # Add a new column for today's date with default value 'P' (Present)
    today_date_column = datetime.now().strftime("%d-%m-%Y_%H:%M")
    alter_query = f"ALTER TABLE {table_name} ADD COLUMN '{today_date_column}' VARCHAR DEFAULT 'P';"
    cursor.execute(alter_query)

    # Update attendance for all students with provided attendance data for today's date
    for index, status in enumerate(attendance_data):
        student_id = index + 1  # Assuming student IDs start from 1 and increment by 1
        update_query = f"UPDATE {table_name} SET '{today_date_column}' = ? WHERE id = ?;"
        cursor.execute(update_query, (status, student_id))

    # Commit changes and close connection
    conn.commit()
    conn.close()


def get_column_names(table_names):
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/college.db')  # Replace 'your_database_name.db' with your database name

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    table_column_list = []

    for table_name in table_names:
        # Execute the PRAGMA statement to get column information
        cursor.execute(f"PRAGMA table_info({table_name})")

        # Fetch all rows from the cursor
        rows = cursor.fetchall()

        # Extract column names from the rows
        column_names = [row[1] for row in rows]

        # Append column names to the list
        table_column_list.append(column_names)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return table_column_list


def get_dates_only(column_list):
    dates = []
    for column in column_list:
        dates_for_this = []
        for valid_column in column[3:]:
            date_only = valid_column.split('_')[0].strip("'")
            dates_for_this.append(date_only)
        dates.append(dates_for_this)
    return dates


def get_record_by_email(table, email):
    try:
        user = table.query.filter_by(email=email).first()
        return user
    except Exception as e:
        print("Error occurred:", str(e))
        return None


def update_password_by_email(table, email, new_password):
    try:
        user = table.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            return True
        else:
            print("User not found.")
            return False
    except Exception as e:
        print("Error occurred:", str(e))
        return False


def update_password_by_register(table, register_number, new_password):
    try:
        user = table.query.filter_by(register_number=register_number).first()
        if user:
            user.password = new_password
            db.session.commit()
            return True
        else:
            print("User not found.")
            return False
    except Exception as e:
        print("Error occurred:", str(e))
        return False


def read_excel_column(excel_file):
    try:
        df = pd.read_excel(excel_file, header=None)
        column_data = df.iloc[:, 0].tolist()
    except Exception as e:
        print("Error:", e)
        column_data = []
    return column_data


def delete_column_data(table_name, column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/college.db')
    c = conn.cursor()

    # Construct SQL query to delete data in the specified column
    query = f"UPDATE {table_name} SET {column_name} = NULL"

    # Execute the query
    c.execute(query)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()


def get_department_by_teacher_id(teacher_id):
    # Query the database to find the record with the matching teacher_id
    class_record = CLASS.query.filter_by(teacher_id=teacher_id).first()

    # If a record is found, return its department
    if class_record:
        return class_record.department
    else:
        return None


def update_cse(register_number, new_data, department):
    cse_record = department.query.filter_by(register_number=register_number).first()
    if cse_record:
        # Update fields with new data
        for key, value in new_data.items():
            setattr(cse_record, key, value)
        db.session.commit()
        return True
    else:
        return False


def delete_record(table_name, register_number):
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/college.db')  # Replace 'your_database.db' with your database file

    # Create a cursor object
    cursor = conn.cursor()

    # SQL query to delete a record with the specified register number from the table
    sql_query = f"DELETE FROM {table_name} WHERE register_number = ?"

    try:
        # Execute the query
        cursor.execute(sql_query, (register_number,))

        # Commit the changes
        conn.commit()

        print("Record deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting record: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
