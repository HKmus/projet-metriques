Here’s a **Software Requirements Specification (SRS)** for the **www.kiestla.edu** attendance management system, structured using a **use-case-based approach**. This document outlines the functional and non-functional requirements, actors, and use cases.

---

# **Software Requirements Specification (SRS)**
**Project:** KIESTLA Attendance Management System
**Version:** 1.0
**Date:** February 24, 2026

---

## **1. Introduction**
### **1.1 Purpose**
The KIESTLA Attendance Management System is designed to streamline the process of tracking, reporting, and justifying student absences. It provides a centralized portal for students, teachers, and administrative staff to manage attendance records efficiently.

### **1.2 Scope**
The system will:
- Allow administrators to manage teaching modules, teachers, and students.
- Enable teachers to report and comment on student absences.
- Provide administrative staff with tools to justify absences and monitor attendance trends.
- Alert teaching staff about students with excessive unjustified absences.

---

## **2. Overall Description**
### **2.1 System Features**
- **User Management:** Creation, maintenance, and deletion of users (administrators, teachers, students).
- **Module Management:** Creation, maintenance, and deletion of teaching modules.
- **Absence Reporting:** Teachers can report absences and add comments.
- **Absence Justification:** Administrative staff can enter reasons for absences.
- **Absence Monitoring:** Grouping absences by module and student.
- **Alert System:** Notifications for students with more than three unjustified absences.

### **2.2 Actors**
| Actor                | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| **Administrator**    | Manages users, modules, and system settings.                                |
| **Teacher**          | Reports absences, adds comments, and views absence lists for their modules.|
| **Student**          | View their own absence records.                                             |
| **Administrative Staff** | Justifies absences and monitors all student absences.                   |

---

## **3. Functional Requirements**
### **3.1 Use Cases**

#### **UC1: Manage Users**
- **Actor:** Administrator
- **Description:** The administrator can create, update, and delete user accounts (teachers, students, administrative staff).
- **Precondition:** Administrator is logged in.
- **Postcondition:** User database is updated.

#### **UC2: Manage Teaching Modules**
- **Actor:** Administrator
- **Description:** The administrator can create, update, and delete teaching modules and associate them with teachers.
- **Precondition:** Administrator is logged in.
- **Postcondition:** Module database is updated.

#### **UC3: Report Absence**
- **Actor:** Teacher
- **Description:** The teacher can report a student’s absence in a module and add a comment.
- **Precondition:** Teacher is logged in and assigned to the module.
- **Postcondition:** Absence record is created.

#### **UC4: View Absence List**
- **Actor:** Teacher
- **Description:** The teacher can view the list of absences for all students in their modules.
- **Precondition:** Teacher is logged in.
- **Postcondition:** Absence list is displayed.

#### **UC5: Justify Absence**
- **Actor:** Administrative Staff
- **Description:** Administrative staff can enter the reason for a student’s absence.
- **Precondition:** Staff is logged in.
- **Postcondition:** Absence record is updated with justification.

#### **UC6: Monitor Absences**
- **Actor:** Administrative Staff
- **Description:** Staff can group and view absences by module or student.
- **Precondition:** Staff is logged in.
- **Postcondition:** Absence data is displayed.

#### **UC7: Alert for Excessive Absences**
- **Actor:** System
- **Description:** The system alerts teaching staff about students with more than three unjustified absences.
- **Precondition:** Absence records exist.
- **Postcondition:** Alert is sent to relevant teachers.

---

## **4. Non-Functional Requirements**
### **4.1 Performance**
- The system should handle up to 10,000 users concurrently.
- Absence reporting should be processed in under 2 seconds.

### **4.2 Security**
- Role-based access control (RBAC) for all users.
- Data encryption for sensitive information (e.g., student records).

### **4.3 Usability**
- Intuitive user interface for all roles.
- Mobile-friendly design for accessibility.

### **4.4 Reliability**
- 99.9% uptime guarantee.
- Automated backups for data recovery.

---

## **5. System Architecture**
### **5.1 High-Level Architecture**
- **Frontend:** Web portal (HTML, CSS, JavaScript).
- **Backend:** Server-side logic (e.g., Python/Django, Node.js).
- **Database:** Relational database (e.g., PostgreSQL, MySQL) for user and absence records.

### **5.2 Data Flow**
1. **User Login:** Authentication and role assignment.
2. **Absence Reporting:** Teacher submits absence → System records data.
3. **Justification:** Staff updates absence reason → System logs justification.
4. **Alerts:** System checks absence count → Sends alerts if threshold exceeded.

---

## **6. Glossary**
- **Module:** A teaching unit or course.
- **Justification:** Reason provided for an absence.
- **Alert:** Notification sent to teaching staff.

---

## **7. Open Questions**
- Should students be allowed to view justifications for their absences?
- What is the process for disputing an absence record?

---
Would you like to refine any section or add specific technical details (e.g., API endpoints, database schema)?
