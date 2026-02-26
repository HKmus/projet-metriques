# Software Requirements Specification

## 1. Identify Actors

**Actor: Administrator**
- Brief Description: The administrator manages the creation, maintenance, and deletion of teaching modules and their association with one or more referring teachers. They also manage the global database of teachers and students.

**Actor: Teacher**
- Brief Description: Teachers can report absences for their modules, add comments to absences, and consult the list of absences for all students enrolled in their modules.

**Actor: Student**
- Brief Description: Students are part of the system, and their absences are recorded and managed. They might also have access to view their own attendance records, but the description doesn't specify this explicitly.

**Actor: Administrative Staff**
- Brief Description: The administrative staff enters the reason for absences and has access to all student absences. They can group absences by module and by student and are alerted to students with more than three unjustified absences.

## 2. Identify Use Cases

**Use Case: Manage Teaching Modules**
- Brief Description: The administrator creates, maintains, and deletes teaching modules and associates them with referring teachers. This is essential for organizing the modules and ensuring that teachers are assigned to the correct modules.

**Use Case: Manage User Database**
- Brief Description: The administrator manages a global database of teachers and students. This ensures that all users are registered and can be added to modules.

**Use Case: Report Absence**
- Brief Description: Teachers can report an absence for a student in one of their modules and add a comment. This is crucial for tracking student attendance.

**Use Case: Consult Absence List**
- Brief Description: Teachers can consult the list of absences for all students enrolled in their modules. This helps teachers keep track of attendance.

**Use Case: Justify Absence**
- Brief Description: Administrative staff enters the reason for an absence and has access to all student absences. This ensures that absences are properly documented and justified.

**Use Case: Alert on Unjustified Absences**
- Brief Description: The system alerts teaching staff to students with more than three unjustified absences. This helps in identifying students who may need intervention.

## 3. Write Full Use-Case Descriptions

### Use Case Name: Manage Teaching Modules
- **Primary Actor:** Administrator
- **Goal:** To manage the creation, maintenance, and deletion of teaching modules and their association with referring teachers.
- **Preconditions:**
  - The administrator is logged into the system.
- **Postconditions:**
  - Teaching modules are created, updated, or deleted as needed.
  - Teachers are associated with the appropriate modules.
- **Flow of Events:**
  - **Basic Flow:**
    1. The administrator initiates the creation of a new teaching module.
    2. The system prompts for module details (e.g., module name, description).
    3. The administrator enters the module details.
    4. The system saves the new module.
    5. The administrator associates one or more referring teachers with the module.
    6. The system updates the module with the associated teachers.
  - **Alternative Flows:**
    - A1: Module Update (from Step 1)
      1. The administrator selects an existing module to update.
      2. The system displays the current module details.
      3. The administrator modifies the module details.
      4. The system saves the updated module details.
    - A2: Module Deletion (from Step 1)
      1. The administrator selects an existing module to delete.
      2. The system confirms the deletion.
      3. The administrator confirms.
      4. The system deletes the module.
  - **Exception Flows:**
    - E1: Invalid Module Details (from Step 3)
      1. The system detects invalid or incomplete module details.
      2. The system prompts the administrator to correct the details.
      3. The administrator corrects the details.
      4. Resume from Step 4.

### Use Case Name: Manage User Database
- **Primary Actor:** Administrator
- **Goal:** To manage the global database of teachers and students.
- **Preconditions:**
  - The administrator is logged into the system.
- **Postconditions:**
  - The database is updated with new users or updated user information.
- **Flow of Events:**
  - **Basic Flow:**
    1. The administrator initiates the addition of a new user (teacher or student).
    2. The system prompts for user details (e.g., name, contact information).
    3. The administrator enters the user details.
    4. The system saves the new user.
  - **Alternative Flows:**
    - A1: Update User Details (from Step 1)
      1. The administrator selects an existing user to update.
      2. The system displays the current user details.
      3. The administrator modifies the user details.
      4. The system saves the updated user details.
    - A2: Delete User (from Step 1)
      1. The administrator selects an existing user to delete.
      2. The system confirms the deletion.
      3. The administrator confirms.
      4. The system deletes the user.
  - **Exception Flows:**
    - E1: Invalid User Details (from Step 3)
      1. The system detects invalid or incomplete user details.
      2. The system prompts the administrator to correct the details.
      3. The administrator corrects the details.
      4. Resume from Step 4.

### Use Case Name: Report Absence
- **Primary Actor:** Teacher
- **Goal:** To report an absence for a student in one of their modules.
- **Preconditions:**
  - The teacher is logged into the system.
  - The teacher is associated with the module.
- **Postconditions:**
  - The absence is recorded in the system.
- **Flow of Events:**
  - **Basic Flow:**
    1. The teacher initiates the reporting of an absence.
    2. The system prompts for the module and student details.
    3. The teacher selects the module and student.
    4. The system records the absence.
    5. The teacher adds a comment (optional).
    6. The system saves the absence and comment.
  - **Alternative Flows:**
    - A1: Multiple Absences (from Step 3)
      1. The teacher selects multiple students for absence reporting.
      2. The system records absences for all selected students.
      3. The teacher adds a comment for each student (optional).
      4. The system saves the absences and comments.
  - **Exception Flows:**
    - E1: Invalid Module or Student (from Step 3)
      1. The system detects an invalid module or student.
      2. The system prompts the teacher to select valid options.
      3. The teacher corrects the selection.
      4. Resume from Step 4.

### Use Case Name: Consult Absence List
- **Primary Actor:** Teacher
- **Goal:** To consult the list of absences for all students enrolled in their modules.
- **Preconditions:**
  - The teacher is logged into the system.
  - The teacher is associated with at least one module.
- **Postconditions:**
  - The teacher views the list of absences.
- **Flow of Events:**
  - **Basic Flow:**
    1. The teacher initiates the consultation of the absence list.
    2. The system prompts for the module selection.
    3. The teacher selects the module.
    4. The system displays the list of absences for the selected module.
  - **Alternative Flows:**
    - A1: Filter Absences (from Step 4)
      1. The teacher applies filters (e.g., date range, student name).
      2. The system displays the filtered list of absences.
  - **Exception Flows:**
    - E1: No Absences Found (from Step 4)
      1. The system informs the teacher that no absences are found for the selected module.
      2. The teacher may select another module or cancel the operation.

### Use Case Name: Justify Absence
- **Primary Actor:** Administrative Staff
- **Goal:** To enter the reason for an absence and manage absence records.
- **Preconditions:**
  - The administrative staff is logged into the system.
- **Postconditions:**
  - The absence is justified and recorded in the system.
- **Flow of Events:**
  - **Basic Flow:**
    1. The administrative staff initiates the justification of an absence.
    2. The system prompts for the student and absence details.
    3. The administrative staff selects the student and absence.
    4. The system displays the absence details.
    5. The administrative staff enters the reason for the absence.
    6. The system saves the justification.
  - **Alternative Flows:**
    - A1: Bulk Justification (from Step 3)
      1. The administrative staff selects multiple absences to justify.
      2. The system displays details for all selected absences.
      3. The administrative staff enters reasons for each absence.
      4. The system saves the justifications.
  - **Exception Flows:**
    - E1: Invalid Absence Details (from Step 3)
      1. The system detects an invalid absence.
      2. The system prompts the administrative staff to select valid options.
      3. The administrative staff corrects the selection.
      4. Resume from Step 4.

### Use Case Name: Alert on Unjustified Absences
- **Primary Actor:** System
- **Goal:** To alert teaching staff to students with more than three unjustified absences.
- **Preconditions:**
  - The system is running and monitoring absences.
- **Postconditions:**
  - Teaching staff are alerted to students with more than three unjustified absences.
- **Flow of Events:**
  - **Basic Flow:**
    1. The system monitors the absence records.
    2. The system identifies students with more than three unjustified absences.
    3. The system generates an alert for the teaching staff.
    4. The teaching staff receive the alert.
  - **Alternative Flows:**
    - A1: Custom Alert Threshold (from Step 2)
      1. The system allows customization of the alert threshold.
      2. The administrative staff sets the custom threshold.
      3. The system monitors based on the custom threshold.
  - **Exception Flows:**
    - E1: Alert Failure (from Step 3)
      1. The system fails to generate the alert.
      2. The system logs the error and notifies the administrator.

## 4. Subflows (If Needed)

**Subflow: User Authentication**
- **Description:** This subflow handles the authentication of users (administrators, teachers, administrative staff).
- **Steps:**
  1. The user initiates login.
  2. The system prompts for credentials.
  3. The user enters credentials.
  4. The system verifies credentials.
  5. The system grants access based on user role.
