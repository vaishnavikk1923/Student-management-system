
import os
import requests
import streamlit as st

API_URL = f"http://127.0.0.1:{os.environ.get('PORT', '8000')}"
#API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Student Management",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")
st.write("Manage student records using FastAPI and Streamlit.")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Choose an operation",
    ["View Students", "Add Student", "Update Student", "Delete Student"]
)


# VIEW STUDENTS
if menu == "View Students":
    st.header("All Students")

    dept = st.selectbox(
        "Filter by Department",
        ["All", "python", "java", "c"]
    )

    try:
        if dept == "All":
            response = requests.get(f"{API_URL}/students")
        else:

            response = requests.get(
                f"{API_URL}/students",
                params={"dept": dept}
            )

        if response.status_code == 200:
            students = response.json()

            if students:
                st.dataframe(students, use_container_width=True)
                st.success(f"Total students: {len(students)}")
            else:
                st.info("No students found.")

        else:
            st.error("Unable to retrieve students.")

    except requests.exceptions.ConnectionError:
        st.error("FastAPI is not running. Start the backend first.")


# ADD STUDENT
elif menu == "Add Student":
    st.header("Add a New Student")

    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        dept = st.selectbox("Department", ["python", "java", "c"])

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if name.strip():
                response = requests.post(
                    f"{API_URL}/add_student",
                    json={
                        "name": name.strip(),
                        "dept": dept
                    }
                )

                if response.status_code == 200:
                    st.success("Student added successfully!")
                    st.json(response.json())
                else:
                    st.error("Failed to add student.")
            else:
                st.warning("Please enter the student's name.")


# UPDATE STUDENT
elif menu == "Update Student":
    st.header("Update Student Details")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    with st.form("update_student_form"):
        name = st.text_input("New Name")
        dept = st.selectbox(
            "New Department",
            ["python", "java", "c"]
        )

        submitted = st.form_submit_button("Update Student")

        if submitted:
            if name.strip():
                response = requests.put(
                    f"{API_URL}/update_student/{student_id}",
                    json={
                        "name": name.strip(),
                        "dept": dept
                    }
                )

                if response.status_code == 200:
                    result = response.json()

                    if "student" in result:
                        st.success("Student updated successfully!")
                        st.json(result["student"])
                    else:
                        st.error(result["message"])
                else:
                    st.error("Failed to update student.")
            else:
                st.warning("Please enter the student's name.")


# DELETE STUDENT
elif menu == "Delete Student":
    st.header("Delete a Student")

    student_id = st.number_input(
        "Student ID to Delete",
        min_value=1,
        step=1,
        key="delete_id"
    )

    if st.button("Delete Student"):
        response = requests.delete(
            f"{API_URL}/delete_info/{student_id}"
        )

        if response.status_code == 200:
            result = response.json()

            if "student" in result:
                st.success("Student deleted successfully!")
                st.dataframe(
                    result["student"],
                    use_container_width=True
                )
            else:
                st.error(result["message"])
        else:
            st.error("Failed to delete student.")