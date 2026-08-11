from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for application-related routes
applications = Blueprint("applications", __name__)

# Allowed application statuses (used to validate PUT updates)
VALID_STATUSES = [
    "SUBMITTED", "SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "REJECTED",
]


# GET /applications  — return all applications
@applications.route("/applications", methods=["GET"])
def get_all_applications():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /applications")
        cursor.execute(
            "SELECT a.application_id, a.student_id, st.name AS student_name, "
            "a.position_id, p.position_title, a.application_status, a.submitted_date "
            "FROM application a "
            "JOIN student st ON st.student_id = a.student_id "
            "JOIN position p ON p.position_id = a.position_id "
            "ORDER BY a.submitted_date DESC"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"get_all_applications: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /applications/<id>  — one application's details
@applications.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT a.application_id, a.student_id, st.name AS student_name, st.email, "
            "a.position_id, p.position_title, e.company_name, a.application_status, "
            "a.submitted_date, a.interview_date, a.offer_date, a.accepted_date "
            "FROM application a "
            "JOIN student st ON st.student_id = a.student_id "
            "JOIN position p ON p.position_id = a.position_id "
            "JOIN employer e ON e.employer_id = p.employer_id "
            "WHERE a.application_id = %s",
            (application_id,),
        )
        application = cursor.fetchone()
        if not application:
            return jsonify({"error": "Application not found"}), 404
        return jsonify(application), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /applications  — submit a new application
@applications.route("/applications", methods=["POST"])
def create_application():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["student_id", "position_id"]
        for field in required:
            if not data or field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor.execute(
            "INSERT INTO application (student_id, position_id, application_status) "
            "VALUES (%s, %s, 'SUBMITTED')",
            (data["student_id"], data["position_id"]),
        )
        get_db().commit()
        return jsonify({"message": "Application submitted", "application_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /applications/<id>  — update application / pipeline status
@applications.route("/applications/<int:application_id>", methods=["PUT"])
def update_application_status(application_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "application_status" not in data:
            return jsonify({"error": "Missing required field: application_status"}), 400
        new_status = data["application_status"]
        if new_status not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status. Must be one of {VALID_STATUSES}"}), 400

        cursor.execute(
            "SELECT application_id FROM application WHERE application_id = %s",
            (application_id,),
        )
        if not cursor.fetchone():
            return jsonify({"error": "Application not found"}), 404

        cursor.execute(
            "UPDATE application SET application_status = %s, "
            "interview_date = CASE WHEN %s = 'INTERVIEW' THEN CURRENT_TIMESTAMP "
            "ELSE interview_date END, "
            "offer_date = CASE WHEN %s = 'OFFER' THEN CURRENT_DATE "
            "ELSE offer_date END, "
            "accepted_date = CASE WHEN %s = 'ACCEPTED' THEN CURRENT_DATE "
            "ELSE accepted_date END "
            "WHERE application_id = %s",
            (new_status, new_status, new_status, new_status, application_id),
        )
        get_db().commit()
        return jsonify({"message": "Application status updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /applications/<id>  — withdraw an application
@applications.route("/applications/<int:application_id>", methods=["DELETE"])
def withdraw_application(application_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "DELETE FROM application WHERE application_id = %s", (application_id,)
        )
        get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Application not found"}), 404
        return jsonify({"message": "Application withdrawn"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()