import mysql.connector as mysql

db = mysql.connect(
    host="localhost", user="your database username", password="your password for mysql", database="your database name"
)
command_hander = db.cursor(buffered=True)


def teacher_session():
    while 1:
        print("")
        print("Teacher's Menu")
        print("1. Mark Student register")
        print("2. View register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Mark student register")
            command_hander.execute(
                "SELECT username FROM users WHERE privilege = 'student'"
            )
            records = command_hander.fetchall()
            date = input(str("Date : DD/MM/YYYY : "))
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                # Present | Absent | Late
                status = input(str("Status for " + str(record) + " P/A/L : "))
                query_vals = (str(record), date, status)
                command_hander.execute(
                    "INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)",
                    query_vals
                )
                db.commit()
                print(record + " Marked as " + status)

        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_hander.execute("SELECT username, date, status FROM attendance")
            records = command_hander.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)


        elif user_option == "3":
            break
        else:
            print("Not a valid option")


def student_session(username):
    while 1:
        print("")
        print("Student's Menu")
        print("")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("Displaying Register")
            username = (str(username),)
            command_hander.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_hander.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)

        elif user_option == "2":
            username = (str(username),)
            command_hander.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_hander.fetchall()
            print("Downloading registers")
            for record in records:
                with open("register.txt", "w") as file:
                    file.write(str(records)+"\n")
                file.close()
            print("All records saved")

        elif user_option == "3":
            break
        else:
            print("Not a valid option")

def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Register new Student")
            username = input(str("Student username : "))
            password = input(str("Student password : "))
            query_vals = (username, password)
            command_hander.execute(
                "INSERT INTO users (username, password, privilege) VALUES(%s,%s, 'student')",
                query_vals,
            )
            db.commit()
            print(username + " has being registered as a student")

        elif user_option == "2":
            print("")
            print("Register new Teacher")
            username = input(str("Teacher username : "))
            password = input(str("Teacher password : "))
            query_vals = (username, password)
            command_hander.execute(
                "INSERT INTO users (username, password, privilege) VALUES(%s,%s, 'teacher')",
                query_vals,
            )
            db.commit()
            print(username + " has being registered as a teacher")
        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = input(str("Student username : "))
            query_vals = (username, "student")
            command_hander.execute(
                "DELETE FROM users WHERE username = %s AND privilege = %s", query_vals
            )
            db.commit()
            if command_hander.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account")
            username = input(str("Teacher username : "))
            query_vals = (username, "teacher")
            command_hander.execute(
                "DELETE FROM users WHERE username = %s AND privilege = %s", query_vals
            )
            db.commit()
            if command_hander.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        elif user_option == "5":
            break
        else:
            print("Not a valid option")

def auth_student():
    print("")
    print("Student's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password, 'student')
    command_hander.execute(
        "SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s",
        query_vals,
    )
    if command_hander.rowcount <= 0:
        print("Invalid login details")
    else:
        student_session(username)



def auth_teacher():
    print("")
    print("Teacher's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_hander.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'",
        query_vals,
    )
    if command_hander.rowcount <= 0:
        print("Login not recognized")
    else:
        teacher_session()


def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect password !")
    else:
        print("Login details not recognized")


def main():
    while 1:
        print("Welcome to the Creed college")
        print("")
        print("1. Login as Student")
        print("2. Login as Teacher")
        print("3. Login as Admin")
        print("4. Close Browser")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        elif user_option == "4":
            break
        else:
            print("option not valid")


main()
