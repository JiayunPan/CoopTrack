from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for position-related routes
positions = Blueprint("positions", __name__)


# GET /positions  — search / list open positions
# Optional query params: role, location, skill, status, employer_id
@positions.route("/positions", methods=["GET"])
def get_all_positions():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /positions")
        role = request.args.get("role")
        location = request.args.get("location")
        skill = request.args.get("skill")
        status = request.args.get("status")
        employer_id = request.args.get("employer_id", type=int)

        query = (
            "SELECT DISTINCT p.position_id, p.employer_id, p.position_title, e.company_name, "
            "p.location, p.work_mode, p.employment_type, p.position_status, "
            "p.application_deadline "
            "FROM position p "
            "JOIN employer e ON e.employer_id = p.employer_id "
            "LEFT JOIN position_skill ps ON ps.position_id = p.position_id "
            "LEFT JOIN skill s ON s.skill_id = ps.skill_id "
            "WHERE 1=1"
        )
        params = []
        if role:
            query += " AND p.position_title LIKE %s"
            params.append(f"%{role}%")
        if location:
            query += " AND p.location LIKE %s"
            params.append(f"%{location}%")
        if skill:
            query += " AND s.skill_name = %s"
            params.append(skill)
        if status:
            query += " AND p.position_status = %s"
            params.append(status)
        if employer_id is not None:
            query += " AND p.employer_id = %s"
            params.append(employer_id)
        query += " ORDER BY p.application_deadline"

        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"get_all_positions: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /positions/<id>  — one position's details
@positions.route("/positions/<int:position_id>", methods=["GET"])
def get_position(position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT p.position_id, p.position_title, e.company_name, p.description, "
            "p.location, p.work_mode, p.employment_type, p.position_status, "
            "p.application_deadline "
            "FROM position p JOIN employer e ON e.employer_id = p.employer_id "
            "WHERE p.position_id = %s",
            (position_id,),
        )
        position = cursor.fetchone()
        if not position:
            return jsonify({"error": "Position not found"}), 404
        return jsonify(position), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /positions/<id>/applicants  — applicants ranked by skill match
@positions.route("/positions/<int:position_id>/applicants", methods=["GET"])
def get_position_applicants(position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT position_id FROM position WHERE position_id = %s", (position_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Position not found"}), 404
        cursor.execute(
            "SELECT a.application_id, st.student_id, st.name AS student_name, "
            "st.email, a.application_status, "
            "COUNT(DISTINCT ss.skill_id) AS matched_skill_count, "
            "COUNT(DISTINCT ps.skill_id) AS required_skill_count "
            "FROM application a "
            "JOIN student st ON st.student_id = a.student_id "
            "JOIN position p ON p.position_id = a.position_id "
            "LEFT JOIN position_skill ps ON ps.position_id = p.position_id "
            "LEFT JOIN student_skill ss ON ss.student_id = st.student_id "
            "AND ss.skill_id = ps.skill_id "
            "WHERE p.position_id = %s "
            "GROUP BY a.application_id, st.student_id, st.name, st.email, a.application_status "
            "ORDER BY matched_skill_count DESC",
            (position_id,),
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /positions/<id>/count  — application count for a position
@positions.route("/positions/<int:position_id>/count", methods=["GET"])
def get_position_count(position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT COUNT(*) AS application_count FROM application WHERE position_id = %s",
            (position_id,),
        )
        return jsonify(cursor.fetchone()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /positions  — post a new position
@positions.route("/positions", methods=["POST"])
def create_position():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["employer_id", "term_id", "position_title"]
        for field in required:
            if not data or field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor.execute(
            "INSERT INTO position "
            "(employer_id, term_id, position_title, description, location, "
            "work_mode, employment_type, position_status, application_deadline) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, 'OPEN', %s)",
            (
                data["employer_id"],
                data["term_id"],
                data["position_title"],
                data.get("description"),
                data.get("location"),
                data.get("work_mode"),
                data.get("employment_type"),
                data.get("application_deadline"),
            ),
        )
        get_db().commit()
        return jsonify({"message": "Position created", "position_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /positions/<id>  — edit a posting or close it
@positions.route("/positions/<int:position_id>", methods=["PUT"])
def update_position(position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        cursor.execute("SELECT position_id FROM position WHERE position_id = %s", (position_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Position not found"}), 404

        allowed = [
            "position_title", "description", "location", "work_mode",
            "employment_type", "position_status", "application_deadline",
        ]
        fields = [f"{f} = %s" for f in allowed if f in data]
        params = [data[f] for f in allowed if f in data]
        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400
        params.append(position_id)
        cursor.execute(
            f"UPDATE position SET {', '.join(fields)} WHERE position_id = %s", params
        )
        get_db().commit()
        return jsonify({"message": "Position updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /positions/<id>  — remove a posting from public view (admin)
@positions.route("/positions/<int:position_id>", methods=["DELETE"])
def delete_position(position_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT position_id FROM position WHERE position_id = %s", (position_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Position not found"}), 404
        cursor.execute(
            "UPDATE position SET position_status = 'REMOVED' WHERE position_id = %s",
            (position_id,),
        )
        get_db().commit()
        return jsonify({"message": "Position removed from public view"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
