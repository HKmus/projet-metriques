# Software Requirements Specification
## Kiestla.edu Attendance Management System
### Use-Case Model (RUP/Jacobson Methodology)

---

## 1. Actors

**Actor: Administrator**  
**Brief Description:** A privileged system user responsible for configuring and maintaining the core structural data of the attendance management system. This actor exists to ensure teaching modules, user accounts, and role assignments remain accurate and up-to-date. The Administrator plays a central role in initializing and sustaining the system's operational foundation.

**Actor: Referring Teacher**  
**Brief Description:** A teacher designated as the coordinator or owner of a specific teaching module. This actor exists to manage module-level participation and oversee attendance tracking for their assigned courses. The Referring Teacher plays a dual role: managing enrollment of pre-registered users into their module and performing standard teaching activities such as reporting and consulting absences.

**Actor: Teacher**  
**Brief Description:** An instructional staff member assigned to deliver classes within one or more teaching modules. This actor exists to record real-time attendance observations during instructional sessions. The Teacher plays an operational role in capturing absence events and consulting absence history for students enrolled in their modules.

**Actor: Administrative Staff**  
**Brief Description:** A non-teaching staff member responsible for processing absence justifications and generating institutional reports. This actor exists to ensure absences are formally documented, validated, and available for academic oversight. The Administrative Staff plays a governance role in finalizing absence records and providing aggregated views for decision-making.

> *Note: Students are represented as data entities within the system but do not actively interact with the system per the provided specifications; therefore, they are not modeled as actors.*

---

## 2. Use Cases Overview

**Use Case: Manage Teaching Modules**  
**Brief Description:** Enables the Administrator to create, update, or delete teaching modules and assign referring teachers to them. This use case provides the foundational structure for organizing attendance tracking by course, benefiting the Administrator by ensuring modules are correctly configured before academic activities begin.

**Use Case: Manage User Registry**  
**Brief Description:** Allows the Administrator to register, update, or deactivate teacher and student records in the global database. This use case ensures all potential participants are available for module enrollment, benefiting the Administrator by maintaining a single source of truth for user identities.

**Use Case: Enroll Participants in Module**  
**Brief Description:** Permits the Referring Teacher to add pre-registered teachers or students to a specific teaching module they coordinate. This use case streamlines class roster management, benefiting the Referring Teacher by enabling quick setup of module participants without requiring Administrator intervention for each change.

**Use Case: Report Student Absence**  
**Brief Description:** Enables a Teacher or Referring Teacher to record that a student was absent from a scheduled session of a module, optionally adding contextual comments. This use case captures attendance events at the point of observation, benefiting teaching staff by providing a simple, immediate mechanism to flag absences for later justification.

**Use Case: Consult Absences by Module**  
**Brief Description:** Allows a Teacher or Referring Teacher to view a filtered list of all recorded absences for students enrolled in a module they teach. This use case supports instructional oversight, benefiting teaching staff by providing visibility into attendance patterns within their specific courses.

**Use Case: Justify Student Absence**  
**Brief Description:** Enables Administrative Staff to enter an official reason or justification for a previously reported student absence. This use case formalizes the absence review process, benefiting Administrative Staff by allowing them to update absence records with validated explanations.

**Use Case: Consult and Filter Absence Records**  
**Brief Description:** Permits Administrative Staff to access all student absence records across the institution and group them by module, student, or justification status. This use case supports administrative reporting and analysis, benefiting Administrative Staff by providing flexible views for monitoring attendance compliance.

**Use Case: View Excessive Unjustified Absences Alert**  
**Brief Description:** Provides Teachers and Referring Teachers with a dedicated view highlighting students who have accumulated more than three unjustified absences across their modules. This use case enables early intervention, benefiting teaching staff by drawing attention to at-risk students requiring follow-up.

---

## 3. Detailed Use-Case Descriptions

### Use Case: Manage Teaching Modules
**Primary Actor:** Administrator  
**Goal:** To create, update, or delete teaching modules and associate them with referring teachers, ensuring the system's course structure reflects institutional offerings.  
**Preconditions:**  
- The Administrator is authenticated and authorized with administrative privileges.  
- The system is operational and accessible.  
**Postconditions:**  
- Teaching module records are created, modified, or removed as requested.  
- Associations between modules and referring teachers are updated in the system.  
- All changes are persisted and immediately available to other actors.  

**Flow of Events:**  
*Basic Flow:*  
1. The Administrator navigates to the module management interface.  
2. The system displays a list of existing teaching modules with options to create, edit, or delete.  
3. The Administrator selects an action (create, update, or delete).  
   a. *If Create:*  
      i. The Administrator enters module details (name, code, schedule, etc.).  
      ii. The Administrator selects one or more referring teachers from the registered user pool.  
      iii. The Administrator confirms the creation.  
   b. *If Update:*  
      i. The Administrator selects a module to modify.  
      ii. The system displays current module details.  
      iii. The Administrator edits desired fields and/or referring teacher assignments.  
      iv. The Administrator confirms the updates.  
   c. *If Delete:*  
      i. The Administrator selects a module to remove.  
      ii. The system displays a confirmation prompt warning of associated data impacts.  
      iii. The Administrator confirms deletion.  
4. The system validates the input data for completeness and consistency.  
5. The system persists the changes to the database.  
6. The system displays a success confirmation and refreshes the module list.  

*Alternative Flows:*  
A1: Cancel Operation (from Step 3)  
- The Administrator selects "Cancel" at any point during data entry.  
- The system discards unsaved changes and returns to the module list view.  

A2: Search/Filter Modules (from Step 2)  
- The Administrator enters search criteria (e.g., module code, teacher name).  
- The system filters and displays matching modules.  
- The Administrator proceeds with management actions on filtered results.  

*Exception Flows:*  
E1: Duplicate Module Identifier (from Step 4)  
- The system detects that the proposed module code already exists.  
- The system displays an error message indicating the conflict.  
- The system returns to the data entry step, preserving other entered values.  

E2: Invalid Referring Teacher Selection (from Step 4)  
- The system detects that a selected referring teacher is not active or lacks required credentials.  
- The system highlights the invalid selection and displays a descriptive error.  
- The system prompts the Administrator to correct the selection before proceeding.  

E3: Deletion with Active Dependencies (from Step 3.c.iii)  
- The system detects that the module to be deleted has active enrollments or recorded absences.  
- The system blocks deletion and displays a warning with dependency details.  
- The system returns to the module list without making changes.  

---

### Use Case: Manage User Registry
**Primary Actor:** Administrator  
**Goal:** To register, update, or deactivate teacher and student records in the global database, ensuring all potential system users have accurate, current profiles.  
**Preconditions:**  
- The Administrator is authenticated with administrative privileges.  
- The system is operational.  
**Postconditions:**  
- User records are created, modified, or deactivated as requested.  
- Updated user information is immediately available for enrollment and reporting functions.  

**Flow of Events:**  
*Basic Flow:*  
1. The Administrator accesses the user registry management interface.  
2. The system displays a searchable list of registered users with role filters (Teacher/Student).  
3. The Administrator selects an action: Register New User, Update Existing User, or Deactivate User.  
   a. *If Register New User:*  
      i. The Administrator specifies user role (Teacher or Student).  
      ii. The Administrator enters required personal and institutional details (name, ID, email, etc.).  
      iii. The Administrator confirms registration.  
   b. *If Update Existing User:*  
      i. The Administrator searches for and selects a user record.  
      ii. The system displays the user's current profile.  
      iii. The Administrator edits permissible fields and confirms updates.  
   c. *If Deactivate User:*  
      i. The Administrator selects a user to deactivate.  
      ii. The system displays a confirmation prompt explaining impact on active enrollments.  
      iii. The Administrator confirms deactivation.  
4. The system validates input data for format, uniqueness, and completeness.  
5. The system persists changes to the user database.  
6. The system confirms the operation and refreshes the user list.  

*Alternative Flows:*  
A1: Bulk User Import (from Step 3)  
- The Administrator chooses to import multiple users via a structured file.  
- The system guides the Administrator through file upload and field mapping.  
- The system processes the import, reporting successes and errors per record.  

A2: Search Users (from Step 2)  
- The Administrator enters search terms (name, ID, email).  
- The system filters and displays matching user records.  
- The Administrator proceeds with actions on the filtered subset.  

*Exception Flows:*  
E1: Duplicate User Identifier (from Step 4)  
- The system detects that the provided institutional ID or email already exists.  
- The system displays an error message and highlights the conflicting field.  
- The system returns to data entry, allowing correction.  

E2: Invalid Data Format (from Step 4)  
- The system detects that entered data violates format rules (e.g., invalid email, missing required field).  
- The system displays field-specific error messages.  
- The system preserves valid entries and prompts for corrections.  

E3: Deactivation with Active Module Assignments (from Step 3.c.iii)  
- The system detects that the user to deactivate is currently assigned as a referring teacher or enrolled in active modules.  
- The system blocks deactivation and displays dependencies requiring resolution first.  
- The system returns to the user list without changes.  

---

### Use Case: Enroll Participants in Module
**Primary Actor:** Referring Teacher  
**Goal:** To add pre-registered teachers or students to a specific teaching module the actor coordinates, establishing the participant roster for attendance tracking.  
**Preconditions:**  
- The Referring Teacher is authenticated and authorized as the referring teacher for the target module.  
- The target module exists and is active.  
- Teachers and students to be enrolled are already registered in the global user database.  
**Postconditions:**  
- Selected users are added to the module's participant list with appropriate roles.  
- Enrolled participants become visible in absence reporting and consultation functions for that module.  

**Flow of Events:**  
*Basic Flow:*  
1. The Referring Teacher navigates to the module management dashboard and selects a module they coordinate.  
2. The system displays the module details and a "Manage Participants" option.  
3. The Referring Teacher selects "Add Participants".  
4. The system presents a searchable interface of registered users not yet enrolled in the module, filterable by role (Teacher/Student).  
5. The Referring Teacher searches for and selects one or more users to enroll.  
6. The Referring Teacher confirms the enrollment selection.  
7. The system validates that selected users are active and eligible for enrollment.  
8. The system adds the users to the module's participant roster.  
9. The system confirms successful enrollment and updates the participant list display.  

*Alternative Flows:*  
A1: Remove Participant (from Step 2)  
- The Referring Teacher selects an enrolled participant to remove.  
- The system prompts for confirmation.  
- Upon confirmation, the system removes the user from the module roster and updates the display.  

A2: Bulk Enrollment via Search Results (from Step 5)  
- The Referring Teacher applies filters (e.g., program, year) to narrow the user list.  
- The system displays matching users.  
- The Referring Teacher selects "Enroll All Filtered Results" and confirms.  
- The system enrolls all matching eligible users.  

*Exception Flows:*  
E1: User Already Enrolled (from Step 7)  
- The system detects that a selected user is already enrolled in the module.  
- The system skips that user, displays a non-blocking notice, and proceeds with other selections.  

E2: Inactive User Selected (from Step 7)  
- The system detects that a selected user account is deactivated.  
- The system excludes the inactive user, displays an error notice, and prompts for alternative selection.  

---

### Use Case: Report Student Absence
**Primary Actor:** Teacher (also applicable to Referring Teacher)  
**Goal:** To record that a student was absent from a scheduled session of a module, optionally providing contextual comments, initiating the absence tracking workflow.  
**Preconditions:**  
- The Teacher is authenticated and assigned to teach the target module.  
- The student is enrolled in the module.  
- The absence corresponds to a valid scheduled session date.  
**Postconditions:**  
- A new absence record is created for the student in the specified module and session.  
- The absence is initially marked as "unjustified" pending administrative review.  
- The record is immediately available for consultation by authorized actors.  

**Flow of Events:**  
*Basic Flow:*  
1. The Teacher accesses the absence reporting interface for a specific module.  
2. The system displays the list of enrolled students for the selected session date.  
3. The Teacher selects one or more students who were absent.  
4. The Teacher optionally enters a comment providing context for the absence (e.g., "no notification received").  
5. The Teacher submits the absence report.  
6. The system validates that the session date is valid and students are enrolled.  
7. The system creates absence records with status "unjustified" and attaches any comments.  
8. The system confirms successful reporting and updates the absence log.  

*Alternative Flows:*  
A1: Report Absence for Different Session Date (from Step 1)  
- The Teacher selects a different session date from a calendar view.  
- The system refreshes the student list for the new date.  
- The Teacher proceeds with selection and submission.  

A2: Add Comment After Initial Submission (from Step 8)  
- Within a configurable time window, the Teacher selects a previously reported absence.  
- The system allows appending an additional comment.  
- The system updates the record and logs the amendment.  

*Exception Flows:*  
E1: Invalid Session Date (from Step 6)  
- The system detects that the selected date does not correspond to a scheduled session for the module.  
- The system displays an error message and prompts the Teacher to select a valid date.  
- The system preserves other entered data.  

E2: Student Not Enrolled in Module (from Step 6)  
- The system detects that a selected student is not officially enrolled in the module for the given session.  
- The system excludes that student from the report, displays a warning, and proceeds with valid selections.  

---

### Use Case: Consult Absences by Module
**Primary Actor:** Teacher (also applicable to Referring Teacher)  
**Goal:** To view a filtered list of all recorded absences for students enrolled in a module the actor teaches, supporting instructional oversight and follow-up.  
**Preconditions:**  
- The Teacher is authenticated and assigned to at least one teaching module.  
- Absence records exist for the selected module.  
**Postconditions:**  
- The system displays absence records matching the Teacher's selection criteria.  
- No data modifications occur; the use case is read-only.  

**Flow of Events:**  
*Basic Flow:*  
1. The Teacher navigates to the absence consultation interface.  
2. The system displays a list of modules the Teacher is assigned to.  
3. The Teacher selects a module to consult.  
4. The system retrieves and displays all absence records for students enrolled in that module, showing student name, date, status (justified/unjustified), and any comments.  
5. The Teacher may optionally filter the list by absence status (justified/unjustified) or date range.  
6. The system refreshes the display to reflect applied filters.  

*Alternative Flows:*  
A1: Export Absence List (from Step 4 or 6)  
- The Teacher selects an export option (e.g., CSV, PDF).  
- The system generates a file containing the currently displayed absence records.  
- The system provides a download link to the Teacher.  

A2: View Student Detail (from Step 4)  
- The Teacher selects a specific absence record or student name.  
- The system displays a detailed view including all absences for that student in the module and justification history.  

*Exception Flows:*  
E1: No Absences Found (from Step 4)  
- The system finds no absence records matching the selected module and filters.  
- The system displays a clear "No records found" message with guidance to adjust filters.  

---

### Use Case: Justify Student Absence
**Primary Actor:** Administrative Staff  
**Goal:** To enter an official reason or justification for a previously reported student absence, updating its status from "unjustified" to "justified" with documented rationale.  
**Preconditions:**  
- Administrative Staff is authenticated and authorized.  
- The absence record exists and is currently marked as "unjustified".  
**Postconditions:**  
- The absence record is updated with a justification reason and status changed to "justified".  
- The updated record is immediately reflected in all consultation and reporting views.  

**Flow of Events:**  
*Basic Flow:*  
1. Administrative Staff accesses the absence justification interface.  
2. The system displays a list of unjustified absences, filterable by module, student, or date.  
3. Administrative Staff searches for and selects a specific absence record to justify.  
4. The system displays the absence details (student, module, date, teacher comments).  
5. Administrative Staff selects a justification reason from a predefined list or enters a custom reason.  
6. Administrative Staff confirms the justification.  
7. The system validates that the reason is provided and the record is still unjustified.  
8. The system updates the absence record: sets status to "justified", records the reason, and logs the action.  
9. The system confirms the update and refreshes the unjustified absences list.  

*Alternative Flows:*  
A1: Bulk Justification (from Step 3)  
- Administrative Staff selects multiple unjustified absences sharing a common reason.  
- The system prompts for a single justification reason to apply to all.  
- Upon confirmation, the system updates all selected records atomically.  

A2: Attach Supporting Document (from Step 5)  
- Administrative Staff uploads a supporting document (e.g., medical certificate).  
- The system attaches the document reference to the absence record.  
- The workflow proceeds to confirmation.  

*Exception Flows:*  
E1: Absence Already Justified (from Step 7)  
- The system detects that the selected absence was justified by another staff member concurrently.  
- The system displays a notification and refreshes the list to reflect current status.  
- The workflow terminates without changes.  

E2: Invalid Justification Reason (from Step 7)  
- The system detects that a custom reason exceeds length limits or contains prohibited content.  
- The system displays a field-specific error and prompts for correction.  

---

### Use Case: Consult and Filter Absence Records
**Primary Actor:** Administrative Staff  
**Goal:** To access and dynamically filter all student absence records across the institution, enabling comprehensive monitoring, reporting, and analysis of attendance compliance.  
**Preconditions:**  
- Administrative Staff is authenticated and authorized.  
- Absence records exist in the system.  
**Postconditions:**  
- The system displays absence records matching the applied filters.  
- No data modifications occur; the use case is read-only.  

**Flow of Events:**  
*Basic Flow:*  
1. Administrative Staff navigates to the comprehensive absence consultation interface.  
2. The system displays a default view of recent absence records with key attributes.  
3. Administrative Staff applies one or more filters: by module, by student, by justification status, by date range, or by referring teacher.  
4. The system queries the database and refreshes the display to show matching records.  
5. Administrative Staff may sort results by any column (e.g., student name, date, status).  
6. The system updates the display order accordingly.  

*Alternative Flows:*  
A1: Group Results by Module or Student (from Step 4)  
- Administrative Staff selects a grouping option (Group by Module / Group by Student).  
- The system reorganizes the display into collapsible sections per group.  
- Administrative Staff can expand/collapse groups for detailed inspection.  

A2: Export Filtered Results (from Step 4 or 6)  
- Administrative Staff selects an export format.  
- The system generates a report file containing the currently filtered and sorted records.  
- The system provides a download link.  

*Exception Flows:*  
E1: Overly Broad Query (from Step 4)  
- The system detects that the filter combination would return an excessively large result set.  
- The system prompts Administrative Staff to narrow filters or confirms intent to proceed.  
- If confirmed, the system paginates results to ensure performance.  

---

### Use Case: View Excessive Unjustified Absences Alert
**Primary Actor:** Teacher, Referring Teacher  
**Goal:** To consult a dedicated view highlighting students who have accumulated more than three unjustified absences across modules the actor teaches, enabling timely academic intervention.  
**Preconditions:**  
- The Teacher/Referring Teacher is authenticated.  
- The actor is assigned to at least one teaching module.  
- Absence records exist and have been processed for justification status.  
**Postconditions:**  
- The system displays a filtered list of at-risk students meeting the threshold criterion.  
- No data modifications occur; the use case is read-only.  

**Flow of Events:**  
*Basic Flow:*  
1. The Teacher/Referring Teacher navigates to the "Attendance Alerts" section.  
2. The system calculates, for each student enrolled in the actor's modules, the count of unjustified absences.  
3. The system filters and displays only students with a count greater than three.  
4. For each listed student, the system shows: name, module(s), count of unjustified absences, and most recent absence date.  
5. The actor may select a student to view detailed absence history and justification status per module.  

*Alternative Flows:*  
A1: Adjust Alert Threshold (if configurable) (from Step 3)  
- The system allows the actor to temporarily adjust the threshold (e.g., view students with >2 unjustified absences).  
- The system recalculates and refreshes the list based on the new threshold.  
- The default threshold (3) is restored upon session end or explicit reset.  

A2: Export Alert List (from Step 4)  
- The actor selects an export option.  
- The system generates a file containing the displayed alert list with student details and absence counts.  
- The system provides a download link.  

*Exception Flows:*  
E1: No Students Meet Threshold (from Step 3)  
- The system finds no students with more than three unjustified absences in the actor's modules.  
- The system displays a clear confirmation message: "No students currently exceed the unjustified absence threshold."  

---

## 4. Subflows
*No reusable subflows are required for this model. All flows are sufficiently modular and context-specific to remain within their parent use cases without loss of clarity or maintainability.*

---

## 5. Model Completeness Statement
This use-case model fully captures all functional requirements specified for the Kiestla.edu Attendance Management System. Each actor's interactions are explicitly defined, all system behaviors are described through structured flows, and exception handling ensures robustness. The model adheres to RUP/Jacobson methodology principles: actor-goal orientation, clear pre/postconditions, and separation of basic, alternative, and exception flows. No ambiguities remain regarding system scope, actor responsibilities, or expected behaviors.
