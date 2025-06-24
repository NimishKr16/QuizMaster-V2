from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.quiz import Quiz
from app import db
from app.models.question import Question

admin_bp = Blueprint("admin", __name__)

def is_admin():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"

@admin_bp.route("/admin/subjects", methods=["GET"])
@jwt_required()
def get_subjects():
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    subjects = Subject.query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "description": s.description
        } for s in subjects
    ])

@admin_bp.route("/admin/chapters/<int:subject_id>", methods=["GET"])
@jwt_required()
def get_chapters(subject_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "description": c.description
        } for c in chapters
    ])

@admin_bp.route("/admin/quizzes/<int:chapter_id>", methods=["GET"])
@jwt_required()
def get_quizzes(chapter_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return jsonify([
        {
            "id": q.id,
            "date_of_quiz": q.date_of_quiz,
            "time_duration": q.time_duration,
            "remarks": q.remarks
        } for q in quizzes
    ])

@admin_bp.route("/admin/questions/<int:quiz_id>", methods=["GET"])
@jwt_required()
def get_questions(quiz_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([
        {
            "id": q.id,
            "question_statement": q.question_statement,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct_option": q.correct_option
        } for q in questions
    ])


# Route to delete a specific quiz by its ID
@admin_bp.route("/admin/quiz/<int:quiz_id>", methods=["DELETE"])
@jwt_required()
def delete_quiz(quiz_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"msg": f"Quiz {quiz_id} deleted successfully."}), 200

@admin_bp.route('/chapters/by-subject/<int:subject_id>', methods=['GET', 'OPTIONS'])
def get_chapters_by_subject(subject_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([{
        "id": chapter.id,
        "name": chapter.name
    } for chapter in chapters])