from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Teacher_preference, Teacher_preferenceSchema, PostTeacher_preferenceSchema, SuccessSchema, IDParameter, TeacherIDParameter, DeleteTeacher_preferenceSchema

@app.route('/teacher-preferences/<teacher_id>', methods=['GET'])
def get_pair_teacher_preferences(teacher_id):
    """Discipline API.
    ---
    get:
      description: Get all discipline
      parameters:
      - in: path
        schema: TeacherIDParameter
      responses:
        200:
          description: Return all discipline
          content:
            application/json:
              schema: 
                type: array
                items: SubgroupSchema
      tags:
        - Discipline
    """
    teacher_preference_schema = Teacher_preferenceSchema(many = True)
    req = Teacher_preference.query.filter_by(teacher_id = teacher_id).all()
    output = teacher_preference_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_teacher_preferences)


@app.route('/teacher-preferences/<teacher_id>', methods=['POST'])
def post_pair_teacher_preferences(teacher_id):
    """Discipline API
    ---
    post:
      description: Create a discipline
      parameters:
      - in: path
        schema: TeacherIDParameter
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostTeacher_preferenceSchema
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: If discipline is created
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Discipline
    """
    data = request.get_json(silent=True)
    preference = data['preference']

    teacher_preference = Teacher_preference(preference = preference, teacher_id = teacher_id)
    db.session.add(teacher_preference)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_teacher_preferences)


@app.route('/teacher-preferences', methods=['DELETE'])
def delete_cur_teacher_preferences():
    """Discipline API.
    ---
    delete:
      description: Get discipline by id
      parameters:
      - in: path
        schema: IDParameter
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: DeleteTeacher_preferenceSchema
      responses:
        200:
          description: Return discipline
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Discipline
    """
    data = request.get_json(silent=True)
    teacher_id = data['teacher_id']
    preference_id = data['preference_id']

    teacher_preference = Teacher_preference.query.filter_by(id = preference_id, teacher_id = teacher_id).first()
    db.session.delete(teacher_preference)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_teacher_preferences)