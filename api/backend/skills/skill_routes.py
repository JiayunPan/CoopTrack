from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for skill-related routes
skills = Blueprint("skills", __name__)


# GET /skills  — list all skills
@skills.route("/skills", methods=["GET"])
def get_all_skills():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /skills")
        cursor.execute(
            "SELECT skill_id, skill_name, skill_status FROM skill ORDER BY skill_name"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f"get_all_skills: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /skills/demand  — most in-demand skills across postings
# NOTE: this static route is declared BEFORE /skills/<int:skill_id>
# so Flask matches "demand" as a literal, not as an id.
@skills.route("/skills/demand", methods=["GET"])
def get_skills_demand():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT s.skill_id, s.skill_name, "
            "COUNT(DISTINCT ps.position_id) AS posting_count "
            "FROM skill s JOIN position_skill ps ON ps.skill_id = s.skill_id "
            "GROUP BY s.skill_id, s.skill_name "
            "ORDER BY posting_count DESC, s.skill_name"
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /skills/<id>  — one skill's details
@skills.route("/skills/<int:skill_id>", methods=["GET"])
def get_skill(skill_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT skill_id, skill_name, skill_status FROM skill WHERE skill_id = %s",
            (skill_id,),
        )
        skill = cursor.fetchone()
        if not skill:
            return jsonify({"error": "Skill not found"}), 404
        return jsonify(skill), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /skills  — add a skill to the master list
@skills.route("/skills", methods=["POST"])
def create_skill():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data or "skill_name" not in data:
            return jsonify({"error": "Missing required field: skill_name"}), 400
        cursor.execute(
            "INSERT INTO skill (skill_name, skill_status, managed_by_admin_id) "
            "VALUES (%s, 'ACTIVE', %s)",
            (data["skill_name"], data.get("admin_id")),
        )
        get_db().commit()
        return jsonify({"message": "Skill created", "skill_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /skills/<id>  — update a skill (rename / status)
@skills.route("/skills/<int:skill_id>", methods=["PUT"])
def update_skill(skill_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        cursor.execute("SELECT skill_id FROM skill WHERE skill_id = %s", (skill_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Skill not found"}), 404

        allowed = ["skill_name", "skill_status"]
        fields = [f"{f} = %s" for f in allowed if f in data]
        params = [data[f] for f in allowed if f in data]
        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400
        params.append(skill_id)
        cursor.execute(
            f"UPDATE skill SET {', '.join(fields)} WHERE skill_id = %s", params
        )
        get_db().commit()
        return jsonify({"message": "Skill updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /skills/<id>  — delete an unused duplicate skill
# Only allowed if the skill is not referenced by any student or position.
@skills.route("/skills/<int:skill_id>", methods=["DELETE"])
def delete_skill(skill_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT skill_id FROM skill WHERE skill_id = %s", (skill_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Skill not found"}), 404

        # Refuse to delete if the skill is still in use
        cursor.execute(
            "SELECT "
            "(SELECT COUNT(*) FROM student_skill WHERE skill_id = %s) + "
            "(SELECT COUNT(*) FROM position_skill WHERE skill_id = %s) AS usage_count",
            (skill_id, skill_id),
        )
        if cursor.fetchone()["usage_count"] > 0:
            return jsonify({"error": "Cannot delete a skill that is still in use"}), 409

        cursor.execute("DELETE FROM skill WHERE skill_id = %s", (skill_id,))
        get_db().commit()
        return jsonify({"message": "Skill deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()