This Software Requirements Specification (SRS) document outlines the functional and non-functional requirements for the **kiestla.edu** attendance management portal.

---

## 1. Introduction

The **kiestla.edu** platform is a centralized web-based solution designed to digitize and streamline the tracking of student attendance. It bridges the gap between students, faculty, and administration by automating the workflow from the initial reporting of an absence to its formal justification.

### 1.1 Scope

The system handles user management, module assignment, real-time absence recording, and administrative reporting. It is intended to replace manual paper-based logs with a transparent, digital audit trail.

---

## 2. System Actors

The system involves four primary actors:

* **Administrator:** Responsible for system-wide configuration, including the global database of users and module creation.
* **Referring Teacher:** A teacher with elevated permissions to manage the roster of specific modules.
* **Teacher:** Faculty members who record attendance and monitor student progress within their assigned modules.
* **Administrative Staff:** Personnel responsible for verifying and entering justifications for absences.

---

## 3. Functional Requirements: Use Case Approach

### 3.1 Use Case Model

The following table summarizes the primary use cases identified for the kiestla.edu portal.

| Use Case ID | Use Case Name | Primary Actor | Description |
| --- | --- | --- | --- |
| **UC-01** | Manage Global Database | Administrator | Create, update, and delete student and teacher records in the central system. |
| **UC-02** | Manage Teaching Modules | Administrator | Create modules and link them to designated Referring Teachers. |
| **UC-03** | Manage Module Enrollment | Referring Teacher | Add registered teachers and students to a specific teaching module. |
| **UC-04** | Record Absence | Teacher | Mark a student as absent during a session and add optional comments. |
| **UC-05** | Consult Absence Logs | Teacher | View attendance history for all students enrolled in their modules. |
| **UC-06** | Justify Absence | Admin Staff | Enter official reasons (e.g., medical certificates) for a recorded absence. |
| **UC-07** | Generate Absence Reports | Admin Staff | View and group absences by module or by specific student. |
| **UC-08** | Critical Absence Alert | Teacher | Automatically identify students with $>3$ unjustified absences. |

---

### 3.2 Detailed Use Case Descriptions

#### UC-04: Record Absence

* **Actor:** Teacher
* **Preconditions:** The teacher is logged in and assigned to the module.
* **Basic Flow:**
1. Teacher selects the specific module and class session.
2. System displays the list of enrolled students.
3. Teacher identifies the absent student(s).
4. Teacher adds a comment (optional) regarding the absence.
5. Teacher submits the record.


* **Post-conditions:** Absence is recorded in the database as "Unjustified" by default.

#### UC-08: Critical Absence Alert

* **Actor:** Teacher
* **Description:** The system maintains a logic gate where if $A_{unjustified} > 3$, the student is flagged.
* **Basic Flow:**
1. Teacher accesses the "Alerts" page.
2. System queries the database for students where the count of unjustified absences is greater than three.
3. System displays a prioritized list of these students.



---

## 4. Non-Functional Requirements

### 4.1 Security

* **Authentication:** All users must authenticate via a secure login portal.
* **Authorization:** Role-Based Access Control (RBAC) must ensure teachers cannot modify global user databases and students (if they have view access) cannot modify records.

### 4.2 Usability

* **Alerting System:** The alert for $>3$ unjustified absences must be visually distinct (e.g., highlighted in red) to ensure immediate faculty awareness.
* **Filtering:** Administrative staff must be able to filter records by "Module" or "Student Name" to handle high volumes of data efficiently.

### 4.3 Data Integrity

* **Referential Integrity:** A Referring Teacher cannot add a student to a module unless that student already exists in the Administrator's global database.

---

## 5. Next Steps

Would you like me to create a **Sequence Diagram** for the "Justify Absence" workflow to show how data moves between the Admin Staff and the database?
