from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Teacher_discipline, Teacher_disciplineSchema, PostTeacher_disciplineSchema, SuccessSchema, IDParameter


@app.route('/teachers-disciplines', methods=['GET'])
def get_teachers_disciplines():
    """Teachers API.
    ---
    get:
      description: Get all teachers
      responses:
        200:
          description: Return all teachers
          content:
            application/json:
              schema: 
                type: array
                items: Teacher_disciplineSchema
      tags:
        - Teacher
    """
    teacher_discipline_schema = Teacher_disciplineSchema(many = True)
    req = Teacher_discipline.query.all()
    output = teacher_discipline_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_teachers_disciplines)


@app.route('/teachers-disciplines', methods=['POST'])
def post_teachers_disciplines():
    """Create a cute furry animal endpoint.
    ---
    post:
      description: Create a teacher
      requestBody:
        description: Request data for teacher
        required: true
        content:
          application/json:
            schema: PostTeacher_disciplineSchema
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: If pet is created
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Teacher
    """
    data = request.get_json(silent=True)
    teacher_id = data['teacher_id']
    discipline_id = data['discipline_id']
    
    teacher_discipline = Teacher_discipline(teacher_id = teacher_id, discipline_id = discipline_id)
    db.session.add(teacher_discipline)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_teachers_disciplines)


@app.route('/teachers/<teacher_id>/disciplines/<discipline_id>', methods=['DELETE'])
def delete_cur_teachers_discipline(teacher_id, discipline_id):
    """Teachers API.
    ---
    delete:
      description: Get teacher by id
      parameters:
      - in: path
        schema: PostTeacher_disciplineSchema
      responses:
        200:
          description: Return teacher
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Teacher
    """
    teacher_discipline = Teacher_discipline.query.filter_by(teacher_id= teacher_id, discipline_id = discipline_id).first()
    db.session.delete(teacher_discipline)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_teachers_discipline)