from app.models.user import User
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.quiz import Quiz
from app import db
from app.models.question import Question
from flask import request

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

@admin_bp.route("/admin/add-subject", methods=["POST", "OPTIONS"])
@jwt_required()
def add_subject():
    print("Adding subject")
    if request.method == "OPTIONS":
        # Handle preflight CORS request
        return jsonify({"msg": "CORS preflight passed"}), 200

    # POST request continues with authentication
    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request()

    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    # print("Received data:", data)
    subject_name = data.get("subjectName")
    chapters_data = data.get("chapters", [])

    if not subject_name or not chapters_data:
        return jsonify({"msg": "Invalid input"}), 400

    # Create subject
    new_subject = Subject(name=subject_name, description=f"{subject_name} subject")
    db.session.add(new_subject)
    db.session.flush()  # Get subject.id before commit

    for chapter in chapters_data:
        chapter_name = chapter.get("chapterName")
        quiz_name = chapter.get("quizName")
        quiz_duration = chapter.get("quizDuration")
        questions = chapter.get("questions", [])

        if not chapter_name or not quiz_name or not quiz_duration or not questions:
            continue  # Skip invalid entries

        new_chapter = Chapter(name=chapter_name, description="", subject_id=new_subject.id)
        db.session.add(new_chapter)
        db.session.flush()

        new_quiz = Quiz(
            chapter_id=new_chapter.id,
            date_of_quiz=None,
            time_duration=quiz_duration,
            remarks=quiz_name
        )
        db.session.add(new_quiz)
        db.session.flush()

        for q in questions:
            question = Question(
                quiz_id=new_quiz.id,
                question_statement=q.get("statement", ""),
                option1=q.get("option1", ""),
                option2=q.get("option2", ""),
                option3=q.get("option3", ""),
                option4=q.get("option4", ""),
                correct_option=q.get("correct_option", "option1")
            )
            db.session.add(question)

    db.session.commit()
    print("Subject, chapters, quizzes, and questions added successfully.")
    return jsonify({"msg": "Subject, chapters, quizzes, and questions added successfully."}), 201

@admin_bp.route("/admin/test", methods=["GET"])
@jwt_required()
def test_route():
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403
    print("Test route hit")
    return jsonify({"msg": "It works!"})

@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def get_users():
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "qualification": user.qualification,
            "dob": user.dob if user.dob else None
        } for user in users
    ])


@admin_bp.route("/admin/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    if not is_admin():
        return jsonify({"msg": "Unauthorized"}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": f"User {user_id} deleted successfully."}), 200