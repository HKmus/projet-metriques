# Software Requirements Specification (SRS)
## For the Kiestla Student Attendance Portal

**Version:** 1.0
**Date:** October 26, 2023
**Prepared by:** Software Requirements Analyst

---

## Table of Contents

1.  **Introduction**
    1.1 Purpose
    1.2 Scope
    1.3 Definitions, Acronyms, and Abbreviations
    1.4 References
2.  **Overall Description**
    2.1 Product Perspective
    2.2 User Characteristics
    2.3 Operating Environment
    2.4 Design and Implementation Constraints
    2.5 Assumptions and Dependencies
3.  **Functional Requirements (Use Case Model)**
    3.1 Actors
    3.2 Use Case Diagram
    3.3 Use Case Descriptions
    3.4 Functional Requirements List
4.  **Non-Functional Requirements**
    4.1 Usability
    4.2 Reliability
    4.3 Performance
    4.4 Security
5.  **Other Requirements**

---

## 1. Introduction

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a detailed overview of the software requirements for the www.kiestla.edu student attendance portal. This document describes the project's target audience, user interface, hardware and software requirements, and functional and non-functional requirements. It is intended to guide the development team and provide a clear baseline for validation by the stakeholders.

### 1.2 Scope
This software system is a web-based portal to be named the "Kiestla Attendance Portal." The system will digitize and streamline the process of tracking and justifying student absences. It will serve three primary user roles: Administrator, Teaching Staff, and Administrative Staff. The scope includes the management of users (students and teachers) and teaching modules, the recording of absences by teachers, the justification of absences by administrative staff, and the generation of alerts for students exceeding a threshold of unjustified absences. The system is exclusively for internal use by the staff of Kiestla.edu.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification.
- **User:** A generic term for anyone who logs into the system (Administrator, Teacher, Admin Staff).
- **Module:** A specific course or teaching unit (e.g., "Advanced Mathematics 101").
- **Referring Teacher:** The teacher primarily responsible for a module, with the authority to add other teachers and students to that module.
- **Global Database:** The central repository of all registered students and teachers within the institution.
- **Unjustified Absence:** An absence that has been recorded by a teacher but has not yet had a reason entered by administrative staff.

### 1.4 References
- Project Specifications: Description and Functionalities provided by the stakeholder.

---

## 2. Overall Description

### 2.1 Product Perspective
The Kiestla Attendance Portal is a new, stand-alone web application. It relies on a central "Global Database" of students and teachers, which exists and is managed outside the core attendance functionalities of this system (by the Administrator). The system will interface with this database to authenticate users and retrieve user information for associating with modules.

### 2.2 User Characteristics
- **Administrator:** A technical or senior academic user with the highest level of privileges. Responsible for the structural setup of the system (modules and their associations). Assumed to be computer literate.
- **Referring Teacher:** An academic user responsible for one or more specific modules. Needs to manage the class list for their modules and report absences. Moderate computer literacy.
- **Administrative Staff:** A non-academic user responsible for processing absence justifications. Needs a comprehensive view of all absence data. Moderate computer literacy.
- **Student:** Not a direct user of this portal. They are data entities within the system whose attendance is tracked.

### 2.3 Operating Environment
The system will operate in a standard web-based environment.
- **Platform:** Accessed via modern web browsers (e.g., latest versions of Chrome, Firefox, Safari, Edge) on desktop and laptop computers.
- **Server:** The application will be hosted on a standard web/application server with connectivity to the Global Database.

### 2.4 Design and Implementation Constraints
- **Technology:** The system must be developed as a web application.
- **Database Integration:** The system must integrate with the existing "Global Database" for user data. It cannot create students or teachers outside of this database; it can only reference them.
- **Security:** Access must be strictly controlled based on user roles.

### 2.5 Assumptions and Dependencies
- **Assumption:** The "Global Database" of students and teachers is accurate, up-to-date, and maintained by a separate process.
- **Assumption:** All users have unique login credentials (e.g., university ID and password) that are recognized by the system.
- **Dependency:** The successful operation of this system depends on the availability and stability of the "Global Database."

---

## 3. Functional Requirements (Use Case Model)

### 3.1 Actors
- **Administrator:** The user who manages the core structure of the system.
- **Referring Teacher:** The user responsible for a module, who manages its roster and records absences.
- **Teacher:** A user who can record absences for a module they are associated with. (Note: A Referring Teacher is a specialization of a Teacher).
- **Administrative Staff:** The user who justifies absences and monitors overall attendance.

### 3.2 Use Case Diagram

*(A textual representation of the diagram is provided below. In a real document, a graphical UML diagram would be included here.)*

```
[System Boundary: Kiestla Attendance Portal]

    +-------------------------------------+
    |                                     |
    |  (UC-01) Manage Modules             |<----[Administrator]
    |  (UC-02) Manage Module Teachers     |<----[Administrator]
    |                                     |
    |  (UC-03) Manage Module Roster       |<----[Referring Teacher]
    |  (UC-04) Report Absence             |<----[Teacher] <<includes>> (UC-07) Select Student
    |  (UC-05) Add Comment to Absence     |<----[Teacher] (extends UC-04)
    |  (UC-06) Consult Module Absences    |<----[Teacher]
    |                                     |
    |  (UC-07) Justify Absence            |<----[Admin Staff]
    |  (UC-08) View All Absences          |<----[Admin Staff]
    |  (UC-09) Filter Absences (by Module)|<----[Admin Staff] (extends UC-08)
    |  (UC-10) Filter Absences (by Student)|<----[Admin Staff] (extends UC-08)
    |  (UC-11) View Absence Alerts        |<----[Admin Staff, Teacher]
    +-------------------------------------+
```

### 3.3 Use Case Descriptions

#### Actor: Administrator

- **UC-01: Manage Modules**
    - **Description:** The Administrator creates, updates, and deletes teaching modules.
    - **Main Flow:**
        1.  The Administrator logs in and navigates to the module management section.
        2.  The system displays a list of existing modules.
        3.  The Administrator can initiate actions to add a new module, edit an existing one's details (e.g., name, code), or delete a module (subject to confirmation).

- **UC-02: Manage Module Teachers**
    - **Description:** The Administrator assigns one or more referring teachers to a specific module.
    - **Main Flow:**
        1.  The Administrator selects a specific module from the list (UC-01).
        2.  The system displays the teachers currently associated with the module.
        3.  The Administrator searches the Global Database for a teacher and assigns them as a "Referring Teacher" for the module.
        4.  The system confirms the new association.

#### Actor: Referring Teacher

- **UC-03: Manage Module Roster**
    - **Description:** The Referring Teacher adds or removes students from the roster of a module they are responsible for. Students must already exist in the Global Database.
    - **Main Flow:**
        1.  The Referring Teacher logs in and selects their module.
        2.  The system displays the module's current student roster.
        3.  The Referring Teacher searches the Global Database for a student and adds them to the roster, or removes an existing student.
        4.  The system updates and confirms the roster change.

#### Actor: Teacher (including Referring Teacher)

- **UC-04: Report Absence**
    - **Description:** A teacher records an absence for a student in a specific module.
    - **Precondition:** The teacher is associated with the module, and the student is on the module's roster.
    - **Main Flow:**
        1.  The Teacher logs in and selects a module they teach.
        2.  The system displays the class roster for that module.
        3.  The Teacher selects a student from the list (UC-07: Select Student).
        4.  The system prompts for the date of the absence.
        5.  The Teacher enters the date and confirms the absence.
        6.  The system records the absence with a status of "Unjustified".

- **UC-05: Add Comment to Absence**
    - **Description:** While reporting an absence, the teacher can add an optional textual comment (e.g., "Student was feeling unwell," "Left early for an appointment").
    - **Main Flow:** This use case extends UC-04. After selecting a student and date, the Teacher has the option to type a comment into a text field before confirming the absence.

- **UC-06: Consult Module Absences**
    - **Description:** A teacher views a list of all absences recorded for students in their specific modules.
    - **Main Flow:**
        1.  The Teacher logs in and selects a module.
        2.  The Teacher navigates to an "Absence List" or similar view.
        3.  The system displays a list of all absences for students in that module, including dates, any teacher comments, and their justification status.

- **UC-11: View Absence Alerts**
    - **Description:** Teaching staff can view a list of students who have more than three unjustified absences across any of their modules.
    - **Main Flow:**
        1.  The Teacher logs in and navigates to the "Alerts" or "Monitoring" page.
        2.  The system automatically displays a list of students (across all modules the teacher has access to) who have accumulated more than three unjustified absences.

#### Actor: Administrative Staff

- **UC-07: Justify Absence**
    - **Description:** Administrative staff enters a reason for a specific absence, changing its status from "Unjustified" to "Justified".
    - **Main Flow:**
        1.  The Administrative Staff logs in and views a list of absences (from UC-08).
        2.  They locate a specific absence record (potentially using filters UC-09, UC-10).
        3.  They select the absence and choose the "Justify" action.
        4.  The system prompts for a reason or justification type (e.g., "Medical certificate received," "Family emergency").
        5.  The staff member enters the reason and confirms.
        6.  The system updates the absence record's status to "Justified".

- **UC-08: View All Absences**
    - **Description:** Administrative staff can see a comprehensive list of all absences recorded in the system for all students.
    - **Main Flow:**
        1.  The Administrative Staff logs in.
        2.  They navigate to the "All Absences" section.
        3.  The system displays a complete, paginated list of all absence records, showing student, module, date, teacher comment, and justification status.

- **UC-09: Filter Absences by Module**
    - **Description:** From the "All Absences" view, administrative staff can narrow down the list to show only absences for a specific module. (Extends UC-08).

- **UC-10: Filter Absences by Student**
    - **Description:** From the "All Absences" view, administrative staff can narrow down the list to show only absences for a specific student. (Extends UC-08).

- **UC-11: View Absence Alerts**
    - **Description:** Administrative staff can also view the list of students with more than three unjustified absences.
    - **Main Flow:**
        1.  The Administrative Staff logs in and navigates to the "Alerts" page.
        2.  The system displays a list of all students in the institution who have accumulated more than three unjustified absences.

### 3.4 Functional Requirements List

- **FR-01:** The system shall authenticate all users based on their role (Administrator, Teacher, Admin Staff).
- **FR-02:** The system shall allow an Administrator to perform Create, Read, Update, and Delete (CRUD) operations on teaching modules.
- **FR-03:** The system shall allow an Administrator to associate one or more referring teachers with a teaching module.
- **FR-04:** The system shall allow a Referring Teacher to add a student from the Global Database to a module's roster.
- **FR-05:** The system shall allow a Referring Teacher to remove a student from a module's roster.
- **FR-06:** The system shall allow a Teacher associated with a module to report an absence for a student on that module's roster.
- **FR-07:** The system shall allow a Teacher to add an optional text comment when reporting an absence.
- **FR-08:** The system shall store the status of each absence (e.g., 'Unjustified', 'Justified').
- **FR-09:** The system shall allow a Teacher to view a list of absences for students in their modules, including justification status.
- **FR-10:** The system shall allow Administrative Staff to view a complete list of all absences for all students.
- **FR-11:** The system shall allow Administrative Staff to filter the all-absence list by student and by module.
- **FR-12:** The system shall allow Administrative Staff to update an absence record with a reason, thereby changing its status to 'Justified'.
- **FR-13:** The system shall provide a dedicated page/view that lists all students with more than three unjustified absences. This view shall be accessible to Teachers and Administrative Staff.

---

## 4. Non-Functional Requirements

### 4.1 Usability
- **NFR-01:** The user interface shall be intuitive and require minimal training for teachers and administrative staff to perform their core tasks (reporting/viewing absences).
- **NFR-02:** The system shall be accessible in English.

### 4.2 Reliability
- **NFR-03:** The system shall have an uptime of 99.5% during core academic hours (e.g., 8:00 AM to 8:00 PM).
- **NFR-04:** In case of a system failure, the most recently recorded data shall not be lost.

### 4.3 Performance
- **NFR-05:** The system shall load the main dashboard and absence lists within 3 seconds under normal network conditions.
- **NFR-06:** Recording an absence shall be confirmed to the user within 2 seconds of submission.
- **NFR-07:** The system shall support at least 200 concurrent users (teachers and admin staff) during peak times (e.g., end of month).

### 4.4 Security
- **NFR-08:** All access to the system shall be protected by a secure login mechanism (username/password).
- **NFR-09:** User permissions shall be strictly enforced. A teacher must not be able to view absences for modules they are not associated with. Admin staff must not be able to modify module structures.
- **NFR-10:** All communication between the user's browser and the web server shall be encrypted using HTTPS.
- **NFR-11:** The system must integrate securely with the external Global Database without exposing its credentials or other data.

---

## 5. Other Requirements
- **OR-01:** The system shall comply with all relevant institutional and regional data protection regulations regarding the storage of student educational records.
- **OR-02:** Upon project completion, the vendor shall provide user manuals for each user role (Administrator, Teacher, Admin Staff).
