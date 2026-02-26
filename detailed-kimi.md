# Software Requirements Specification (SRS)
## Student Attendance Control System - www.kiestla.edu

---

## 1. ACTORS

**Actor: Administrator**
Brief Description: The Administrator is a privileged user responsible for the overall system configuration and data management. This actor exists to maintain the foundational structure of the academic environment by creating and managing teaching modules, user accounts, and system-wide data integrity. The Administrator plays the central governance role, ensuring that the global database of teachers and students is accurate and that modules are properly associated with referring teachers.

**Actor: Referring Teacher**
Brief Description: The Referring Teacher is a faculty member designated as the primary responsible party for one or more teaching modules. This actor exists to coordinate module-specific academic activities and personnel management within their assigned modules. The Referring Teacher plays a supervisory role by adding registered teachers and students to their modules and overseeing absence-related activities within their domain.

**Actor: Teacher**
Brief Description: The Teacher is a faculty member who delivers instruction in one or more teaching modules and records student attendance. This actor exists to document student presence and absence during class sessions and provide contextual information about absences. The Teacher plays an operational role by reporting absences with optional comments and consulting absence records for students enrolled in their modules.

**Actor: Administrative Staff**
Brief Description: The Administrative Staff member is an administrative employee responsible for processing and justifying student absences. This actor exists to provide formal validation and documentation of absence reasons, ensuring compliance with institutional attendance policies. The Administrative Staff plays a regulatory role by entering justification reasons, accessing comprehensive absence records, and monitoring students with excessive unjustified absences.

**Actor: Student**
Brief Description: The Student is the learner enrolled in teaching modules whose attendance is being tracked. This actor exists as the subject of the attendance management process, though they interact with the system primarily as passive data entities rather than active users. The Student is the beneficiary of the system's core functionality, with their attendance history, justification status, and academic standing being managed through the portal.

---

## 2. USE CASES

**Use Case: UC-001 Manage Teaching Modules**
Brief Description: This use case enables the Administrator to create, modify, and delete teaching modules within the system. It provides the structural foundation for the attendance control process by establishing the academic units where attendance is tracked. The Administrator benefits from this capability to organize the curriculum and prepare modules for teacher assignment.

**Use Case: UC-002 Manage User Accounts**
Brief Description: This use case allows the Administrator to maintain the global database of teachers and students by adding, updating, and removing user records. It ensures that all potential system participants are properly registered before they can be assigned to specific modules. The Administrator benefits from centralized user management, preventing duplicate accounts and maintaining data consistency.

**Use Case: UC-003 Assign Referring Teacher**
Brief Description: This use case enables the Administrator to associate one or more teachers as referring teachers with specific teaching modules. It establishes the hierarchical relationship necessary for module management and delegation of responsibilities. The Administrator and Referring Teachers benefit from clear assignment of authority and accountability.

**Use Case: UC-004 Manage Module Personnel**
Brief Description: This use case allows the Referring Teacher to add registered teachers and students to their assigned modules from the global database. It populates modules with the necessary participants for attendance tracking. The Referring Teacher benefits from the ability to assemble their teaching team and student roster without requiring Administrator intervention for each individual assignment.

**Use Case: UC-005 Report Student Absence**
Brief Description: This use case enables a Teacher to record a student's absence in a module they teach, optionally adding explanatory comments. It captures the initial attendance event that triggers the justification workflow. The Teacher benefits from a streamlined mechanism to document absences, while the Student and Administrative Staff benefit from having a recorded history for subsequent processing.

**Use Case: UC-006 Consult Module Absences**
Brief Description: This use case allows a Teacher to view the list of absences for all students enrolled in any of their modules. It provides visibility into attendance patterns for academic oversight and intervention. The Teacher benefits from comprehensive access to absence data to identify at-risk students and track attendance trends.

**Use Case: UC-007 Justify Student Absence**
Brief Description: This use case enables Administrative Staff to enter the official reason for a student's absence and mark it as justified. It transforms an unverified absence into a formally excused absence within institutional policy. The Administrative Staff benefits from a structured process to apply institutional standards, while Students benefit from proper documentation of legitimate absences.

**Use Case: UC-008 Generate Absence Reports**
Brief Description: This use case allows Administrative Staff to view and group student absences by module or by individual student, providing comprehensive oversight of attendance data. It supports administrative decision-making and policy enforcement. The Administrative Staff benefits from flexible reporting capabilities to analyze attendance patterns across different dimensions.

**Use Case: UC-009 Monitor Unjustified Absence Alerts**
Brief Description: This use case provides an automated alert mechanism that identifies and displays students with more than three unjustified absences to teaching staff. It serves as an early warning system for academic intervention and policy enforcement. Teaching Staff benefit from proactive notification of at-risk students, enabling timely support or disciplinary action.

---

## 3. FULL USE-CASE DESCRIPTIONS

---

### UC-001: Manage Teaching Modules

**Use Case Name:** Manage Teaching Modules  
**Primary Actor:** Administrator  
**Goal:** To create, maintain, and remove teaching modules from the system, and associate them with referring teachers.  
**Preconditions:**
- Administrator is authenticated and logged into the system
- Administrator has administrative privileges  
**Postconditions:**
- Module database is updated (created, modified, or deleted)
- Referring teacher associations are established or updated
- Changes are persisted and visible to authorized users

**Flow of Events:**

**Basic Flow:**
1. The Administrator selects the "Module Management" function from the main menu.
2. The system displays the Module Management interface with options to Create, Edit, or Delete modules.
3. The Administrator selects the desired operation.
4. **IF** Create: The system displays a form requesting module details (code, name, description, credits, schedule).
5. The Administrator enters the required module information and submits.
6. The system validates the input data for completeness and uniqueness.
7. The system creates the new module record and confirms successful creation.
8. **IF** Edit: The system displays a searchable list of existing modules.
9. The Administrator selects a module from the list.
10. The system retrieves and displays the current module details in an editable form.
11. The Administrator modifies the desired fields and submits.
12. The system validates the changes and updates the module record.
13. The system confirms successful modification.
14. **IF** Delete: The system displays a searchable list of existing modules.
15. The Administrator selects a module for deletion.
16. The system checks for existing associations (teachers, students, absence records).
17. The system prompts for confirmation of deletion.
18. The Administrator confirms the deletion.
19. The system removes the module record and all associated enrollments.
20. The system confirms successful deletion.
21. The system returns to the Module Management main interface.

**Alternative Flows:**

A1: Cancel Operation (from Steps 5, 11, or 18)  
At any point before final submission, the Administrator may select "Cancel." The system discards any changes and returns to the Module Management main interface without modifying data.

A2: Associate Referring Teacher During Creation (from Step 7)  
After creating a module, the system prompts: "Assign referring teacher now?" If the Administrator selects "Yes," the system transitions to UC-003 Assign Referring Teacher for the newly created module.

A3: Soft Delete with Preservation (from Step 16)  
If the system detects historical absence records for the module, it offers the option to "Deactivate" rather than delete, preserving historical data while preventing new assignments.

**Exception Flows:**

E1: Validation Failure (from Steps 6 or 12)  
If the system detects invalid data (missing required fields, duplicate module code, invalid format):  
- The system displays specific error messages indicating the validation failures  
- The system highlights the problematic fields  
- The system returns to the form with entered data preserved  
- The Administrator corrects the errors and resubmits

E2: Deletion Constraint Violation (from Step 16)  
If the module has active absence records that cannot be archived:  
- The system displays an error message: "Cannot delete module with active academic records"  
- The system provides options to view associated records or cancel deletion  
- If the Administrator chooses to view records, the system displays a summary  
- The system returns to the module list without deleting

E3: Database Connection Failure (from any submission step)  
If the system cannot connect to the database during save operations:  
- The system displays: "System error: Unable to save changes. Please try again later."  
- The system logs the error for technical support  
- The system preserves the form data in session for retry  
- The Administrator may retry or cancel

---

### UC-002: Manage User Accounts

**Use Case Name:** Manage User Accounts  
**Primary Actor:** Administrator  
**Goal:** To add, update, and remove teacher and student records in the global database.  
**Preconditions:**
- Administrator is authenticated and logged into the system
- Administrator has administrative privileges  
**Postconditions:**
- Global user database is updated
- User records are available for module assignment
- Changes are persisted and immediately effective

**Flow of Events:**

**Basic Flow:**
1. The Administrator selects the "User Management" function from the main menu.
2. The system displays the User Management interface with tabs for "Teachers" and "Students."
3. The Administrator selects the appropriate user type tab.
4. The system displays the selected user type interface with options to Add, Edit, or Delete users.
5. The Administrator selects the desired operation.
6. **IF** Add: The system displays a form requesting user details (ID, name, email, department/program, status).
7. The Administrator enters the required user information and submits.
8. The system validates the input for completeness, format, and uniqueness.
9. The system creates the new user record with a generated temporary password.
10. The system sends a notification email to the new user's address with login credentials.
11. The system confirms successful creation and displays the new user ID.
12. **IF** Edit: The system displays a searchable/filterable list of users.
13. The Administrator searches for and selects a user from the list.
14. The system retrieves and displays the current user details in an editable form (excluding password).
15. The Administrator modifies the desired fields and submits.
16. The system validates the changes and updates the user record.
17. If email was changed, the system sends a notification to the new address.
18. The system confirms successful modification.
19. **IF** Delete: The system displays a searchable/filterable list of users.
20. The Administrator searches for and selects a user for deletion.
21. The system checks for existing module assignments or absence records.
22. The system displays a confirmation dialog with a summary of associated data.
23. The Administrator confirms the deletion.
24. The system removes the user record or marks it as inactive based on data retention policy.
25. The system confirms the deletion action.
26. The system returns to the User Management interface.

**Alternative Flows:**

A1: Bulk Import (from Step 5)  
The Administrator selects "Import from File" instead of individual Add. The system accepts a CSV/Excel file, validates the format, processes each record, and provides a summary of successful imports and errors.

A2: Reset Password (from Step 14)  
During Edit, the Administrator may select "Reset Password." The system generates a new temporary password, updates the record, and sends credentials to the user's email.

A3: Deactivate Instead of Delete (from Step 21)  
If the user has historical records preventing deletion, the system offers "Deactivate Account" option, which disables login but preserves all historical data.

**Exception Flows:**

E1: Duplicate User ID (from Step 8)  
If the entered ID already exists:  
- The system displays: "User ID already exists in the system"  
- The system suggests available alternatives or allows modification  
- The Administrator enters a unique ID and resubmits

E2: Invalid Email Format (from Step 8)  
If the email address format is invalid:  
- The system highlights the email field  
- The system displays format requirements  
- The Administrator corrects the email and resubmits

E3: User Has Active Assignments (from Step 21)  
If the user is currently assigned to active modules:  
- The system lists the active module assignments  
- The system requires the Administrator to reassign or remove these associations first  
- The system prevents deletion until dependencies are resolved

E4: Email Delivery Failure (from Step 10)  
If the notification email cannot be sent:  
- The system saves the user record successfully  
- The system displays a warning: "User created but email notification failed. Please manually provide credentials."  
- The system displays the temporary password on screen for the Administrator to copy  
- The system logs the email failure for technical review

---

### UC-003: Assign Referring Teacher

**Use Case Name:** Assign Referring Teacher  
**Primary Actor:** Administrator  
**Goal:** To designate one or more teachers as referring teachers for specific teaching modules.  
**Preconditions:**
- Administrator is authenticated and logged into the system
- Target module exists in the system (UC-001 completed)
- Target teacher exists in the global database (UC-002 completed)  
**Postconditions:**
- Teacher is associated with the module as a referring teacher
- Referring teacher gains module management privileges
- Association is persisted and effective immediately

**Flow of Events:**

**Basic Flow:**
1. The Administrator selects the "Assign Referring Teachers" function from the main menu or from within UC-001.
2. The system displays a list of available modules without referring teachers or with existing referring teachers indicated.
3. The Administrator selects a target module from the list.
4. The system displays the current referring teacher assignments for the selected module (if any).
5. The system provides an "Add Referring Teacher" option.
6. The Administrator selects "Add Referring Teacher."
7. The system displays a searchable list of eligible teachers from the global database.
8. The Administrator searches for and selects a teacher to assign.
9. The system validates that the selected teacher is not already assigned as referring teacher for this module.
10. The system adds the teacher as a referring teacher for the module.
11. The system updates the module record with the new association.
12. The system sends a notification to the newly assigned referring teacher.
13. The system displays the updated referring teacher list for the module.
14. The Administrator may assign additional referring teachers (return to Step 6) or exit.

**Alternative Flows:**

A1: Remove Referring Teacher (from Step 4)  
The Administrator selects an existing referring teacher and chooses "Remove Assignment." The system validates that at least one referring teacher remains (or warns if removing the last), removes the association, and notifies the teacher of the removal.

A2: Transfer Responsibilities (from Step 8)  
Instead of adding, the Administrator may select "Replace" on an existing referring teacher, which requires selecting a new teacher and transferring all module associations before removing the original.

**Exception Flows:**

E1: Teacher Already Assigned (from Step 9)  
If the selected teacher is already a referring teacher for this module:  
- The system displays: "This teacher is already assigned as referring teacher for this module"  
- The system returns to the teacher selection list

E2: Teacher Not Eligible (from Step 8)  
If the selected teacher is inactive or lacks required qualifications:  
- The system displays the reason for ineligibility  
- The system prevents selection and returns to the list

E3: Module Not Found (from Step 3)  
If the selected module ID is invalid due to concurrent deletion:  
- The system displays: "Module no longer exists"  
- The system refreshes the module list  
- The Administrator selects a different module

---

### UC-004: Manage Module Personnel

**Use Case Name:** Manage Module Personnel  
**Primary Actor:** Referring Teacher  
**Goal:** To add registered teachers and students to modules under their responsibility.  
**Preconditions:**
- Referring Teacher is authenticated and logged into the system
- Referring Teacher has been assigned to at least one module (UC-003 completed)
- Target users exist in the global database (UC-002 completed)  
**Postconditions:**
- Teachers and students are associated with the module
- Associated teachers can report absences for the module
- Associated students can have absences recorded in the module
- Changes are persisted and immediately effective

**Flow of Events:**

**Basic Flow:**
1. The Referring Teacher selects the "My Modules" function from the main menu.
2. The system displays a list of modules where the Referring Teacher is assigned as referring teacher.
3. The Referring Teacher selects a specific module to manage.
4. The system displays the Module Management dashboard with tabs for "Teachers" and "Students."
5. The Referring Teacher selects the "Teachers" tab.
6. The system displays currently assigned teachers for the module.
7. The Referring Teacher selects "Add Teacher."
8. The system displays a searchable list of available teachers from the global database (excluding already assigned).
9. The Referring Teacher searches for and selects one or more teachers to add.
10. The system validates that selected teachers are registered and available.
11. The system adds the selected teachers to the module.
12. The system notifies the added teachers of their module assignment.
13. The system updates the teacher list display.
14. The Referring Teacher selects the "Students" tab.
15. The system displays currently enrolled students for the module.
16. The Referring Teacher selects "Add Students."
17. The system displays a searchable list of available students from the global database (excluding already enrolled).
18. The Referring Teacher searches for and selects one or more students to enroll.
19. The system validates that selected students are registered and eligible.
20. The system enrolls the selected students in the module.
21. The system notifies the enrolled students of their module enrollment.
22. The system updates the student list display.
23. The Referring Teacher may add more personnel or exit the module management interface.

**Alternative Flows:**

A1: Remove Teacher (from Step 6)  
The Referring Teacher selects an assigned teacher and chooses "Remove." The system checks for pending absence reports or historical data, warns if data exists, and upon confirmation, removes the association and notifies the teacher.

A2: Remove Student (from Step 15)  
The Referring Teacher selects an enrolled student and chooses "Remove." The system checks for existing absence records. If records exist, the system warns that historical data will be preserved but the student will be marked as withdrawn. Upon confirmation, the system updates the status.

A3: Bulk Enrollment (from Steps 9 or 18)  
The Referring Teacher may upload a CSV file with multiple user IDs for batch processing. The system validates each ID, processes valid entries, and provides a report of successes and failures.

**Exception Flows:**

E1: User Not in Database (from Steps 10 or 19)  
If a selected user ID does not exist in the global database:  
- The system displays: "User not found in global database. Please contact Administrator to add user first."  
- The system removes the invalid selection from the current operation  
- The Referring Teacher may select different users

E2: User Already Assigned (from Steps 10 or 19)  
If a selected user is already associated with the module:  
- The system skips the duplicate without error  
- The system includes this information in the confirmation summary

E3: Student Enrollment Limit Reached (from Step 19)  
If adding students would exceed the module capacity:  
- The system displays: "Module capacity limit reached. Cannot add more students."  
- The system suggests contacting Administrator to increase capacity  
- The system processes only up to the limit

---

### UC-005: Report Student Absence

**Use Case Name:** Report Student Absence  
**Primary Actor:** Teacher  
**Goal:** To record a student's absence in a module and optionally add explanatory comments.  
**Preconditions:**
- Teacher is authenticated and logged into the system
- Teacher is assigned to at least one module (UC-004 completed)
- Target student is enrolled in the module (UC-004 completed)
- Class session is scheduled for the current or past date  
**Postconditions:**
- Absence record is created with status "Unjustified"
- Record includes timestamp, reporter ID, and optional comment
- Absence is visible to referring teachers and administrative staff
- Student's absence count is updated

**Flow of Events:**

**Basic Flow:**
1. The Teacher selects the "Record Absence" function from the main menu.
2. The system displays a list of modules where the Teacher is assigned.
3. The Teacher selects the module for which to report an absence.
4. The system displays the class session selection interface (defaulting to current date).
5. The Teacher selects or confirms the class session date.
6. The system displays the enrollment list for the selected module and date, showing attendance status for each student (Present/Absent/Not Recorded).
7. The Teacher identifies the absent student(s) and selects "Mark Absent" for each.
8. The system marks the selected student(s) as absent and displays a comment entry dialog.
9. The Teacher enters optional comments explaining the absence (e.g., "Student notified of illness via email") or leaves blank.
10. The Teacher submits the absence report.
11. The system validates the data (student enrollment, date validity).
12. The system creates the absence record with status "Unjustified."
13. The system updates the student's absence statistics.
14. The system checks if this absence triggers the unjustified absence threshold (more than 3).
15. If threshold exceeded, the system flags the record for alert processing (UC-009).
16. The system displays confirmation: "Absence recorded successfully."
17. The system returns to the enrollment list for additional entries or exit.

**Alternative Flows:**

A1: Mark Present (Correction) (from Step 6)  
If a student was previously marked absent in error, the Teacher may select "Mark Present" to remove the absence record before it is justified by Administrative Staff.

A2: Bulk Absence Entry (from Step 7)  
The Teacher may select multiple students simultaneously to mark absent, enter a common comment (e.g., "Field trip group"), and submit all at once.

A3: Future Date Entry (from Step 5)  
For planned absences known in advance, the Teacher may select a future date within the academic calendar and record the anticipated absence.

**Exception Flows:**

E1: Student Not Enrolled (from Step 11)  
If the selected student is not enrolled in the module:  
- The system displays: "Student is not enrolled in this module"  
- The system does not create the record  
- The Teacher may select a different student or exit

E2: Duplicate Absence Report (from Step 11)  
If an absence record already exists for this student, module, and date:  
- The system displays the existing record with reporter and timestamp  
- The system asks: "Update existing record or cancel?"  
- If update, the system replaces the comment if provided  
- If cancel, no changes are made

E3: Past Reporting Deadline (from Step 11)  
If the date exceeds the allowed reporting window (e.g., 30 days):  
- The system displays: "Reporting deadline exceeded. Contact Administrator."  
- The system prevents record creation  
- The system logs the attempt for audit

---

### UC-006: Consult Module Absences

**Use Case Name:** Consult Module Absences  
**Primary Actor:** Teacher  
**Goal:** To view the list of absences for all students enrolled in modules they teach.  
**Preconditions:**
- Teacher is authenticated and logged into the system
- Teacher is assigned to at least one module (UC-004 completed)  
**Postconditions:**
- Absence data is displayed in the requested format
- No data is modified (read-only operation)
- Viewing activity may be logged for audit purposes

**Flow of Events:**

**Basic Flow:**
1. The Teacher selects the "View Absences" function from the main menu.
2. The system displays the Absence Consultation interface with filter options.
3. The Teacher selects filter criteria: Module (dropdown of assigned modules), Date Range, Student (optional), Status (All/Justified/Unjustified).
4. The Teacher submits the query.
5. The system validates that the Teacher has access to the selected module.
6. The system retrieves absence records matching the criteria.
7. The system displays the results in a sortable table with columns: Date, Student ID, Student Name, Status, Reporter, Comments.
8. The Teacher may click on any record to view full details.
9. The system displays the detailed absence view including justification reason (if applicable), administrative notes, and audit trail.
10. The Teacher may export the results to PDF/Excel, print, or return to the list.
11. The Teacher may modify filters and repeat the query or exit.

**Alternative Flows:**

A1: Quick View Dashboard (from Step 2)  
The system provides a default dashboard view showing summary statistics (total absences this week, unjustified count, top absentees) without requiring filter selection.

A2: Student-Centric View (from Step 7)  
The Teacher may switch to "Group by Student" view, which aggregates all absences per student with counts and trends, rather than chronological list.

A3: Alert View (from Step 2)  
The Teacher may select "View Alert List" to see only students in their modules with more than 3 unjustified absences (subset of UC-009).

**Exception Flows:**

E1: No Access to Module (from Step 5)  
If the Teacher attempts to view a module they are not assigned to:  
- The system displays: "Access denied: You are not authorized to view this module's data"  
- The system logs the access attempt for security review  
- The system returns to module selection with only authorized modules listed

E2: No Records Found (from Step 6)  
If no absence records match the criteria:  
- The system displays: "No absence records found for the selected criteria"  
- The system offers to broaden filters or return to main menu

E3: Data Retrieval Timeout (from Step 6)  
If the query exceeds processing time limits (large date range):  
- The system displays: "Query timeout. Please narrow your date range or contact support"  
- The system suggests maximum efficient date ranges

---

### UC-007: Justify Student Absence

**Use Case Name:** Justify Student Absence  
**Primary Actor:** Administrative Staff  
**Goal:** To enter the official reason for a student's absence and change its status to justified.  
**Preconditions:**
- Administrative Staff is authenticated and logged into the system
- Target absence record exists with status "Unjustified" (UC-005 completed)
- Administrative Staff has access to absence records (system-wide or delegated scope)  
**Postconditions:**
- Absence record status is updated to "Justified"
- Justification reason is recorded with timestamp and staff ID
- Student's unjustified absence count is decremented
- Alert status is recalculated if applicable

**Flow of Events:**

**Basic Flow:**
1. The Administrative Staff selects the "Process Absences" function from the main menu.
2. The system displays the Absence Processing interface with a queue of pending (unjustified) absences.
3. The system displays absences sorted by date (oldest first) with student and module details.
4. The Administrative Staff selects an absence record to process.
5. The system displays the absence details: Student info, Module, Date, Reporter, Teacher Comments, Current Status.
6. The system provides a form for entering justification details: Reason Category (Illness, Family Emergency, Academic Activity, Other), Detailed Explanation, Supporting Document Reference (optional).
7. The Administrative Staff enters the justification information.
8. The Administrative Staff submits the justification.
9. The system validates the completeness of the justification data.
10. The system updates the absence record status to "Justified."
11. The system records the justification metadata (staff ID, timestamp, reason).
12. The system recalculates the student's unjustified absence count.
13. If the student previously exceeded the alert threshold and now falls below it, the system updates the alert status.
14. The system sends a notification to the student confirming the justified absence.
15. The system sends a notification to the referring teacher of the module.
16. The system displays confirmation: "Absence justified successfully."
17. The system returns to the pending absences queue.

**Alternative Flows:**

A1: Reject Justification (from Step 8)  
If the justification is insufficient, the Administrative Staff may select "Request More Information" instead of submitting. The system returns the record to the referring teacher with a comment requesting additional documentation.

A2: Batch Justification (from Step 4)  
The Administrative Staff may select multiple absence records for the same student with the same reason (e.g., medical leave spanning multiple days) and justify them all with a single submission.

A3: View Student History (from Step 5)  
Before processing, the Administrative Staff may select "View Student Absence History" to see the full context of the student's attendance record across all modules.

**Exception Flows:**

E1: Record Already Justified (from Step 4)  
If the absence was already justified by another staff member:  
- The system displays: "This absence has already been justified by [Staff Name] on [Date]"  
- The system shows the existing justification  
- The system removes the record from the queue  
- The Administrative Staff selects a different record

E2: Insufficient Justification Data (from Step 9)  
If required fields are missing:  
- The system highlights the missing fields  
- The system displays: "Please complete all required fields"  
- The Administrative Staff completes the information and resubmits

E3: Student Record Locked (from Step 10)  
If the student record is under review or hold status:  
- The system displays: "Student record is currently locked. Cannot process justification."  
- The system logs the attempt  
- The Administrative Staff contacts Administrator for resolution

---

### UC-008: Generate Absence Reports

**Use Case Name:** Generate Absence Reports  
**Primary Actor:** Administrative Staff  
**Goal:** To view and group student absences by module or by student for comprehensive oversight.  
**Preconditions:**
- Administrative Staff is authenticated and logged into the system
- Absence records exist in the system (UC-005 completed)  
**Postconditions:**
- Report is generated and displayed or exported
- No data is modified (read-only operation)
- Report generation is logged for audit purposes

**Flow of Events:**

**Basic Flow:**
1. The Administrative Staff selects the "Reports" function from the main menu.
2. The system displays the Reporting interface with report type options.
3. The Administrative Staff selects report type: "By Module" or "By Student."
4. **IF** By Module: The system displays module selection options (all modules or specific).
5. The Administrative Staff selects the desired module(s) and date range.
6. The system retrieves absence data aggregated by module.
7. The system displays the report showing: Module Info, Total Enrolled, Total Absences, Justified vs Unjustified breakdown, List of absent students with details.
8. **IF** By Student: The system displays student search options.
9. The Administrative Staff enters search criteria (Student ID, Name, or Group) and date range.
10. The system retrieves absence data aggregated by student.
11. The system displays the report showing: Student Info, Total Modules, Absence Count per Module, Total Justified/Unjustified, Alert Status.
12. The Administrative Staff may apply additional filters (Status, Module, Date range).
13. The system updates the report display based on filters.
14. The Administrative Staff may export the report to PDF, Excel, or print.
15. The system generates the export file and provides download/print options.
16. The Administrative Staff may generate another report or exit.

**Alternative Flows:**

A1: Combined Report (from Step 3)  
The Administrative Staff may select "Combined View" which presents a matrix: rows as students, columns as modules, cells showing absence counts, enabling quick identification of patterns.

A2: Trend Analysis (from Step 7 or 11)  
The system may display graphical trend charts (line/bar charts) showing absence patterns over time for the selected grouping.

A3: Scheduled Reports (from Step 2)  
The Administrative Staff may access "Scheduled Reports" to view previously generated periodic reports (weekly/monthly summaries) saved by the system.

**Exception Flows:**

E1: No Data for Criteria (from Steps 6 or 10)  
If no absence records exist for the selected criteria:  
- The system displays: "No data found for the selected report criteria"  
- The system suggests broadening the date range or selecting different parameters

E2: Export Generation Failure (from Step 14)  
If the export file cannot be generated due to size or system error:  
- The system displays: "Report generation failed. Data set may be too large. Try narrowing your criteria."  
- The system offers to generate in smaller chunks or contact technical support

E3: Permission Denied (from Step 1)  
If the Administrative Staff lacks reporting privileges:  
- The system displays: "Access denied: Insufficient privileges for reporting functions"  
- The system logs the access attempt

---

### UC-009: Monitor Unjustified Absence Alerts

**Use Case Name:** Monitor Unjustified Absence Alerts  
**Primary Actor:** Teacher (Teaching Staff)  
**Goal:** To receive and view alerts about students with more than three unjustified absences.  
**Preconditions:**
- Teacher is authenticated and logged into the system
- Teacher is assigned to at least one module (UC-004 completed)
- Absence records exist with unjustified status (UC-005 completed)  
**Postconditions:**
- Alert list is displayed with current data
- Teacher is informed of at-risk students
- Alert viewing may be logged for follow-up tracking

**Flow of Events:**

**Basic Flow:**
1. The Teacher logs into the system.
2. The system checks for any students in the Teacher's assigned modules with more than 3 unjustified absences.
3. **IF** such students exist: The system displays a dashboard alert notification: "Attention: Students with excessive absences require review."
4. The Teacher selects the "Absence Alerts" function from the main menu or clicks the dashboard notification.
5. The system displays the Alert Monitor interface.
6. The system retrieves and displays the list of students meeting the criteria (>3 unjustified absences) within the Teacher's module scope.
7. For each student, the system displays: Student ID, Name, Module, Unjustified Absence Count, Last Absence Date, Alert Level (4=Warning, 5+=Critical).
8. The Teacher may select a specific student to view detailed absence history.
9. The system displays the detailed view: Chronological list of all absences for that student across all their modules, with status and justification details.
10. The Teacher may mark the alert as "Acknowledged" indicating they have seen and will act on the information.
11. The system records the acknowledgment with timestamp.
12. The Teacher may return to the alert list or exit.

**Alternative Flows:**

A1: Filter by Alert Level (from Step 6)  
The Teacher may filter the alert list to show only Critical (5+) or Warning (4) level alerts.

A2: Export Alert List (from Step 7)  
The Teacher may export the current alert list to PDF for departmental meetings or intervention planning.

A3: Notify Student (from Step 9)  
From the detailed view, the Teacher may select "Send Notification" to trigger a system message to the student about their absence status and potential consequences.

**Exception Flows:**

E1: No Alerts (from Step 3)  
If no students meet the alert criteria:  
- The system displays: "No absence alerts at this time. All students within acceptable absence limits."  
- The system still allows access to the Alert Monitor to view historical alerts or adjust threshold

E2: Data Synchronization Delay (from Step 6)  
If the alert data is temporarily stale due to processing delays:  
- The system displays: "Alert data last updated: [timestamp]. Recent changes may not be reflected."  
- The system offers a manual refresh option

E3: Student Withdrawn (from Step 8)  
If the student has been withdrawn from the module since the alert was generated:  
- The system displays: "Student is no longer enrolled in this module"  
- The system archives the alert  
- The system removes the student from active alert list

---

## 4. SUBFLOWS (Reusable Components)

**Subflow: Authenticate User**
1. The system displays the login form requesting User ID and Password.
2. The user enters credentials and submits.
3. The system validates the credentials against the user database.
4. **IF** valid: The system establishes a session, logs the login, and redirects to the role-appropriate dashboard.
5. **IF** invalid: The system increments failed attempt counter.
6. **IF** failed attempts < 3: The system displays "Invalid credentials. Please try again" and returns to Step 2.
7. **IF** failed attempts >= 3: The system locks the account and displays "Account locked. Contact Administrator."

**Subflow: Validate User Permissions**
1. The system retrieves the user's role and permission set from the session.
2. The system checks if the requested operation is in the allowed permission set.
3. **IF** permitted: The system proceeds with the operation.
4. **IF** not permitted: The system logs the access attempt and displays "Access Denied."

**Subflow: Send Notification**
1. The system receives notification parameters: recipient ID, message type, content.
2. The system retrieves the recipient's contact preferences (email, in-app, SMS).
3. The system formats the message according to the type template.
4. The system queues the notification for delivery via preferred channels.
5. The system logs the notification dispatch.
6. The system confirms notification sent or queued.

---

## 5. USE-CASE DIAGRAM RELATIONSHIPS

**Include Relationships:**
- All use cases include **Authenticate User** subflow at initiation
- UC-001, UC-002, UC-003 include **Validate User Permissions** before operations
- UC-005, UC-007 include **Send Notification** for relevant updates

**Extend Relationships:**
- UC-009 extends UC-006 (Consult Module Absences) when alert threshold is detected
- UC-003 extends UC-001 when creating new modules

**Generalization:**
- Referring Teacher is a specialization of Teacher (inherits all Teacher use cases plus UC-004)
- Administrative Staff may inherit read-only access to UC-006

---
