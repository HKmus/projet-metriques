# Software Requirements Specification (SRS)

## Attendance Management System – [www.kiestla.edu](http://www.kiestla.edu)

---

# 1. Introduction

## 1.1 Purpose

This document describes the functional and non-functional requirements of the **[www.kiestla.edu](http://www.kiestla.edu)** website.

The system is designed to manage and simplify student attendance tracking, absence reporting, and absence justification within an educational institution.

This SRS is intended for:

* Developers
* Project managers
* System administrators
* Academic staff

---

## 1.2 Scope

The system is a web-based portal that connects:

* Students
* Teachers
* Referring teachers
* Administrative staff
* System administrator

The platform manages the full attendance workflow:

1. Recording absences
2. Adding comments
3. Justifying absences
4. Monitoring unjustified absences
5. Alerting teaching staff

---

## 1.3 Definitions

* **Module**: A teaching course.
* **Referring Teacher**: Teacher responsible for a module.
* **Administrative Staff**: Personnel responsible for validating and justifying absences.
* **Unjustified Absence**: An absence without an accepted reason.

---

# 2. Overall Description

## 2.1 System Perspective

The Attendance Management System is a centralized web platform with a shared database containing:

* Students
* Teachers
* Modules
* Absence records

The system uses role-based access control.

---

## 2.2 User Classes and Characteristics

| User Type            | Description                                      |
| -------------------- | ------------------------------------------------ |
| Administrator        | Manages modules, teachers, and students database |
| Referring Teacher    | Manages module members and monitors absences     |
| Teacher              | Records absences and views absence lists         |
| Administrative Staff | Justifies absences and accesses all records      |
| Student              | Subject of absence records                       |

---

# 3. Use Case Model

---

# 3.1 Actors

* Administrator
* Referring Teacher
* Teacher
* Administrative Staff

---

# 3.2 Use Cases Overview

1. Manage Modules
2. Manage Users Database
3. Assign Teachers to Modules
4. Add Students/Teachers to Module
5. Record Student Absence
6. Add Comment to Absence
7. View Absence List by Module
8. View Absence List by Student
9. Justify Absence
10. View Alert for Excessive Unjustified Absences

---

# 4. Detailed Use Cases

---

## UC1: Manage Modules

**Actor:** Administrator

**Description:**
Administrator creates, updates, or deletes teaching modules.

**Preconditions:**

* Administrator is authenticated.

**Main Flow:**

1. Administrator selects “Manage Modules”.
2. Creates, edits, or deletes a module.
3. System updates database.

**Postconditions:**

* Module data is updated successfully.

---

## UC2: Manage Users Database

**Actor:** Administrator

**Description:**
Administrator manages global database of teachers and students.

**Main Flow:**

1. Add new teacher/student.
2. Edit teacher/student information.
3. Delete teacher/student.

**Postconditions:**

* Database is updated.

---

## UC3: Assign Teachers to Modules

**Actor:** Administrator

**Description:**
Administrator associates one or more teachers with a module.

**Main Flow:**

1. Select module.
2. Select teacher(s).
3. Confirm association.

**Postconditions:**

* Teacher(s) linked to module.

---

## UC4: Add Students/Teachers to Module

**Actor:** Referring Teacher

**Description:**
Referring teacher adds registered teachers or students to their module.

**Precondition:**

* Users must already exist in the global database.

**Main Flow:**

1. Referring teacher selects module.
2. Searches user in database.
3. Adds user to module.

---

## UC5: Record Student Absence

**Actor:** Teacher

**Description:**
Teacher records absence of a student in a module.

**Preconditions:**

* Teacher is assigned to module.
* Student is enrolled in module.

**Main Flow:**

1. Teacher selects module session.
2. Selects student.
3. Marks as absent.
4. Optionally adds comment.
5. Saves record.

**Postconditions:**

* Absence record created.

---

## UC6: View Absence List by Module

**Actor:** Teacher

**Description:**
Teacher views all absences of students in their module.

**Main Flow:**

1. Select module.
2. System displays absence list grouped by module.

---

## UC7: View Absence List by Student

**Actor:** Administrative Staff

**Description:**
Administrative staff views absence records grouped by student.

**Main Flow:**

1. Search student.
2. System displays full absence history.

---

## UC8: Justify Absence

**Actor:** Administrative Staff

**Description:**
Administrative staff enters justification for absence.

**Main Flow:**

1. Select absence record.
2. Enter reason.
3. Validate justification.

**Postconditions:**

* Absence marked as justified or unjustified.

---

## UC9: Alert for Excessive Unjustified Absences

**Actor:** Teaching Staff

**Description:**
System alerts teachers when a student exceeds three unjustified absences.

**Trigger Condition:**

* Student has more than 3 unjustified absences.

**Main Flow:**

1. Teacher logs in.
2. System displays alert page.
3. List of students exceeding threshold is shown.

---

# 5. Functional Requirements

FR1: The system shall allow the administrator to manage modules.
FR2: The system shall allow management of teachers and students database.
FR3: The system shall allow teachers to record absences.
FR4: The system shall allow adding comments to absences.
FR5: The system shall allow administrative staff to justify absences.
FR6: The system shall group absences by module and by student.
FR7: The system shall automatically detect students with more than three unjustified absences.
FR8: The system shall generate alerts for excessive absences.

---

# 6. Non-Functional Requirements

## 6.1 Security

* Role-based access control.
* Secure authentication system.
* Only authorized users can modify absence records.

## 6.2 Performance

* The system shall load pages within 3 seconds under normal load.

## 6.3 Reliability

* The system shall ensure data consistency in absence records.

## 6.4 Usability

* User-friendly interface.
* Clear navigation between modules and absence records.

## 6.5 Availability

* The system shall be accessible 24/7 except during maintenance.

---

# 7. Assumptions and Constraints

* All users must be pre-registered in the system.
* The system requires internet access.
* The threshold for alerts is fixed at three unjustified absences.

---

# 8. Future Enhancements

* Email notifications to students.
* Automated reports generation.
* Integration with academic grading system.



