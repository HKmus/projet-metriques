# Software Requirements Specification (SRS)
## Kiestla Student Attendance Management System
**Document Version:** 1.0  
**Project:** www.kiestla.edu  
**Date:** February 24, 2026  
**Prepared by:** Software Requirements Analyst  

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for the Kiestla Student Attendance Management System (www.kiestla.edu). The system aims to simplify the management of student attendance control during classes by providing a centralized portal linking students, teachers, and administrative staff. This SRS uses a use-case-based approach to define system behavior from the user's perspective.

### 1.2 Scope
The Kiestla system is a web-based portal that:
- Manages teaching modules and their association with referring teachers
- Maintains a global database of teachers and students
- Enables teachers to record and consult student absences with comments
- Allows administrative staff to justify absences and generate reports
- Provides automated alerts for students exceeding absence thresholds
- Supports grouping and filtering of absence data by module and student

**Out of Scope:**
- Grade management or academic performance tracking
- Real-time biometric attendance verification
- Mobile native applications (responsive web design only)
- Integration with external payment or financial systems

### 1.3 Definitions, Acronyms, and Abbreviations
| Term | Definition |
|------|-----------|
| SRS | Software Requirements Specification |
| Actor | A role played by a user or external system interacting with the system |
| Use Case | A sequence of actions performed by the system to yield an observable result |
| Referring Teacher | Primary teacher responsible for a teaching module |
| Unjustified Absence | An absence record without an approved administrative reason |
| Module | A teaching unit/course managed within the system |

### 1.4 References
- IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications
- UML 2.5 Specification: Use Case Diagrams
- Institutional policies of Kiestla Educational Institution

### 1.5 Document Overview
Section 2 provides an overall description of the product. Section 3 details the use-case model with actors and use case specifications. Sections 4-6 cover interface, non-functional, and other requirements.

---

## 2. Overall Description

### 2.1 Product Perspective
The Kiestla system is a standalone web application that serves as the central attendance management hub for the institution. It interfaces with:
- Institutional authentication system (LDAP/SSO) for user login
- Email/SMS gateway for alert notifications
- Browser-based client interfaces (no native mobile apps)

```
[External Systems]
       │
       ▼
┌─────────────────┐
│  Kiestla Portal │◄──► [Users: Admin, Teachers, Staff, Students]
└─────────────────┘
       │
       ▼
[Database: Users, Modules, Absences, Justifications]
```

### 2.2 Product Functions Summary
1. User and role management (Administrator)
2. Teaching module CRUD operations and teacher assignment
3. Global user database management (teachers/students)
4. Absence reporting with comments (Teachers)
5. Absence consultation and filtering (Teachers, Admin Staff)
6. Absence justification and status management (Administrative Staff)
7. Automated alerting for excessive unjustified absences
8. Reporting: group absences by module/student

### 2.3 User Classes and Characteristics
| Actor | Description | Key Characteristics |
|-------|-------------|-------------------|
| **Administrator** | Manages system configuration, modules, and global user database | Technical proficiency; full system access; low frequency, high-impact actions |
| **Referring Teacher** | Primary instructor for a module; can associate existing users to their modules | Moderate technical skill; frequent absence reporting; needs quick data entry |
| **Teacher** | Instructors who report absences in modules they teach | Similar to Referring Teacher but without module management rights |
| **Administrative Staff** | Processes absence justifications and generates institutional reports | Detail-oriented; needs comprehensive search/filter capabilities |
| **Student** | Views own attendance record and absence status (read-only) | Minimal training; mobile-friendly access; privacy-sensitive |

### 2.4 Operating Environment
- **Server**: Linux/Windows server with PHP/Python/Node.js runtime, MySQL/PostgreSQL database
- **Client**: Modern web browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled
- **Network**: HTTPS encryption required; institutional intranet or public internet access
- **Accessibility**: WCAG 2.1 AA compliance for users with disabilities

### 2.5 Design and Implementation Constraints
- Must comply with institutional data privacy policies (FERPA/GDPR equivalent)
- All absence modifications must be auditable (who, when, what changed)
- System must support 500+ concurrent users during peak class hours
- Response time: <2 seconds for 95% of user interactions
- Data retention: Absence records retained for minimum 5 academic years

### 2.6 Assumptions and Dependencies
- Users have institutional email accounts for authentication and notifications
- Referring teachers have verified authority to manage their assigned modules
- Administrative staff follow institutional policies for absence justification
- System backups performed daily by institutional IT department

---

## 3. System Features: Use-Case Model

### 3.1 Actors
```
Primary Actors:
• Administrator
• Referring Teacher
• Teacher
• Administrative Staff
• Student

Secondary Actors:
• Email/SMS Notification Service
• Authentication System (SSO/LDAP)
```

### 3.2 Use Case Diagram (Textual Representation)
```
┌─────────────────┐
│  Administrator  │
└────────┬────────┘
         │
         ├──► Manage Teaching Modules (CRUD)
         ├──► Assign Referring Teacher to Module
         ├──► Manage Global User Database (Teachers/Students)
         └──► View System Audit Logs

┌─────────────────┐
│ Referring Teacher│
└────────┬────────┘
         │
         ├──► Add Existing Teacher/Student to Module
         ├──► Report Student Absence (with comment)
         ├──► Consult Absences for Module Students
         └──► Receive Alerts: Students >3 Unjustified Absences

┌─────────────────┐
│     Teacher     │
└────────┬────────┘
         │
         ├──► Report Student Absence (with comment)
         └──► Consult Absences for Module Students

┌─────────────────────┐
│ Administrative Staff│
└────────┬────────────┘
         │
         ├──► Enter/Update Absence Justification
         ├──► Consult All Student Absences
         ├──► Group Absences by Module/Student
         └──► Generate Absence Reports

┌─────────────────┐
│     Student     │
└────────┬────────┘
         │
         └──► View Personal Attendance Record
```

### 3.3 Use Case Specifications

#### UC-01: Manage Teaching Modules
| Field | Description |
|-------|-------------|
| **ID** | UC-01 |
| **Name** | Manage Teaching Modules |
| **Primary Actor** | Administrator |
| **Description** | Create, read, update, or delete teaching modules and associate them with referring teachers |
| **Preconditions** | Administrator is authenticated with elevated privileges |
| **Postconditions** | Module record is created/updated/deleted in database; referring teacher association is maintained |
| **Main Flow** | 1. Admin navigates to Module Management<br>2. System displays existing modules<br>3. Admin selects action (Create/View/Edit/Delete)<br>4. For Create/Edit: Admin enters module details (code, name, schedule, capacity)<br>5. Admin assigns one or more referring teachers from registered users<br>6. System validates data and saves changes<br>7. System confirms operation success |
| **Alternative Flows** | A1: Module code already exists → System displays error, returns to step 4<br>A2: Delete module with existing absences → System requires confirmation and archives records instead of hard delete |
| **Exceptions** | E1: Database connection failure → System logs error, displays maintenance message<br>E2: Unauthorized access attempt → System denies action, logs security event |
| **Business Rules** | BR-01: Module codes must be unique institution-wide<br>BR-02: At least one referring teacher must be assigned to active modules |

#### UC-02: Manage Global User Database
| Field | Description |
|-------|-------------|
| **ID** | UC-02 |
| **Name** | Manage Global User Database |
| **Primary Actor** | Administrator |
| **Description** | Add, update, deactivate, or search for teachers and students in the central repository |
| **Preconditions** | Administrator authenticated; user data source available |
| **Postconditions** | User record is created/updated/deactivated; changes reflected across all modules |
| **Main Flow** | 1. Admin accesses User Management<br>2. System displays search/filter interface<br>3. Admin searches or selects "Add New User"<br>4. For new user: Admin enters personal data, role (teacher/student), contact info<br>5. System validates uniqueness (email/student ID)<br>6. System creates account and sends activation credentials<br>7. For updates: Admin modifies fields and saves |
| **Alternative Flows** | A1: Duplicate email/student ID detected → System prompts for correction<br>A2: Bulk import via CSV → System validates file format, processes records, reports errors |
| **Exceptions** | E1: Invalid data format → System highlights errors, prevents save<br>E2: Network timeout during activation email → System queues retry, notifies admin |
| **Business Rules** | BR-03: Student IDs and teacher IDs must follow institutional format<br>BR-04: Deactivated users retain historical absence data but cannot log in |

#### UC-03: Add Existing Users to Module
| Field | Description |
|-------|-------------|
| **ID** | UC-03 |
| **Name** | Add Existing Users to Module |
| **Primary Actor** | Referring Teacher |
| **Description** | Enroll already-registered teachers or students into a module the actor refers |
| **Preconditions** | Referring Teacher is authenticated; module exists; users exist in global database |
| **Postconditions** | Selected users are enrolled in the module and appear in attendance rosters |
| **Main Flow** | 1. Referring Teacher selects "Manage Module Enrollment"<br>2. System displays module details and current enrollees<br>3. Teacher selects "Add Participants"<br>4. System provides search interface for global database<br>5. Teacher searches and selects users by name/ID<br>6. System confirms selection and adds users to module<br>7. System notifies added users (optional) |
| **Alternative Flows** | A1: User already enrolled → System displays warning, skips duplicate<br>A2: Search returns no results → Teacher can request admin to create missing user |
| **Exceptions** | E1: Module is archived/closed → System prevents enrollment changes<br>E2: Permission error → System denies action if teacher is not referring teacher for module |
| **Business Rules** | BR-05: Only referring teachers can modify module enrollment<br>BR-06: Students cannot be enrolled in more than one section of the same module |

#### UC-04: Report Student Absence
| Field | Description |
|-------|-------------|
| **ID** | UC-04 |
| **Name** | Report Student Absence |
| **Primary Actor** | Teacher, Referring Teacher |
| **Description** | Record a student's absence for a specific class session with optional comment |
| **Preconditions** | Teacher is authenticated; enrolled in module; student is enrolled in module; class session exists |
| **Postconditions** | Absence record created with status "Unjustified"; teacher can edit within 24h |
| **Main Flow** | 1. Teacher accesses "Take Attendance" for a module/session<br>2. System displays roster with presence checkboxes<br>3. Teacher marks student(s) as absent<br>4. Teacher optionally adds comment (e.g., "no notification received")<br>5. Teacher submits attendance<br>6. System creates absence records with timestamp, teacher ID, comment<br>7. System updates student's absence counter |
| **Alternative Flows** | A1: Teacher corrects absence within 24h → System allows edit/delete with audit trail<br>A2: Multiple sessions marked → System processes batch submission |
| **Exceptions** | E1: Session date is in the future → System prevents marking<br>E2: Student not found in module → System validates enrollment before allowing action |
| **Business Rules** | BR-07: Absences can only be reported for scheduled class sessions<br>BR-08: Comments are optional but encouraged for pattern analysis |

#### UC-05: Consult Absence Lists
| Field | Description |
|-------|-------------|
| **ID** | UC-05 |
| **Name** | Consult Absence Lists |
| **Primary Actor** | Teacher, Referring Teacher, Administrative Staff |
| **Description** | View and filter absence records for students in modules |
| **Preconditions** | Actor authenticated; has permission to view module/student data |
| **Postconditions** | Actor views filtered absence data; no data modification |
| **Main Flow** | 1. Actor selects "Absence Reports"<br>2. System presents filter options: by module, student, date range, justification status<br>3. Actor applies filters<br>4. System queries database and displays results in tabular format<br>5. Actor can export results to PDF/CSV (if permitted) |
| **Alternative Flows** | A1: Teacher views only their modules; Admin Staff views all<br>A2: Click student name → System shows detailed absence history for that student |
| **Exceptions** | E1: No records match filters → System displays "No results" message<br>E2: Large result set → System paginates results, offers summary statistics |
| **Business Rules** | BR-09: Teachers can only view absences for modules they teach<br>BR-10: Administrative Staff can view all institutional absence data |

#### UC-06: Justify Absence
| Field | Description |
|-------|-------------|
| **ID** | UC-06 |
| **Name** | Justify Absence |
| **Primary Actor** | Administrative Staff |
| **Description** | Review and assign official justification status to reported absences |
| **Preconditions** | Absence record exists with status "Unjustified"; Administrative Staff authenticated |
| **Postconditions** | Absence status updated to "Justified" or "Denied"; reason recorded; student notified |
| **Main Flow** | 1. Admin Staff accesses "Absence Justification Queue"<br>2. System displays unjustified absences sorted by date/student<br>3. Staff selects an absence record<br>4. Staff reviews teacher comment and student history<br>5. Staff selects justification outcome and enters official reason<br>6. Staff submits decision<br>7. System updates record, logs action, triggers notification to student/teacher |
| **Alternative Flows** | A1: Bulk justification for same reason → Staff selects multiple records, applies single decision<br>A2: Request additional documentation → System flags record, pauses timer, notifies student |
| **Exceptions** | E1: Concurrent modification by another staff member → System locks record during edit<br>E2: Invalid justification code → System validates against institutional policy codes |
| **Business Rules** | BR-11: Only Administrative Staff can change absence justification status<br>BR-12: Justification decisions are immutable after 48h except by supervisor override |

#### UC-07: Generate Absence Alerts
| Field | Description |
|-------|-------------|
| **ID** | UC-07 |
| **Name** | Generate Absence Alerts |
| **Primary Actor** | System (automated), Referring Teacher, Administrative Staff |
| **Description** | Automatically identify and alert teaching staff about students exceeding unjustified absence threshold |
| **Preconditions** | Absence records exist; threshold rule configured (default: >3 unjustified absences) |
| **Postconditions** | Alert generated; notified actors can view flagged students; audit log updated |
| **Main Flow** | 1. System runs scheduled job (daily) or triggers on absence update<br>2. System queries for students with unjustified absence count > threshold per module<br>3. System compiles alert list with student details, module, absence count<br>4. System notifies referring teachers via dashboard alert and email<br>5. Administrative Staff can view institutional alert dashboard<br>6. Teachers acknowledge alerts; system tracks acknowledgment |
| **Alternative Flows** | A1: Threshold adjusted per module → System uses module-specific rules<br>A2: Student submits justification pending → System temporarily excludes from alert count |
| **Exceptions** | E1: Notification service unavailable → System queues alerts, retries with exponential backoff<br>E2: False positive due to data error → Teacher can flag alert for admin review |
| **Business Rules** | BR-13: Default alert threshold is 3 unjustified absences per module per term<br>BR-14: Alerts reset at start of new academic term unless configured otherwise |

#### UC-08: View Personal Attendance (Student)
| Field | Description |
|-------|-------------|
| **ID** | UC-08 |
| **Name** | View Personal Attendance |
| **Primary Actor** | Student |
| **Description** | Allow students to view their own attendance record and absence justifications |
| **Preconditions** | Student authenticated; enrolled in at least one module |
| **Postconditions** | Student views read-only attendance summary; no data modification |
| **Main Flow** | 1. Student logs in and selects "My Attendance"<br>2. System displays list of enrolled modules<br>3. Student selects a module<br>4. System shows attendance summary: total sessions, present, absent, justified/unjustified<br>5. Student can view details of each absence including teacher comment and justification status |
| **Alternative Flows** | A1: Student downloads personal attendance report (PDF)<br>A2: Student sees pending justification requests and upload documentation link |
| **Exceptions** | E1: Student not enrolled in any active modules → System displays explanatory message<br>E2: Attempt to view another student's record → System denies access, logs attempt |
| **Business Rules** | BR-15: Students can only view their own attendance data<br>BR-16: Justification status updates reflected in student view within 1 hour |

### 3.4 Use Case Relationships
- **Include**: UC-04 (Report Absence) includes "Validate Session Enrollment"
- **Extend**: UC-07 (Generate Alerts) extends UC-05 (Consult Absences) when threshold exceeded
- **Generalization**: Teacher and Referring Teacher generalize to "Instructor" for shared use cases UC-04, UC-05

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Login Portal**: Role-based dashboard redirection post-authentication
- **Dashboard**: Personalized widgets (upcoming classes, pending justifications, alerts)
- **Attendance Grid**: Calendar/session view with color-coded presence status
- **Reporting Interface**: Filter panels, export buttons, visual charts (bar/line graphs)
- **Responsive Design**: Mobile-optimized views for teachers marking attendance on-the-go

### 4.2 Hardware Interfaces
- Server: Minimum 4-core CPU, 8GB RAM, SSD storage for database
- Client: No special hardware; standard devices with modern browsers
- Backup: Integration with institutional backup infrastructure

### 4.3 Software Interfaces
| Interface | Purpose | Protocol/Format |
|-----------|---------|----------------|
| Authentication System | User login and role verification | OAuth 2.0 / SAML |
| Email/SMS Gateway | Send alerts and notifications | SMTP / REST API |
| Database | Persistent storage of all entities | PostgreSQL 14+ with SSL |
| File Storage | Store uploaded justification documents | S3-compatible API |

### 4.4 Communications Interfaces
- All client-server communication via HTTPS (TLS 1.3)
- Internal microservices communication via gRPC or REST with API gateway
- Rate limiting: 100 requests/minute per user to prevent abuse

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- Page load time: <2 seconds for 95% of requests under normal load
- Attendance submission: <1 second response time
- Report generation: <10 seconds for datasets up to 10,000 records
- Support 500 concurrent users; scalable to 2000 with load balancing

### 5.2 Security Requirements
- **Authentication**: Multi-factor authentication optional for admin roles
- **Authorization**: Role-Based Access Control (RBAC) with principle of least privilege
- **Data Protection**: 
  - PII encrypted at rest (AES-256)
  - Absence comments sanitized to prevent XSS
- **Audit**: All CRUD operations on absence records logged with user, timestamp, IP
- **Compliance**: Adhere to institutional data retention and privacy policies

### 5.3 Software Quality Attributes
| Attribute | Requirement |
|-----------|-------------|
| **Reliability** | 99.5% uptime during academic terms; automated failover |
| **Maintainability** | Modular architecture; API documentation; <1 hour deployment cycle |
| **Usability** | Intuitive navigation; <15 minute training for new teachers; WCAG 2.1 AA |
| **Portability** | Containerized deployment (Docker); cloud-agnostic design |
| **Scalability** | Horizontal scaling of web tier; database read replicas for reporting |

### 5.4 Business Rules Summary
| ID | Rule |
|----|------|
| BR-01 | Module codes must be unique institution-wide |
| BR-02 | At least one referring teacher must be assigned to active modules |
| BR-03 | Student/teacher IDs must follow institutional format |
| BR-04 | Deactivated users retain historical data but cannot log in |
| BR-05 | Only referring teachers can modify module enrollment |
| BR-06 | Students cannot be enrolled in multiple sections of same module |
| BR-07 | Absences can only be reported for scheduled class sessions |
| BR-08 | Comments on absences are optional but encouraged |
| BR-09 | Teachers can only view absences for modules they teach |
| BR-10 | Administrative Staff can view all institutional absence data |
| BR-11 | Only Administrative Staff can change absence justification status |
| BR-12 | Justification decisions immutable after 48h except supervisor override |
| BR-13 | Default alert threshold: 3 unjustified absences per module per term |
| BR-14 | Alerts reset at start of new academic term unless configured otherwise |
| BR-15 | Students can only view their own attendance data |
| BR-16 | Justification status updates reflected in student view within 1 hour |

---

## 6. Other Requirements

### 6.1 Legal and Compliance
- System must support data subject access requests (DSAR) per privacy regulations
- Audit logs retained for 7 years for compliance investigations
- Terms of Use and Privacy Policy accessible from all pages

### 6.2 Documentation Requirements
- User manuals for each actor role (PDF and in-app help)
- Administrator technical guide for system maintenance
- API documentation for future integrations

### 6.3 Training Requirements
- Role-based onboarding tutorials within the application
- Video tutorials for common tasks (reporting absence, justifying records)
- Administrator training session for configuration management

### 6.4 Future Enhancements (Non-Binding)
- Mobile application for offline attendance marking
- Integration with learning management systems (LMS)
- Predictive analytics for at-risk student identification
- Multi-language support for international students

---

## Appendix A: Use Case Priority Matrix
| Use Case | Priority | Rationale |
|----------|----------|-----------|
| UC-04: Report Absence | High | Core functionality; daily use by teachers |
| UC-06: Justify Absence | High | Critical administrative workflow |
| UC-07: Generate Alerts | High | Proactive intervention requirement |
| UC-01: Manage Modules | Medium | Setup task; performed periodically |
| UC-02: Manage Users | Medium | Administrative overhead; bulk operations |
| UC-03: Add to Module | Medium | Module setup; less frequent |
| UC-05: Consult Absences | Medium | Reporting need; supports decision-making |
| UC-08: Student View | Low | Read-only; nice-to-have for transparency |

---

## Appendix B: Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-24 | Requirements Analyst | Initial SRS document creation |

---

> **Approval Signatures**  
> _________________________  
> Project Sponsor | Date  
>   
> _________________________  
> Lead Developer | Date  
>   
> _________________________  
> Quality Assurance Manager | Date  

*This document is confidential and intended solely for the Kiestla Educational Institution project team.*
