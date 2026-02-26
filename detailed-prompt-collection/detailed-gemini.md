Here is the Software Requirements Specification for the **www.kiestla.edu** Attendance Management System, modeled according to the Ivar Jacobson / RUP Use-Case methodology.

# Software Requirements Specification (SRS)

**Project:** Kiestla Attendance Portal

---

## 1. Identify Actors

### **Administrator**

**Brief Description:** The super-user responsible for the structural configuration of the system. This actor exists to ensure the foundational data (users and course structures) is correct and up-to-date so that the operational actors can perform their tasks.

### **Referring Teacher**

**Brief Description:** A specific faculty member assigned ownership of a teaching module. They play a managerial role for their specific courses, responsible for defining which other teachers and students belong to that module.

### **Teacher**

**Brief Description:** Academic staff members responsible for conducting classes. Their role is to capture operational data (attendance) and monitor the engagement of students within their assigned classes.
*(Note: A Referring Teacher also inherits all capabilities of a Teacher).*

### **Administrative Staff**

**Brief Description:** Staff members responsible for the bureaucratic handling of student records. They exist to process the justification of absences and maintain oversight of the institution's overall attendance compliance.

---

## 2. Identify Use Cases

### **Use Case: Manage Global Database**

**Brief Description:** Allows the **Administrator** to create, update, and delete student and teacher profiles in the central repository. This ensures that a pool of valid users exists for assignment to specific modules.

### **Use Case: Manage Teaching Modules**

**Brief Description:** Allows the **Administrator** to define new teaching modules and assign a Referring Teacher to them. This sets up the digital environment where attendance can be tracked.

### **Use Case: Configure Module Participants**

**Brief Description:** Allows the **Referring Teacher** to populate their module by selecting existing teachers and students from the global database. This links the generic user pool to specific academic contexts.

### **Use Case: Report Absence**

**Brief Description:** Allows a **Teacher** to record that a student was not present during a session and optionally add a qualitative comment. This provides the raw data for attendance tracking.

### **Use Case: Justify Absence**

**Brief Description:** Allows **Administrative Staff** to review recorded absences and input the official reason (e.g., medical certificate). This changes the status of an absence from "unjustified" to "justified."

### **Use Case: Consult Absences**

**Brief Description:** Allows **Teachers** to view records for their modules, and **Administrative Staff** to view all records (grouped by module or student). This provides visibility into student attendance trends.

### **Use Case: Monitor At-Risk Students**

**Brief Description:** alerts **Teaching Staff** to students who have accumulated more than three unjustified absences. This facilitates early intervention for students at risk of failure due to non-attendance.

---

## 3. Full Use-Case Descriptions

### **Use Case: Configure Module Participants**

* **Primary Actor:** Referring Teacher
* **Goal:** To populate a teaching module with the correct students and assistant teachers.
* **Preconditions:**
1. The User (Referring Teacher) is logged in.
2. The target module has been created by the Administrator.
3. The students and teachers to be added already exist in the Global Database.


* **Postconditions:** The selected users are associated with the module and will appear in future attendance lists.

#### **4. Flow of Events**

**Basic Flow (Happy Path)**

1. The **Referring Teacher** selects the "My Modules" option from the dashboard.
2. The **System** displays a list of modules where the actor is the designated referrer.
3. The **Referring Teacher** selects a specific module to configure.
4. The **System** displays the current list of enrolled students and associated teachers.
5. The **Referring Teacher** selects the "Add Participant" function.
6. The **System** prompts for a search criteria (Name or ID).
7. The **Referring Teacher** enters the search criteria and submits.
8. The **System** searches the Global Database and displays matching results.
9. The **Referring Teacher** selects the desired user(s) and confirms the addition.
10. The **System** links the user to the module and displays a success message.

**Alternative Flows**

* **A1: Bulk Addition (from Step 6)**
1. The **Referring Teacher** chooses to upload a list of IDs.
2. The **System** parses the list and matches them against the Global Database.
3. The **System** presents a summary of found users.
4. The flow resumes at Step 9.



**Exception Flows**

* **E1: User Not Found (from Step 8)**
1. The **System** finds no match in the Global Database.
2. The **System** displays an error: "User not registered in Global Database. Contact Administrator."
3. The flow returns to Step 6.


* **E2: User Already Enrolled (from Step 9)**
1. The **Referring Teacher** selects a user who is already in the module.
2. The **System** notifies the actor that the association already exists.
3. The system prevents duplicate entry and resumes at Step 4.



---

### **Use Case: Report Absence**

* **Primary Actor:** Teacher
* **Goal:** To record a student's lack of attendance for a specific class session.
* **Preconditions:** The Teacher is assigned to the module.
* **Postconditions:** An absence record is created with the status "Unjustified."

#### **4. Flow of Events**

**Basic Flow (Happy Path)**

1. The **Teacher** navigates to the "Attendance Entry" page.
2. The **System** displays a list of modules assigned to the teacher.
3. The **Teacher** selects the relevant module.
4. The **System** retrieves and displays the list of enrolled students.
5. The **Teacher** identifies the absent student(s) and marks the checkbox next to their name.
6. The **System** highlights the selection and enables the "Add Comment" field.
7. The **Teacher** (optionally) types a comment regarding the absence (e.g., "Arrived very late" or "Left early").
8. The **Teacher** clicks "Submit Absences."
9. The **System** saves the records as "Unjustified" and confirms the submission.
10. The **System** checks the total unjustified absences for the student. (See *Subflow: Alert Trigger*).

**Alternative Flows**

* **A1: No Absences (from Step 5)**
1. The **Teacher** marks a "All Present" toggle.
2. The **System** records attendance for the session without absence records.
3. The flow ends.



**Subflow: Alert Trigger**

1. The **System** calculates the new total of unjustified absences for the student.
2. IF the total > 3, the **System** flags the student record for the "At-Risk" dashboard.

---

### **Use Case: Justify Absence**

* **Primary Actor:** Administrative Staff
* **Goal:** To process an excuse (medical/legal) and update the absence status.
* **Preconditions:** An absence has been recorded by a teacher.
* **Postconditions:** The absence status is updated to "Justified" and the reason is logged.

#### **4. Flow of Events**

**Basic Flow (Happy Path)**

1. The **Administrative Staff** logs into the administrative dashboard.
2. The **System** displays a summary of recent absences.
3. The **Actor** searches for a specific student or selects a module to view "Unjustified Absences."
4. The **System** displays a list of absences requiring attention.
5. The **Actor** selects a specific absence record.
6. The **System** presents the details (Date, Module, Teacher Comment) and an input field for "Justification Reason."
7. The **Actor** enters the reason (e.g., "Medical Certificate provided").
8. The **Actor** confirms the justification.
9. The **System** updates the record status to "Justified."
10. The **System** recalculates the student's "At-Risk" status (decrementing the unjustified count).

**Exception Flows**

* **E1: Database Connection Failure (from Step 9)**
1. The **System** fails to update the record.
2. The **System** displays an error message and retains the input data.
3. The **Actor** is prompted to retry.



---

### **Use Case: Monitor At-Risk Students**

* **Primary Actor:** Teacher (or Referring Teacher)
* **Goal:** To identify students exceeding the threshold of allowed unjustified absences.
* **Preconditions:** Students exist with > 3 unjustified absences.
* **Postconditions:** The teacher is informed of at-risk students.

#### **4. Flow of Events**

**Basic Flow (Happy Path)**

1. The **Teacher** accesses the system homepage or dashboard.
2. The **System** queries the database for all students linked to the Teacher's modules who have > 3 unjustified absences.
3. The **System** displays a prominent "At-Risk Alerts" widget or page.
4. The **Teacher** clicks to view the details.
5. The **System** lists the students, their total unjustified count, and the specific modules where absences occurred.

**Alternative Flows**

* **A1: No At-Risk Students**
1. The **System** finds no students exceeding the threshold.
2. The **System** displays a "No Attendance Alerts" status on the dashboard.



---

### **Use Case: Consult Absences (Global)**

* **Primary Actor:** Administrative Staff
* **Goal:** To view attendance data organized by different hierarchies for reporting or auditing.
* **Preconditions:** None.
* **Postconditions:** Data is displayed.

#### **4. Flow of Events**

**Basic Flow (Happy Path)**

1. The **Administrative Staff** selects "Global Attendance Report."
2. The **System** prompts the user to group by: "Student" or "Module."
3. The **Actor** selects "Group by Module."
4. The **System** displays a list of modules.
5. The **Actor** selects a module.
6. The **System** displays all absences (justified and unjustified) for that module.

**Alternative Flows**

* **A1: Group by Student (from Step 3)**
1. The **Actor** selects "Group by Student."
2. The **System** displays a searchable list of students.
3. The **Actor** selects a student.
4. The **System** displays a chronological list of all absences for that student across all modules.



---

### Next Steps for the User

Would you like me to generate a **Domain Model** (Class Diagram description) to visualize how the "Global Database," "Modules," and "Absence Records" relate to one another based on these use cases?
