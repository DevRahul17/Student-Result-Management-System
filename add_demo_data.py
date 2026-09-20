import sqlite3

DATABASE = "student_result_management.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# =========================================================
# 1. ADD COURSES
# =========================================================

courses = [
    (101, "B.Tech Computer Science", "4 Years", "85000", "Computer Science and Engineering"),
    (102, "B.Tech Information Technology", "4 Years", "82000", "Information Technology"),
    (103, "BCA", "3 Years", "55000", "Bachelor of Computer Applications"),
    (104, "MCA", "2 Years", "70000", "Master of Computer Applications"),
    (105, "BBA", "3 Years", "50000", "Bachelor of Business Administration")
]

for course in courses:
    cursor.execute("""
        INSERT OR IGNORE INTO course
        (cid, name, duration, charges, description)
        VALUES (?, ?, ?, ?, ?)
    """, course)


# =========================================================
# 2. ADD STUDENTS
# =========================================================

students = [
    (1001, "Rahul Kumar", "rahul@gmail.com", "Male", "2004-05-12",
     "9876543201", "2024-07-10", "B.Tech Computer Science",
     "Uttar Pradesh", "Ghaziabad", "201001", "Ghaziabad"),

    (1002, "Aman Sharma", "aman@gmail.com", "Male", "2004-08-21",
     "9876543202", "2024-07-10", "BCA",
     "Delhi", "New Delhi", "110001", "New Delhi"),

    (1003, "Priya Singh", "priya@gmail.com", "Female", "2005-01-15",
     "9876543203", "2024-07-11", "B.Tech Information Technology",
     "Uttar Pradesh", "Noida", "201301", "Noida"),

    (1004, "Arjun Verma", "arjun@gmail.com", "Male", "2004-11-05",
     "9876543204", "2024-07-11", "BCA",
     "Haryana", "Gurugram", "122001", "Gurugram"),

    (1005, "Neha Gupta", "neha@gmail.com", "Female", "2005-03-19",
     "9876543205", "2024-07-12", "B.Tech Computer Science",
     "Uttar Pradesh", "Lucknow", "226001", "Lucknow"),

    (1006, "Rohit Mehta", "rohit@gmail.com", "Male", "2004-06-25",
     "9876543206", "2024-07-12", "MCA",
     "Rajasthan", "Jaipur", "302001", "Jaipur"),

    (1007, "Anjali Yadav", "anjali@gmail.com", "Female", "2005-02-08",
     "9876543207", "2024-07-13", "BBA",
     "Uttar Pradesh", "Agra", "282001", "Agra"),

    (1008, "Vikas Singh", "vikas@gmail.com", "Male", "2004-09-14",
     "9876543208", "2024-07-13", "B.Tech Information Technology",
     "Uttar Pradesh", "Meerut", "250001", "Meerut"),

    (1009, "Simran Kaur", "simran@gmail.com", "Female", "2005-04-22",
     "9876543209", "2024-07-14", "BCA",
     "Punjab", "Amritsar", "143001", "Amritsar"),

    (1010, "Karan Malhotra", "karan@gmail.com", "Male", "2004-12-10",
     "9876543210", "2024-07-14", "B.Tech Computer Science",
     "Delhi", "New Delhi", "110002", "New Delhi"),

    (1011, "Pooja Sharma", "pooja@gmail.com", "Female", "2005-05-16",
     "9876543211", "2024-07-15", "BBA",
     "Uttar Pradesh", "Kanpur", "208001", "Kanpur"),

    (1012, "Aditya Jain", "aditya@gmail.com", "Male", "2004-07-28",
     "9876543212", "2024-07-15", "MCA",
     "Madhya Pradesh", "Bhopal", "462001", "Bhopal"),

    (1013, "Sneha Kapoor", "sneha@gmail.com", "Female", "2005-06-11",
     "9876543213", "2024-07-16", "B.Tech Computer Science",
     "Uttar Pradesh", "Ghaziabad", "201002", "Ghaziabad"),

    (1014, "Manish Kumar", "manish@gmail.com", "Male", "2004-10-18",
     "9876543214", "2024-07-16", "BCA",
     "Bihar", "Patna", "800001", "Patna"),

    (1015, "Kavya Agarwal", "kavya@gmail.com", "Female", "2005-08-02",
     "9876543215", "2024-07-17", "B.Tech Information Technology",
     "Uttar Pradesh", "Varanasi", "221001", "Varanasi"),

    (1016, "Sahil Khan", "sahil@gmail.com", "Male", "2004-04-30",
     "9876543216", "2024-07-17", "BBA",
     "Uttar Pradesh", "Aligarh", "202001", "Aligarh"),

    (1017, "Isha Verma", "isha@gmail.com", "Female", "2005-09-09",
     "9876543217", "2024-07-18", "BCA",
     "Rajasthan", "Kota", "324001", "Kota"),

    (1018, "Nitin Sharma", "nitin@gmail.com", "Male", "2004-02-17",
     "9876543218", "2024-07-18", "MCA",
     "Haryana", "Faridabad", "121001", "Faridabad"),

    (1019, "Riya Mishra", "riya@gmail.com", "Female", "2005-07-07",
     "9876543219", "2024-07-19", "B.Tech Computer Science",
     "Uttar Pradesh", "Prayagraj", "211001", "Prayagraj"),

    (1020, "Deepak Joshi", "deepak@gmail.com", "Male", "2004-03-26",
     "9876543220", "2024-07-19", "B.Tech Information Technology",
     "Uttarakhand", "Dehradun", "248001", "Dehradun")
]

for student in students:
    cursor.execute("""
        INSERT OR IGNORE INTO student
        (roll, name, email, gender, dob, contact, admission,
         Course, state, city, pin, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, student)


# =========================================================
# 3. ADD RESULTS
# =========================================================

# =========================================================
# 3. ADD RESULTS
# =========================================================

# Your database has a UNIQUE constraint on result.cid,
# so we can store one result for each course.

results = [
    (101, "1001", "Rahul Kumar", "B.Tech Computer Science", "435", "500", "87%"),
    (102, "1003", "Priya Singh", "B.Tech Information Technology", "455", "500", "91%"),
    (103, "1002", "Aman Sharma", "BCA", "410", "500", "82%"),
    (104, "1006", "Rohit Mehta", "MCA", "420", "500", "84%"),
    (105, "1007", "Anjali Yadav", "BBA", "395", "500", "79%")
]

for result in results:
    cursor.execute("""
        INSERT OR IGNORE INTO result
        (cid, roll, name, course, marks_ob, full_marks, per)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, result)
 


# =========================================================
# 4. ADD EXAM RECORDS
# =========================================================

exam_records = [
    (1001, "Rahul Kumar", "B.Tech Computer Science", "Semester 1", "Final Examination", 85, 88, 90, 84, 86, 92, "87%"),
    (1002, "Aman Sharma", "BCA", "Semester 1", "Final Examination", 80, 82, 84, 79, 81, 86, "82%"),
    (1003, "Priya Singh", "B.Tech Information Technology", "Semester 1", "Final Examination", 92, 90, 94, 91, 89, 90, "91%"),
    (1004, "Arjun Verma", "BCA", "Semester 1", "Final Examination", 75, 78, 80, 74, 76, 73, "76%"),
    (1005, "Neha Gupta", "B.Tech Computer Science", "Semester 1", "Final Examination", 88, 90, 91, 87, 89, 89, "89%"),
    (1006, "Rohit Mehta", "MCA", "Semester 1", "Final Examination", 82, 84, 86, 83, 85, 80, "84%"),
    (1007, "Anjali Yadav", "BBA", "Semester 1", "Final Examination", 78, 80, 77, 79, 81, 79, "79%"),
    (1008, "Vikas Singh", "B.Tech Information Technology", "Semester 1", "Final Examination", 85, 87, 86, 84, 88, 86, "86%"),
    (1009, "Simran Kaur", "BCA", "Semester 1", "Final Examination", 90, 91, 89, 92, 88, 90, "90%"),
    (1010, "Karan Malhotra", "B.Tech Computer Science", "Semester 1", "Final Examination", 94, 92, 95, 91, 93, 94, "93%"),
    (1011, "Pooja Sharma", "BBA", "Semester 1", "Final Examination", 80, 82, 81, 79, 83, 81, "81%"),
    (1012, "Aditya Jain", "MCA", "Semester 1", "Final Examination", 87, 89, 88, 86, 90, 88, "88%"),
    (1013, "Sneha Kapoor", "B.Tech Computer Science", "Semester 1", "Final Examination", 84, 86, 85, 83, 87, 85, "85%"),
    (1014, "Manish Kumar", "BCA", "Semester 1", "Final Examination", 76, 79, 78, 80, 77, 78, "78%"),
    (1015, "Kavya Agarwal", "B.Tech Information Technology", "Semester 1", "Final Examination", 91, 93, 92, 90, 94, 92, "92%"),
    (1016, "Sahil Khan", "BBA", "Semester 1", "Final Examination", 73, 75, 77, 74, 76, 75, "75%"),
    (1017, "Isha Verma", "BCA", "Semester 1", "Final Examination", 86, 88, 87, 85, 89, 87, "87%"),
    (1018, "Nitin Sharma", "MCA", "Semester 1", "Final Examination", 81, 84, 83, 82, 85, 83, "83%"),
    (1019, "Riya Mishra", "B.Tech Computer Science", "Semester 1", "Final Examination", 95, 94, 96, 93, 92, 94, "94%"),
    (1020, "Deepak Joshi", "B.Tech Information Technology", "Semester 1", "Final Examination", 79, 81, 80, 78, 82, 80, "80%")
]

for exam in exam_records:
    cursor.execute("""
        INSERT OR IGNORE INTO examrecord
        (roll, name, course, semester, examination,
         sub1, sub2, sub3, sub4, sub5, sub6, per)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, exam)


# =========================================================
# SAVE EVERYTHING
# =========================================================

conn.commit()
conn.close()

print()
print("==============================================")
print("      DEMO DATA ADDED SUCCESSFULLY!")
print("==============================================")
print("20 Students added")
print("5 Courses added")
print("5 Results added")
print("20 Exam records added")
print("==============================================")