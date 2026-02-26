# Software Requirements Specification (SRS)
## Student Attendance Control System – www.kiestla.edu

---

## 1. Actors

| Actor | Brief Description |
|-------|-------------------|
| **Administrator** | A member of the IT or academic administration responsible for the overall configuration of the system. Creates, maintains, and deletes teaching modules, assigns referring teachers to modules, and manages the global database of teachers and students. |
| **Teacher** | A lecturer or instructor who teaches one or more modules. Can report absences with optional comments, consult absence lists for modules they teach, and (if designated as referring teacher for a module) add other teachers or students to that module. Also may view the alert page for students with excessive unjustified absences. |
| **Administrative Staff** | A member of the administration office who handles absence justifications. Enters the official reason for each absence, has full read access to all student absences (with grouping by module and by student), and is alerted to students having more than three unjustified absences. |

> **Note:** Students are not direct actors; they are represented as data entities. The system does not require student login interaction.

---

## 2. Use Cases (Overview)

| Use Case | Brief Description | Primary Actor(s) |
|---------|-------------------|------------------|
| UC-01: Manage Teaching Modules | Administrator creates, modifies, or deletes a teaching module. | Administrator |
| UC-02: Manage User Database | Administrator adds, updates, or removes teachers and students in the global database. | Administrator |
| UC-03: Assign Referring Teacher to Module | Administrator designates one or more teachers as referring teachers for a specific module. | Administrator |
| UC-04: Add Teacher to Module | A referring teacher adds an existing teacher to the teaching staff of the module. | Teacher (with referring privileges) |
| UC-05: Add Student to Module | A referring teacher adds an existing student to the enrolment list of the module. | Teacher (with referring privileges) |
| UC-06: Report Absence | A teacher records an absence for a student in one of their modules, optionally adding a comment. | Teacher |
| UC-07: Consult Module Absences | A teacher views the list of absences for all students enrolled in a specific module they teach. | Teacher |
| UC-08: Enter Absence Reason | Administrative staff assigns an official reason (e.g., medical, family) to an existing absence record. | Administrative Staff |
| UC-09: View All Absences | Administrative staff accesses the complete absence repository, with filters to group by module or by student. | Administrative Staff |
| UC-10: View Excessive Unjustified Absences Alert | System provides a page listing students who have accumulated more than three unjustified absences. Accessible by teaching staff (teachers and administrative staff). | Teacher, Administrative Staff |

---

## 3. Full Use‑Case Descriptions

---

### UC-01: Manage Teaching Modules

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Manage Teaching Modules |
| **Primary Actor** | Administrator |
| **Goal** | Create, modify, or delete a teaching module in the system. |
| **Preconditions** | Administrator is authenticated and authorized. |
| **Postconditions** | The teaching module is created, updated, or removed accordingly; the change is persisted in the system. |

**Flow of Events**

**Basic Flow – Create a new module**
1. The actor selects “Create new module”.
2. The system presents a form to enter module code, title, description, and academic period.
3. The actor fills in the required fields and submits the form.
4. The system validates that the module code is unique.
5. The system stores the new module and confirms success.

**Alternative Flows**
- **A1: Modify an existing module** (from Step 1)  
  *The actor chooses “Edit module”, selects a module, updates the information, and submits. The system updates the record.*
- **A2: Delete an existing module** (from Step 1)  
  *The actor chooses “Delete module”, selects a module, confirms deletion. The system removes the module and all its associations (absences, teacher assignments, enrolments are handled according to business rules).*

**Exception Flows**
- **E1: Duplicate module code** (from Step 4)  
  *If the module code already exists, the system displays an error message and returns to the form without saving.*
- **E2: Required fields missing** (from Step 4)  
  *If mandatory fields (code, title) are empty, the system highlights the missing fields and does not save.*

---

### UC-02: Manage User Database

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Manage User Database |
| **Primary Actor** | Administrator |
| **Goal** | Add, update, or delete teacher/student records in the global user database. |
| **Preconditions** | Administrator is authenticated and authorized. |
| **Postconditions** | User record is created, updated, or removed. |

**Flow of Events**

**Basic Flow – Add a new user**
1. The actor selects “Add user”.
2. The system asks for user type (Teacher / Student).
3. The actor chooses a type and fills in personal details (ID, name, email, etc.).
4. The actor submits the form.
5. The system validates that the user ID is unique.
6. The system stores the user record and confirms success.

**Alternative Flows**
- **A1: Update user** (from Step 1)  
  *Actor searches for an existing user, modifies the data, and submits. System updates.*
- **A2: Delete user** (from Step 1)  
  *Actor selects a user, confirms deletion. System removes the user; any future assignments are prevented but historical absences remain anonymised or flagged as “deleted user”.*

**Exception Flows**
- **E1: Duplicate user ID** (from Step 5)  
  *System rejects and prompts to use a different identifier.*
- **E2: Invalid email format** (from Step 5)  
  *System rejects submission and indicates the error.*

---

### UC-03: Assign Referring Teacher to Module

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Assign Referring Teacher to Module |
| **Primary Actor** | Administrator |
| **Goal** | Designate one or more teachers as referring teachers for a specific module. |
| **Preconditions** | The module and the teachers exist in the system. |
| **Postconditions** | The selected teachers are marked as referring teachers for the module. |

**Flow of Events**

**Basic Flow**
1. The actor selects a module from the module list.
2. The system displays the module details and current referring teachers.
3. The actor clicks “Assign referring teacher”.
4. The system shows a list of available teachers (not already assigned as referring).
5. The actor selects one or more teachers and confirms.
6. The system adds the teacher(s) to the module’s referring teacher list.
7. The system confirms the assignment.

**Alternative Flows**
- **A1: Remove referring teacher** (from Step 3)  
  *Actor selects “Remove referring teacher”, chooses a teacher from the current list, and confirms removal.*

**Exception Flows**
- **E1: No teachers available** (from Step 4)  
  *If no unassigned teachers exist, the system informs the actor and suggests creating a teacher first.*

---

### UC-04: Add Teacher to Module

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Add Teacher to Module |
| **Primary Actor** | Teacher (acting as referring teacher for the module) |
| **Goal** | Add an existing teacher to the teaching staff of a module. |
| **Preconditions** | The actor is authenticated and is a referring teacher for the selected module. The teacher to be added exists in the global database. |
| **Postconditions** | The teacher is associated with the module and can now report absences for it. |

**Flow of Events**

**Basic Flow**
1. The actor selects the module from their list of referred modules.
2. The system displays the module dashboard.
3. The actor chooses “Add teacher to module”.
4. The system presents a search field to find a teacher by name or ID.
5. The actor enters search criteria and selects the correct teacher from the results.
6. The system adds the teacher to the module’s teaching staff.
7. The system confirms the addition.

**Alternative Flows**
- **A1: Cancel addition** (at any step)  
  *Actor aborts the operation; no changes are made.*

**Exception Flows**
- **E1: Teacher not found** (from Step 5)  
  *If the search returns no results, the system notifies the actor and offers to refine the search.*
- **E2: Teacher already assigned** (from Step 6)  
  *If the selected teacher is already part of the module, the system informs the actor and does not duplicate the assignment.*

---

### UC-05: Add Student to Module

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Add Student to Module |
| **Primary Actor** | Teacher (acting as referring teacher for the module) |
| **Goal** | Enrol an existing student into a module. |
| **Preconditions** | Actor is referring teacher for the module; student exists in global database. |
| **Postconditions** | Student is enrolled in the module and can have absences recorded. |

**Flow of Events**

*(Structure identical to UC-04, with “teacher” replaced by “student”.)*

**Basic Flow**
1. Actor selects module → “Add student to module”.
2. System provides student search.
3. Actor selects student.
4. System enrols student, confirms.

**Exception Flows**
- **E1: Student not found** – similar to UC-04 E1.
- **E2: Student already enrolled** – system rejects duplicate enrolment.

---

### UC-06: Report Absence

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Report Absence |
| **Primary Actor** | Teacher |
| **Goal** | Record an absence for a student in one of the teacher’s modules, optionally with a comment. |
| **Preconditions** | Teacher is authenticated and assigned to the module. Student is enrolled in the module. |
| **Postconditions** | An absence record is created with status “unjustified”, date, module, student, reporting teacher, and optional comment. |

**Flow of Events**

**Basic Flow**
1. The actor selects the module from their teaching dashboard.
2. The system displays the list of enrolled students for that module.
3. The actor identifies the absent student (e.g., by checking a checkbox next to the student’s name).
4. The actor optionally enters a comment in a text field.
5. The actor clicks “Record absence”.
6. The system creates an absence record with current date, the selected student, the module, the teacher, the comment, and default status “unjustified”.
7. The system confirms the recording.

**Alternative Flows**
- **A1: Bulk absence reporting** (from Step 3)  
  *Actor selects multiple students at once, enters a common comment (optional), and records all absences in one action. System creates individual records for each selected student.*

**Exception Flows**
- **E1: No student selected** (from Step 5)  
  *System displays error: “At least one student must be selected.”*
- **E2: Duplicate absence on same day** (from Step 6)  
  *If an absence record already exists for the same student, module, and date, the system warns the actor and does not create a duplicate unless overridden (business decision: allow multiple? Typically no). We assume prevention.*

---

### UC-07: Consult Module Absences

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Consult Module Absences |
| **Primary Actor** | Teacher |
| **Goal** | View a list of absences for all students enrolled in a specific module. |
| **Preconditions** | Teacher is authenticated and assigned to the module. |
| **Postconditions** | System displays the absence records of the module. |

**Flow of Events**

**Basic Flow**
1. The actor selects a module from their teaching dashboard.
2. The system displays a summary of the module, including a tab or section “Absences”.
3. The actor clicks “View absences”.
4. The system retrieves all absence records for the module, ordered by date (most recent first).
5. The system shows a table with columns: Student name, Date, Comment, Status (justified/unjustified), Reason (if entered).
6. The actor may optionally filter by date range or student name.

**Alternative Flows**
- **A1: Export list** (from Step 5)  
  *Actor clicks “Export” and downloads the absence list in CSV/PDF format.*

**Exception Flows**
- **E1: No absences** (from Step 5)  
  *System displays a message “No absences recorded for this module.”*

---

### UC-08: Enter Absence Reason

| Attribute | Value |
|----------|-------|
| **Use Case Name** | Enter Absence Reason |
| **Primary Actor** | Administrative Staff |
| **Goal** | Assign an official justification reason to an existing unjustified absence, thereby marking it as justified. |
| **Preconditions** | Absence record exists with status “unjustified”. Actor is authenticated as administrative staff. |
| **Postconditions** | The absence record is updated with a reason and its status becomes “justified”. |

**Flow of Events**

**Basic Flow**
1. The actor searches for an absence (by student, module, or date) using UC-09 functionality or accesses the alert page (UC-10).
2. The system displays a list of absences.
3. The actor selects a specific absence record.
4. The system shows the absence details, including a field to enter a reason.
5. The actor chooses a reason from a predefined list (e.g., medical, family, administrative) or enters free text.
6. The actor saves the justification.
7. The system changes the status to “justified”, stores the reason and the staff member who entered it, and confirms success.

**Alternative Flows**
- **A1: Bulk justification** (from Step 3)  
  *Actor selects multiple unjustified absences (e.g., all absences of one student on different dates) and assigns the same reason in one action.*

**Exception Flows**
- **E1: Absence already justified** (from Step 3)  
  *System warns that the absence is already justified; the actor may choose to override/change the reason.*
- **E2: Reason field left blank** (from Step 6)  
  *System rejects and prompts to enter a reason.*

---

### UC-09: View All Absences

| Attribute | Value |
|----------|-------|
| **Use Case Name** | View All Absences |
| **Primary Actor** | Administrative Staff |
| **Goal** | Access the complete absence repository with grouping capabilities (by module, by student). |
| **Preconditions** | Actor is authenticated as administrative staff. |
| **Postconditions** | System displays the requested absence view. |

**Flow of Events**

**Basic Flow – Group by Module**
1. The actor selects “Absence overview” from the main menu.
2. The system presents two grouping options: “By module” and “By student”.
3. The actor chooses “By module”.
4. The system displays a list of modules; for each module, the total number of absences, and optionally a link to view detailed absences (similar to UC-07 but with all modules).
5. The actor can drill down into a module to see the absence list.

**Alternative Flows**
- **A1: Group by student** (from Step 3)  
  *Actor selects “By student”. System shows a list of students, each with total absences and a breakdown by module.*
- **A2: Filter by date/status** (at any view)  
  *Actor applies filters to narrow the list.*

**Exception Flows**
- **E1: No data** – System displays “No absences recorded in the system.”

---

### UC-10: View Excessive Unjustified Absences Alert

| Attribute | Value |
|----------|-------|
| **Use Case Name** | View Excessive Unjustified Absences Alert |
| **Primary Actor** | Teacher, Administrative Staff |
| **Goal** | Obtain a list of students who currently have more than three unjustified absences (across any module). |
| **Preconditions** | Actor is authenticated and has teaching staff privileges (teacher or admin staff). |
| **Postconditions** | System displays the alert list. |

**Flow of Events**

**Basic Flow**
1. The actor navigates to the “Alerts” or “At-risk students” page.
2. The system computes, for each student, the count of absence records with status = “unjustified”.
3. The system filters those students with a count > 3.
4. The system displays the list, including student name, number of unjustified absences, and links to view the detailed absences.
5. The actor can click on a student to see the individual absences (UC-09/UC-07 style).

**Alternative Flows**
- **A1: No students exceed threshold** (from Step 4)  
  *System displays “No students with excessive unjustified absences at this time.”*

**Exception Flows**
- None specific.

---

## 4. Subflows (Reusable)

No explicit subflows were factored out to keep the descriptions self-contained. However, common behavior (e.g., searching for a user) can be considered a subflow but is described inline for brevity and clarity.

---

**End of Software Requirements Specification**
