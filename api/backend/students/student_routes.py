from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for student-related routes
students = Blueprint("students", __name__)


# GET /students  — return all students
@students.route("/students", methods=["GET"])
def get_all_students():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /students")
        cursor.execute(
            "SELECT student_id, name, email, major, active_status, resume_url "
            "FROM student ORDER BY name"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"get_all_students: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /students/<id>  — one student's profile
@students.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT student_id, name, email, major, active_status, resume_url "
            "FROM student WHERE student_id = %s",
            (student_id,),
        )
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /students/<id>/applications  — all applications by a student
@students.route("/students/<int:student_id>/applications", methods=["GET"])
def get_student_applications(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT student_id FROM student WHERE student_id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404
        cursor.execute(
            "SELECT a.application_id, a.position_id, p.position_title, "
            "a.application_status, a.submitted_date "
            "FROM application a JOIN position p ON p.position_id = a.position_id "
            "WHERE a.student_id = %s ORDER BY a.submitted_date DESC",
            (student_id,),
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /students/<id>/saved  — save a position to the shortlist
@students.route("/students/<int:student_id>/saved", methods=["POST"])
def save_position(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "position_id" not in data:
            return jsonify({"error": "Missing required field: position_id"}), 400
        cursor.execute(
            "INSERT INTO saved_position (student_id, position_id) VALUES (%s, %s)",
            (student_id, data["position_id"]),
        )
        get_db().commit()
        return jsonify({"message": "Position saved"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /students/<id>/saved/<position_id>  — remove a saved position
@students.route("/students/<int:student_id>/saved/<int:position_id>", methods=["DELETE"])
def remove_saved_position(student_id, position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "DELETE FROM saved_position WHERE student_id = %s AND position_id = %s",
            (student_id, position_id),
        )
        get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Saved position not found"}), 404
        return jsonify({"message": "Saved position removed"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /students/<id>  — suspend / reactivate a student (admin)
@students.route("/students/<int:student_id>", methods=["PUT"])
def update_student_status(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "active_status" not in data:
            return jsonify({"error": "Missing required field: active_status"}), 400
        cursor.execute("SELECT student_id FROM student WHERE student_id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404
        cursor.execute(
            "UPDATE student SET active_status = %s, suspended_by_admin_id = %s "
            "WHERE student_id = %s",
            (data["active_status"], data.get("admin_id"), student_id),
        )
        get_db().commit()
        return jsonify({"message": "Student status updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()