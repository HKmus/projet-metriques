Absolutely, Mustapha — this is a clean and classic **attendance management portal**, perfect for a full **RUP / Jacobson-style Use-Case Requirements Specification**.

Below is a complete Software Requirements Specification written **strictly using the Use-Case Modeling methodology** (Actors → Use Cases → Full Use-Case Descriptions with flows).

---

# Software Requirements Specification (SRS)

## Use-Case Model Based Requirements (Jacobson / RUP)

---

## 1. Identified Actors

---

### Actor: Administrator

**Brief Description:**
The Administrator is responsible for managing the academic structure of the system. This actor maintains the global database of modules, teachers, and students and ensures that the portal remains consistent and up to date.

---

### Actor: Referring Teacher

**Brief Description:**
A Referring Teacher is a teacher assigned responsibility over one or more teaching modules. This actor manages student enrollment in modules and records absences during class sessions.

---

### Actor: Teacher

**Brief Description:**
A Teacher participates in module teaching activities and may consult student absence information. Teachers interact with the system mainly for attendance monitoring and alerts.

---

### Actor: Student

**Brief Description:**
A Student is enrolled in teaching modules and is the subject of attendance tracking. Students may consult their absence records and justification status.

---

### Actor: Administrative Staff

**Brief Description:**
Administrative Staff members validate and justify absences. They enter reasons for absences and monitor absence statistics across modules and students.

---

## 2. Main Identified Use Cases

---

### Use Case: Manage Teaching Modules

**Brief Description:**
This use case allows the Administrator to create, update, delete, and associate teaching modules with referring teachers, ensuring the academic structure is maintained.

---

### Use Case: Manage Global User Database

**Brief Description:**
This use case allows the Administrator to maintain the master list of teachers and students who may participate in modules.

---

### Use Case: Assign Teachers and Students to Module

**Brief Description:**
This use case enables the Referring Teacher to add already-registered teachers and students into their module roster.

---

### Use Case: Record Student Absence

**Brief Description:**
This use case allows a Teacher to report a student absence during a class session, optionally including a comment.

---

### Use Case: Consult Absence List by Module

**Brief Description:**
This use case allows Teachers to view absences of all students enrolled in their teaching modules.

---

### Use Case: Enter Absence Justification

**Brief Description:**
This use case allows Administrative Staff to record the official reason for a student absence and mark it as justified or unjustified.

---

### Use Case: Consult Absence Records by Student

**Brief Description:**
This use case allows Administrative Staff to access all absences related to a particular student.

---

### Use Case: Generate Absence Alerts

**Brief Description:**
This use case automatically alerts teaching staff when a student exceeds three unjustified absences.

---

## 3. Full Use-Case Descriptions

---

# Use Case 1: Manage Teaching Modules

### Primary Actor

Administrator

### Goal

To maintain the list of teaching modules and associate each module with one or more referring teachers.

### Preconditions

* The Administrator is authenticated in the system.
* The global teacher database contains valid teacher accounts.

### Postconditions

* A module is created, updated, or deleted successfully.
* Module-teacher associations are stored in the system.

---

## Flow of Events

### Basic Flow (Happy Path)

1. The Administrator initiates module management.
2. The system displays the list of existing modules.
3. The Administrator selects **Create Module**.
4. The system requests module information (name, code, assigned teacher).
5. The Administrator enters module details.
6. The system validates the information.
7. The system records the new module and its teacher association.
8. The system confirms successful creation.

---

### Alternative Flows

**A1: Update Module (from Step 3)**

1. The Administrator selects an existing module instead of creating a new one.
2. The system displays current module information.
3. The Administrator edits the information.
4. The system saves the updated module.

---

**A2: Delete Module (from Step 3)**

1. The Administrator selects **Delete Module**.
2. The system asks for confirmation.
3. The Administrator confirms deletion.
4. The system removes the module.

---

### Exception Flows

**E1: Invalid Module Data (from Step 6)**

1. The system detects missing or incorrect information.
2. The system displays an error message.
3. The Administrator re-enters valid data.

---

---

# Use Case 2: Manage Global User Database

### Primary Actor

Administrator

### Goal

To manage the master list of teachers and students available in the system.

### Preconditions

* Administrator is authenticated.

### Postconditions

* New users are added, updated, or removed from the database.

---

## Flow of Events

### Basic Flow

1. The Administrator opens the user management section.
2. The system displays registered teachers and students.
3. The Administrator selects **Add User**.
4. The system requests user information.
5. The Administrator provides the details.
6. The system validates and stores the new user.
7. The system confirms registration.

---

### Alternative Flows

**A1: Remove User (from Step 3)**

1. The Administrator selects a user and chooses **Delete**.
2. The system removes the user from the database.

---

### Exception Flows

**E1: User Already Exists (from Step 6)**

1. The system detects duplicate registration.
2. The system rejects the entry and informs the Administrator.

---

---

# Use Case 3: Assign Teachers and Students to Module

### Primary Actor

Referring Teacher

### Goal

To enroll teachers and students into a module roster.

### Preconditions

* The module exists.
* Teachers/students are already registered globally.

### Postconditions

* Selected users become enrolled in the module.

---

## Flow of Events

### Basic Flow

1. The Referring Teacher selects one of their modules.
2. The system displays module roster management options.
3. The actor chooses **Add Student/Teacher**.
4. The system displays the global database list.
5. The actor selects users to add.
6. The system records the module enrollment.
7. The system confirms assignment.

---

### Exception Flows

**E1: User Not Found (from Step 4)**

1. The system cannot locate the selected user.
2. The system informs the teacher that the user must be registered first.

---

---

# Use Case 4: Record Student Absence

### Primary Actor

Teacher

### Goal

To report a student absence during a module session.

### Preconditions

* Teacher is assigned to the module.
* Student is enrolled in the module.

### Postconditions

* Absence is recorded with optional comment.
* Absence status is initially unjustified.

---

## Flow of Events

### Basic Flow

1. The Teacher initiates attendance recording for a module session.
2. The system displays enrolled students.
3. The Teacher selects a student marked absent.
4. The system requests optional comments.
5. The Teacher enters a comment.
6. The system records the absence.
7. The system confirms successful reporting.

---

### Alternative Flows

**A1: No Comment Provided (from Step 4)**

1. The Teacher skips comment entry.
2. The system records the absence without comment.

---

### Exception Flows

**E1: Student Not Enrolled (from Step 3)**

1. The system detects the student is not registered in the module.
2. The system rejects the absence entry.

---

---

# Use Case 5: Consult Absence List by Module

### Primary Actor

Teacher

### Goal

To view absences of students enrolled in one of the teacher’s modules.

### Preconditions

* Teacher is authenticated.
* Teacher is assigned to the module.

### Postconditions

* Absence list is displayed.

---

## Flow of Events

### Basic Flow

1. The Teacher selects **Consult Absences**.
2. The system displays modules taught by the Teacher.
3. The Teacher selects a module.
4. The system displays all absences grouped by student.
5. The Teacher reviews absence details.

---

---

# Use Case 6: Enter Absence Justification

### Primary Actor

Administrative Staff

### Goal

To provide an official reason for an absence and mark it justified or unjustified.

### Preconditions

* Absence record exists.
* Staff member is authenticated.

### Postconditions

* Absence is updated with reason and justification status.

---

## Flow of Events

### Basic Flow

1. Administrative Staff accesses the absence management page.
2. The system displays all recorded absences.
3. The actor selects an absence entry.
4. The system requests a justification reason.
5. The actor enters the reason and selects status.
6. The system updates the absence record.
7. The system confirms the update.

---

### Exception Flows

**E1: Missing Justification Reason (from Step 5)**

1. The system detects empty justification.
2. The system requests completion before saving.

---

---

# Use Case 7: Consult Absence Records by Student

### Primary Actor

Administrative Staff

### Goal

To access all absences belonging to a specific student.

### Preconditions

* Student exists in database.

### Postconditions

* Absence history is displayed.

---

## Flow of Events

### Basic Flow

1. The actor searches for a student.
2. The system displays student profile.
3. The actor selects **View Absence History**.
4. The system displays all absences grouped by module.

---

---

# Use Case 8: Generate Absence Alerts

### Primary Actor

Teacher (Beneficiary)

### Goal

To alert teaching staff when students exceed three unjustified absences.

### Preconditions

* Absence records exist.
* At least one student has more than three unjustified absences.

### Postconditions

* Alert list is displayed.

---

## Flow of Events

### Basic Flow

1. The system automatically checks unjustified absence counts.
2. The system identifies students exceeding the threshold.
3. The system displays an alert page to teaching staff.
4. Teachers consult flagged student records.

---

### Exception Flows

**E1: No Students Exceed Threshold (from Step 2)**

1. The system finds no matching students.
2. The system displays “No alerts at this time.”

---

# End of Requirements Document

