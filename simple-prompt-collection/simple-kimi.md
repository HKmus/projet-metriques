 # Software Requirements Specification (SRS)

## Student Attendance Management System
### www.kiestla.edu Portal

---

**Document Version:** 1.0  
**Date:** February 24, 2026  
**Author:** Software Requirements Analyst  
**Status:** Draft

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features (Use Cases)](#3-system-features-use-cases)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Appendices](#6-appendices)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the **Student Attendance Management System** (SAMS) for www.kiestla.edu. The system is designed to streamline attendance tracking across teaching modules, connecting students, teachers, and administrative staff in a unified workflow from absence recording to justification.

### 1.2 Scope
The SAMS portal will provide:
- **Administrator management** of teaching modules and user databases
- **Teacher capabilities** for recording absences with comments and viewing absence reports
- **Administrative staff functions** for justifying absences and monitoring attendance patterns
- **Automated alerting** for students exceeding absence thresholds

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|------------|
| **SAMS** | Student Attendance Management System |
| **Referring Teacher** | Primary teacher responsible for a module who can manage enrollments |
| **Module** | Teaching unit/course subject |
| **Unjustified Absence** | Absence without administrative-approved reason |
| **Justification** | Administrative validation of absence reason |

### 1.4 References
- Project Description Document (PDD) v1.0
- Educational Institution Data Protection Guidelines

---

## 2. Overall Description

### 2.1 Product Perspective
The SAMS is a standalone web portal that serves as the central hub for attendance management. It maintains a global database of users (students and teachers) and manages the relationships between users, modules, and absence records.

### 2.2 User Classes and Characteristics

| User Class | Characteristics | Privilege Level |
|------------|----------------|-----------------|
| **Administrator** | System-level management, full database control | Highest |
| **Referring Teacher** | Module ownership, enrollment management, absence recording | High |
| **Teacher** | Absence recording and viewing for assigned modules | Medium |
| **Administrative Staff** | Absence justification and comprehensive reporting | High |
| **Student** | Subject of attendance records (view-only implied) | Low |

### 2.3 Operating Environment
- Web-based application accessible via modern browsers
- Server-side database for user and attendance data storage
- Responsive design for potential mobile access

### 2.4 Design and Implementation Constraints
- Must comply with educational data privacy regulations
- Role-based access control required
- Audit trail for all absence modifications

---

## 3. System Features (Use Cases)

### 3.1 Use Case Diagram Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      STUDENT ATTENDANCE SYSTEM                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │Administrator│ │Referring│  │ Teacher  │  │ Admin    │        │
│  │            │ │ Teacher │  │          │  │ Staff    │        │
│  └────┬───────┘ └────┬────┘  └────┬─────┘  └────┬─────┘        │
│       │              │            │             │               │
│       ▼              ▼            ▼             ▼               │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           MODULE MANAGEMENT (UC-01)                  │      │
│  │  • Create module    • Maintain module                │      │
│  │  • Delete module    • Assign referring teacher       │      │
│  └──────────────────────────────────────────────────────┘      │
│       ▲              ▲                                    │
│       │              │                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           USER DATABASE MANAGEMENT (UC-02)           │      │
│  │  • Manage students  • Manage teachers                │      │
│  └──────────────────────────────────────────────────────┘      │
│       ▲              ▲            ▲             │               │
│       │              │            │             │               │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           MODULE ENROLLMENT (UC-03)                  │      │
│  │  • Add students to module  • Add teachers to module  │      │
│  └──────────────────────────────────────────────────────┘      │
│                      ▲            ▲                            │
│                      │            │                            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           ABSENCE RECORDING (UC-04)                  │      │
│  │  • Record absence  • Add comment                     │      │
│  └──────────────────────────────────────────────────────┘      │
│                      ▲            ▲                            │
│                      │            │                            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           ABSENCE CONSULTATION (UC-05)               │      │
│  │  • View by module  • View by student                 │      │
│  └──────────────────────────────────────────────────────┘      │
│                                    ▲             ▲             │
│                                    │             │             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           ABSENCE JUSTIFICATION (UC-06)              │      │
│  │  • Enter reason  • Access all records                │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                  │             │
│                                                  ▼             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           ALERT MANAGEMENT (UC-07)                   │      │
│  │  • Alert on >3 unjustified absences                  │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3.2 Detailed Use Case Specifications

#### **UC-01: Module Management**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Manage Teaching Modules |
| **Primary Actor** | Administrator |
| **Secondary Actors** | Referring Teacher (as assignee) |
| **Description** | The administrator manages the lifecycle of teaching modules including creation, modification, deletion, and teacher assignment. |
| **Trigger** | Administrator initiates module management from dashboard |
| **Preconditions** | Administrator is authenticated and authorized |
| **Postconditions** | Module database is updated; referring teachers are notified of assignments |

**Basic Flow:**
1. Administrator selects "Module Management" from main menu
2. System displays list of existing modules with search/filter options
3. Administrator chooses action: Create, Edit, or Delete
4. **If Create:**
   - 4a. System presents module creation form (name, code, description, credits)
   - 4b. Administrator enters module details
   - 4c. System validates unique module code
   - 4d. Administrator selects referring teacher from database
   - 4e. System confirms creation and notifies assigned teacher
5. **If Edit:**
   - 5a. System retrieves selected module data
   - 5b. Administrator modifies fields (name, description, referring teacher)
   - 5c. System validates changes and updates associations
6. **If Delete:**
   - 6a. System checks for existing absence records
   - 6b. If records exist, system warns of data preservation requirements
   - 6c. Administrator confirms deletion or archival
   - 6d. System removes module or marks as inactive

**Alternative Flows:**
- **4c-A1:** Module code exists → System prompts for unique code
- **6b-A1:** Existing records → System offers "archive" option instead of deletion

**Exception Flows:**
- Database connection failure → System displays error, logs incident, maintains data integrity

**Business Rules:**
- BR-01: Module codes must be unique and follow institutional naming convention
- BR-02: Each module must have exactly one referring teacher
- BR-03: Deleted modules with historical data must be archived, not purged

---

#### **UC-02: User Database Management**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-02 |
| **Use Case Name** | Manage Global User Database |
| **Primary Actor** | Administrator |
| **Secondary Actors** | None |
| **Description** | The administrator maintains the central registry of all students and teachers in the system. |
| **Trigger** | New academic year, new hires, or student enrollment changes |
| **Preconditions** | Administrator authenticated; institutional data available |
| **Postconditions** | User database updated; affected modules reflect changes |

**Basic Flow:**
1. Administrator accesses "User Database" management section
2. System presents tabbed interface: Students | Teachers
3. Administrator selects user type to manage
4. **For Students:**
   - 4a. System displays student list with filters (program, year, status)
   - 4b. Administrator adds new student (ID, name, email, program, enrollment date)
   - 4c. System validates student ID uniqueness
   - 4d. Administrator edits existing student data
   - 4e. Administrator deactivates/activates student status
5. **For Teachers:**
   - 5a. System displays teacher directory with department filters
   - 5b. Administrator adds new teacher (ID, name, email, department, specialization)
   - 5c. System validates teacher ID uniqueness
   - 5d. Administrator edits teacher profiles
   - 5e. Administrator manages teacher active status

**Alternative Flows:**
- Bulk import: Administrator uploads CSV → System validates and imports batch data

**Business Rules:**
- BR-04: Student IDs must be unique and immutable
- BR-05: Teacher IDs must be unique and immutable
- BR-06: Deactivated users cannot be assigned to new modules but retain historical data

---

#### **UC-03: Module Enrollment Management**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-03 |
| **Use Case Name** | Manage Module Enrollments |
| **Primary Actor** | Referring Teacher |
| **Secondary Actors** | Administrator (indirect), Students, Teachers |
| **Description** | Referring teachers manage the roster of students and additional teachers for their assigned modules. |
| **Trigger** | Referring teacher accesses module enrollment page |
| **Preconditions** | User authenticated as referring teacher; module assigned to user; target users exist in global database |
| **Postconditions** | Enrollment records created; enrolled users gain module access |

**Basic Flow:**
1. Referring teacher views "My Modules" dashboard
2. System displays list of modules where user is referring teacher
3. Teacher selects specific module to manage
4. System shows current enrollment: enrolled students and teaching staff
5. Teacher selects "Add Students" or "Add Teachers"
6. **Add Students:**
   - 6a. System presents searchable list of active students from global database
   - 6b. Teacher selects students (multi-select enabled)
   - 6c. System validates students not already enrolled
   - 6d. System adds students to module roster
   - 6e. System notifies students of enrollment
7. **Add Teachers:**
   - 7a. System presents searchable list of teachers from global database
   - 7b. Teacher selects additional teaching staff
   - 7c. System validates selections
   - 7d. System grants teaching privileges for module
   - 7e. System notifies added teachers

**Alternative Flows:**
- **6c-A1:** Student already enrolled → System skips duplicate, alerts teacher
- Remove enrollment: Teacher selects user → System confirms → Removes access (retains historical absence data)

**Business Rules:**
- BR-07: Only referring teachers can modify module enrollment
- BR-08: Users must exist in global database before enrollment
- BR-09: Enrollment changes are logged with timestamp and actor

---

#### **UC-04: Absence Recording**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-04 |
| **Use Case Name** | Record Student Absence |
| **Primary Actor** | Teacher (including Referring Teacher) |
| **Secondary Actors** | Student (notification recipient) |
| **Description** | Teachers record student absences during class sessions with optional contextual comments. |
| **Trigger** | Teacher identifies absent student during module session |
| **Preconditions** | Teacher authenticated; teacher assigned to module; student enrolled in module |
| **Postconditions** | Absence record created; justification status set to "pending"; alert system updated |

**Basic Flow:**
1. Teacher accesses "Record Absence" function
2. System displays teacher's assigned modules (default to current session if identifiable)
3. Teacher selects module and session date/time
4. System displays enrolled student list with attendance status indicators
5. Teacher marks student as "Absent"
6. System highlights absence for confirmation
7. Teacher enters optional comment (max 500 chars): reason given, circumstances, etc.
8. System validates input
9. Teacher confirms submission
10. System creates absence record with:
    - Student ID, Module ID, Date/Time
    - Recording teacher ID, Comment
    - Status: "Unjustified" (pending administrative review)
    - Timestamp of record creation
11. System updates student absence count
12. System checks threshold (>3 unjustified) and triggers alert if met

**Alternative Flows:**
- **5-A1:** Bulk absence recording: Teacher selects multiple students → System applies same session data to all
- **7-A1:** Late arrival: Teacher marks "Late" → System records as partial absence per institutional policy

**Exception Flows:**
- Student not enrolled → System alerts teacher, prevents recording
- Session date in future → System warns and requires confirmation

**Business Rules:**
- BR-10: Absence records are immutable once submitted (corrections require administrative override)
- BR-11: Comments are optional but recommended for transparency
- BR-12: All absence records initially marked as "unjustified" until administrative review

---

#### **UC-05: Absence Consultation**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-05 |
| **Use Case Name** | Consult Absence Records |
| **Primary Actor** | Teacher / Administrative Staff |
| **Secondary Actors** | None |
| **Description** | Authorized users view absence records filtered by module or student with aggregation capabilities. |
| **Trigger** | User requests absence report |
| **Preconditions** | User authenticated; user has module access (teachers) or administrative privileges |
| **Postconditions** | Report displayed; export options available |

**Basic Flow:**
1. User selects "Absence Reports" from navigation
2. System presents filter options:
   - View by: Module | Student
   - Date range: Today | Week | Month | Custom | All time
   - Status: All | Unjustified | Justified | Pending
3. **If "By Module" selected:**
   - 3a. User selects from accessible modules
   - 3b. System displays module absence summary:
       - Total sessions, Total absences, Absence rate
       - List of absent students with dates and status
       - Grouping by session date
4. **If "By Student" selected:**
   - 4a. User searches/selects student
   - 4b. System displays student absence portfolio:
       - All modules where student has absences
       - Chronological absence history
       - Justification status per absence
       - Running total of unjustified absences
5. User selects specific absence for detailed view
6. System displays full record including comments and audit trail

**Alternative Flows:**
- Export: User selects "Export" → System generates PDF/CSV of current view
- Print: User selects "Print" → System formats printer-friendly version

**Business Rules:**
- BR-13: Teachers can only view absence data for their assigned modules
- BR-14: Administrative staff can view all student absence records across all modules
- BR-15: Data exports must include generation timestamp and user identification

---

#### **UC-06: Absence Justification**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-06 |
| **Use Case Name** | Justify Absence |
| **Primary Actor** | Administrative Staff |
| **Secondary Actors** | Student (notification recipient), Teachers (module staff) |
| **Description** | Administrative staff review and justify student absences, converting "unjustified" records to "justified" with official reason documentation. |
| **Trigger** | Student submits justification documentation; or administrative review initiated |
| **Preconditions** | Staff authenticated; absence record exists in "unjustified" status |
| **Postconditions** | Absence status updated; alert thresholds recalculated; notifications sent |

**Basic Flow:**
1. Staff accesses "Absence Justification" queue
2. System displays list of unjustified absences pending review, sorted by date (oldest first)
3. System provides filtering: by student, by module, by date range, by urgency (alert threshold proximity)
4. Staff selects specific absence record to review
5. System displays:
   - Student information
   - Module and session details
   - Recording teacher and comment
   - Days since absence (aging indicator)
6. Staff reviews supporting documentation (uploaded or physical reference)
7. Staff selects action: Justify or Reject
8. **If Justify:**
   - 8a. Staff selects/enters justification reason from standardized list (medical, family emergency, institutional activity, etc.)
   - 8b. Staff enters detailed explanation (optional)
   - 8c. Staff uploads supporting document reference (optional)
   - 8d. System updates record status to "Justified"
   - 8e. System recalculates student's unjustified absence count
   - 8f. System removes alert if count drops below threshold
9. **If Reject:**
   - 9a. Staff enters rejection reason
   - 9b. System maintains "Unjustified" status
   - 9c. System flags for potential follow-up if threshold exceeded

10. System logs justification action with staff ID and timestamp
11. System notifies student of decision
12. System notifies module teachers of status change

**Alternative Flows:**
- **8a-A1:** Bulk justification: Staff selects multiple related absences (e.g., medical leave spanning multiple days) → System applies same justification to all

**Exception Flows:**
- Record already justified → System displays current status, prevents duplicate action
- Missing documentation → System allows "pending documentation" hold status

**Business Rules:**
- BR-16: Only administrative staff can justify absences (teachers cannot)
- BR-17: Justification reasons must be standardized for reporting consistency
- BR-18: All justification actions are permanently logged for audit purposes
- BR-19: Justification can be retroactive but must include explanation for delay

---

#### **UC-07: Absence Alert Management**

| Attribute | Description |
|-----------|-------------|
| **Use Case ID** | UC-07 |
| **Use Case Name** | Monitor and Alert on Excessive Absences |
| **Primary Actor** | System (automated) / Administrative Staff |
| **Secondary Actors** | Referring Teachers, Teachers, Students |
| **Description** | The system automatically identifies students exceeding three unjustified absences and alerts teaching staff through a dedicated dashboard. |
| **Trigger** | Absence record creation/update causes unjustified count to exceed threshold |
| **Preconditions** | Absence justification system active; threshold configured (default: 3) |
| **Postconditions** | Alert generated; staff notified; intervention workflow initiated |

**Basic Flow:**
1. System detects condition: Student's unjustified absence count > 3
2. System creates alert record containing:
   - Student identification and contact info
   - Current unjustified absence count
   - List of unjustified absences (dates, modules, comments)
   - Days since first threshold breach
   - Alert severity: Warning (4 absences) | Critical (5+ absences)
3. System updates "Alerts Dashboard" accessible to:
   - Administrative staff (all alerts)
   - Referring teachers (alerts for their modules' students)
   - Teachers (alerts for their specific module enrollments)
4. Alert dashboard displays:
   - Sortable list of at-risk students
   - Visual indicators (color coding: yellow for 4, red for 5+)
   - Quick action links: View details, Contact student, Schedule meeting
5. Staff acknowledges alert review
6. System logs acknowledgment

**Alert Resolution Paths:**
- **Path A - Justification:** Staff justifies absence → System recalculates → If count ≤3, alert auto-resolves
- **Path B - Intervention:** Staff records intervention action (meeting, warning letter, etc.) → Alert remains active with intervention noted
- **Path C - Escalation:** Staff escalates to academic affairs → Alert status updated to "Escalated"

**Alternative Flows:**
- Threshold configuration: Administrator adjusts threshold per module or institutional policy
- Alert suppression: Staff marks as "Under Review" to pause notifications temporarily

**Business Rules:**
- BR-20: Alert threshold default is 3 unjustified absences, configurable by administrator
- BR-21: Alerts persist until unjustified count drops below threshold or academic decision rendered
- BR-22: All alert views and acknowledgments are logged
- BR-23: Students are not directly alerted by the system (institutional policy decision)

---

### 3.3 Use Case Relationships

| Relationship | From | To | Type | Description |
|--------------|------|-----|------|-------------|
| **Include** | UC-03 (Enrollment) | UC-02 (User DB) | Mandatory | Enrollment requires existing users |
| **Include** | UC-04 (Recording) | UC-07 (Alerts) | Mandatory | Recording triggers alert evaluation |
| **Include** | UC-06 (Justification) | UC-07 (Alerts) | Mandatory | Justification may resolve alerts |
| **Extend** | UC-05 (Consultation) | UC-06 (Justification) | Optional | Staff can justify from consultation view |
| **Extend** | UC-01 (Module Mgmt) | UC-03 (Enrollment) | Optional | Enrollment can follow module creation |

---

## 4. External Interface Requirements

### 4.1 User Interfaces

**UI-01: Responsive Web Design**
- Compatible with Chrome, Firefox, Safari, Edge (latest 2 versions)
- Mobile-responsive for tablet-based attendance recording

**UI-02: Dashboard Layout**
- Role-based landing pages showing relevant functions
- Quick action buttons for frequent tasks
- Notification center for alerts and system messages

**UI-03: Forms and Validation**
- Real-time validation with inline error messages
- Required field indicators
- Character limits enforced (e.g., comments 500 chars)

### 4.2 Hardware Interfaces
- Support for barcode/RFID student ID scanning (future consideration)
- Touch-screen optimized for classroom use

### 4.3 Software Interfaces
- Integration with institutional LDAP/Active Directory for authentication (optional)
- Calendar system integration for session scheduling
- Email notification system SMTP configuration

### 4.4 Communications Interfaces
- HTTPS/TLS 1.3 for all data transmission
- RESTful API architecture for potential mobile app development

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement |
|----|-------------|
| **PERF-01** | Page load time < 2 seconds for standard reports |
| **PERF-02** | Absence recording transaction < 1 second |
| **PERF-03** | Support for 1000 concurrent users during peak (class change periods) |
| **PERF-04** | Database queries for absence reports < 3 seconds for 10,000 record datasets |

### 5.2 Security Requirements

| ID | Requirement |
|----|-------------|
| **SEC-01** | Role-based access control (RBAC) enforced at every endpoint |
| **SEC-02** | Password policy: minimum 12 characters, complexity requirements, 90-day rotation |
| **SEC-03** | Session timeout after 30 minutes inactivity |
| **SEC-04** | All absence data modifications logged with IP address and timestamp |
| **SEC-05** | SQL injection and XSS prevention through parameterized queries and output encoding |
| **SEC-06** | GDPR/privacy compliance: student data encryption at rest |

### 5.3 Availability and Reliability

| ID | Requirement |
|----|-------------|
| **AVAIL-01** | 99.5% uptime during academic terms (scheduled maintenance in breaks) |
| **AVAIL-02** | Daily automated backups with 30-day retention |
| **AVAIL-03** | Disaster recovery plan with < 4 hour RTO (Recovery Time Objective) |

### 5.4 Usability Requirements

| ID | Requirement |
|----|-------------|
| **USE-01** | New user training time < 30 minutes for basic functions |
| **USE-02** | Context-sensitive help available on all pages |
| **USE-03** | Accessibility compliance with WCAG 2.1 Level AA |

### 5.5 Scalability Requirements

| ID | Requirement |
|----|-------------|
| **SCALE-01** | Support for 50,000 student records and 5,000 teacher records |
| **SCALE-02** | Support for 10,000 concurrent modules per academic year |
| **SCALE-03** | Absence record retention for 7 years (institutional requirement) |

---

## 6. Appendices

### Appendix A: Data Model Overview

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    USERS        │       │    MODULES      │       │   ABSENCES      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ PK user_id      │◄──────┤ PK module_id    │◄──────┤ PK absence_id   │
│    first_name   │       │    module_code  │       │ FK student_id   │
│    last_name    │       │    module_name  │       │ FK module_id    │
│    email        │       │    description  │       │    absence_date │
│    role         │       │ FK referring_   │       │ FK recorded_by  │
│    status       │       │    teacher_id   │       │    comment      │
│    created_at   │       │    status       │       │    status       │
└─────────────────┘       │    created_at   │       │    created_at   │
         ▲                └─────────────────┘       │    justified_by │
         │                         ▲                │    justification│
         │                         │                │    reason       │
         │                ┌─────────────────┐       └─────────────────┘
         │                │ MODULE_ENROLL   │                ▲
         └────────────────┤ (junction)      │────────────────┘
                          ├─────────────────┤
                          │ FK module_id    │
                          │ FK user_id      │
                          │ enrollment_type │
                          │ (student/teacher│
                          │ enrolled_at     │
                          └─────────────────┘
```

### Appendix B: Glossary

- **Absence:** Non-attendance of an enrolled student at a scheduled module session
- **Justification:** Administrative validation that converts an absence from "unjustified" to "justified" status with documented reason
- **Module:** Academic course unit with defined curriculum and schedule
- **Referring Teacher:** Primary instructor responsible for module administration and enrollment management

### Appendix C: Open Issues

| ID | Issue | Impact | Resolution Target |
|----|-------|--------|-------------------|
| **ISS-01** | Integration with existing student information system | High | Phase 2 |
| **ISS-02** | Mobile app development for offline-then-sync absence recording | Medium | Phase 2 |
| **ISS-03** | Parent/guardian notification system for minor students | Medium | Policy decision pending |
| **ISS-04** | API for third-party calendar applications | Low | Future release |

---

**End of Document**

---

*This SRS establishes the foundation for the Student Attendance Management System development. All use cases are traceable to the original project specifications and provide comprehensive coverage of the described functionalities.*
