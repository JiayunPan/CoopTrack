from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for admin / moderation routes
admin = Blueprint("admin", __name__)

# Allowed report review statuses
VALID_REPORT_STATUSES = ["PENDING", "RESOLVED", "DISMISSED"]


# GET /admin/reports  — pending flagged / reported postings
@admin.route("/admin/reports", methods=["GET"])
def get_pending_reports():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /admin/reports")
        cursor.execute(
            "SELECT r.report_id, r.reason, r.review_status, r.reported_at, "
            "p.position_id, p.position_title, e.company_name, "
            "st.name AS reported_by "
            "FROM report r "
            "JOIN position p ON p.position_id = r.position_id "
            "JOIN employer e ON e.employer_id = p.employer_id "
            "JOIN student st ON st.student_id = r.student_id "
            "WHERE r.review_status = 'PENDING' "
            "ORDER BY r.reported_at ASC"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"get_pending_reports: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /admin/employers  — list all employers (including pending)
@admin.route("/admin/employers", methods=["GET"])
def get_all_employers():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT employer_id, company_name, email, verification_status "
            "FROM employer ORDER BY verification_status, company_name"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /admin/placements  — placement rate by recruiting term
@admin.route("/admin/placements", methods=["GET"])
def get_placements():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT rt.term_id, rt.season, "
            "COUNT(DISTINCT CASE WHEN a.application_status = 'ACCEPTED' "
            "THEN a.student_id END) AS placed_students, "
            "COUNT(DISTINCT a.student_id) AS applicant_students, "
            "ROUND(100 * COUNT(DISTINCT CASE WHEN a.application_status = 'ACCEPTED' "
            "THEN a.student_id END) / NULLIF(COUNT(DISTINCT a.student_id), 0), 1) "
            "AS placement_rate "
            "FROM recruiting_term rt "
            "LEFT JOIN position p ON p.term_id = rt.term_id "
            "LEFT JOIN application a ON a.position_id = p.position_id "
            "GROUP BY rt.term_id, rt.season "
            "ORDER BY rt.term_id"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /admin/employers  — register and verify a new employer
@admin.route("/admin/employers", methods=["POST"])
def register_employer():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["company_name", "email"]
        for field in required:
            if not data or field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor.execute(
            "INSERT INTO employer "
            "(company_name, email, verification_status, verified_by_admin_id) "
            "VALUES (%s, %s, 'VERIFIED', %s)",
            (data["company_name"], data["email"], data.get("admin_id")),
        )
        get_db().commit()
        return jsonify({"message": "Employer registered and verified",
                        "employer_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /admin/reports/<id>  — resolve / close a report
@admin.route("/admin/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "review_status" not in data:
            return jsonify({"error": "Missing required field: review_status"}), 400
        new_status = data["review_status"]
        if new_status not in VALID_REPORT_STATUSES:
            return jsonify({"error": f"Invalid status. Must be one of {VALID_REPORT_STATUSES}"}), 400

        cursor.execute("SELECT report_id FROM report WHERE report_id = %s", (report_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Report not found"}), 404

        cursor.execute(
            "UPDATE report SET review_status = %s, reviewed_by_admin_id = %s "
            "WHERE report_id = %s",
            (new_status, data.get("admin_id"), report_id),
        )
        get_db().commit()
        return jsonify({"message": "Report updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()