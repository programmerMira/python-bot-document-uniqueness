BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Result" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"courseProject_ID"	INTEGER,
	"courseProject_compared_ID"	INTEGER,
	"result"	INTEGER,
	FOREIGN KEY("courseProject_ID") REFERENCES "CourseProject"("id") ON DELETE SET NULL,
	FOREIGN KEY("courseProject_compared_ID") REFERENCES "CourseProject"("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "CourseProject" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"student_ID"	INTEGER,
	"file"	TEXT,
	FOREIGN KEY("student_ID") REFERENCES "Student"
);
CREATE TABLE IF NOT EXISTS "Student" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Surname"	TEXT NOT NULL,
	"Name"	TEXT NOT NULL,
	"FatherName"	TEXT,
	"acadYear"	INTEGER,
	"faculty"	TEXT,
	"group"	TEXT
);
COMMIT;
