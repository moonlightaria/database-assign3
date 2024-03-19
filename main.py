from datetime import datetime
import sys
import psycopg2


def initalize():
    # create table in database with sql statement
    cursor.execute(
        "CREATE TABLE students(student_id SERIAL, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL, enrollment_date date, PRIMARY KEY (student_id), UNIQUE (email));")
    # add the inital values to the table
    addStudent('John', 'Doe', 'john.doe@example.com', '2023-09-01')
    addStudent('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01')
    addStudent('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')


# Retrieves and displays all records from the students table.
def getAllStudents():
    cursor.execute("select * from students")
    # get all values from the result and print them to the command line
    print(cursor.fetchall())


# Inserts a new student record into the students table.
def addStudent(first_name: str, last_name: str, email: str, enrollment_date):
    cursor.execute("""
    INSERT INTO students (first_name, last_name, email, enrollment_date) 
    VALUES (%s, %s, %s, %s)
    """, [first_name, last_name, email, enrollment_date])


# Updates the email address for a student with the specified student_id.
def updateStudentEmail(student_id: int, new_email: str):
    cursor.execute("""
    UPDATE students
    SET email = %s
    WHERE student_id = %s;
    """, [new_email, student_id])


# Deletes the record of the student with the specified student_id.
def deleteStudent(student_id):
    cursor.execute("""
        DELETE FROM students
        WHERE student_id = %s
        """, [student_id])


if __name__ == "__main__":
    # create connection to database
    conn = psycopg2.connect(database="assign3_test",
                            host="localhost",
                            user="postgres",
                            password="postgres",
                            port="5432")
    # create database pointer
    cursor = conn.cursor()
    # get which mode to run
    execute = sys.argv[1]

    match execute:
        case "init":
            initalize()
        case "fetch":
            getAllStudents()
        case "insert":
            addStudent(sys.argv[2], sys.argv[3], sys.argv[4], datetime.strptime(sys.argv[5], "%d-%m-%Y"))
        case "update":
            updateStudentEmail(sys.argv[2], sys.argv[3])
        case "delete":
            deleteStudent(sys.argv[2])
        case _:
            print("invalid option")

    # save changes and close connection to database
    conn.commit()
    cursor.close()
    conn.close()
