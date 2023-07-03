from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Teacher_preference, Teacher_preferenceSchema, PostTeacher_preferenceSchema, SuccessSchema, IDParameter

@app.route('/teacher-preferences', methods=['GET'])
def get_pair_teacher_preferences():
    """Discipline API.
    ---
    get:
      description: Get all discipline
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
    req = Teacher_preference.query.all()
    output = teacher_preference_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_teacher_preferences)


@app.route('/teacher-preferences', methods=['POST'])
def post_pair_teacher_preferences():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostSubgroupSchema
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
    teacher_id = data['teacher_id']

    teacher_preference = Teacher_preference(preference = preference, teacher_id = teacher_id)
    db.session.add(teacher_preference)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_teacher_preferences)

@app.route('/teacher-preferences/<id>', methods=['GET'])
def get_cur_teacher_preferences(id):
    """Discipline API.
    ---
    get:
      description: Get discipline by id
      parameters:
      - in: path
        schema: IDParameter
      responses:
        200:
          description: Return discipline
          content:
            application/json:
              schema: SubgroupSchema
      tags:
        - Discipline
    """
    teacher_preference_schema = Teacher_preferenceSchema(many = False)

    req = Teacher_preference.query.filter_by(id = id).first()
    output = teacher_preference_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_teacher_preferences)


@app.route('/teacher-preferences/<id>', methods=['POST'])
def edit_cur_teacher_preferences(id):
    """Discipline API.
    ---
    post:
      description: Edit a auditorium
      parameters:
      - in: path
        schema: IDParameter
      requestBody:
        description: Request data for auditorium
        required: true
        content:
          application/json:
            schema: PostSubgroupSchema
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: If discipline is edited
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Discipline
    """
    data = request.get_json(silent=True)
    preference = data['preference']
    teacher_id = data['teacher_id']

    teacher_preference = Teacher_preference.query.filter_by(id = id).first()
    teacher_preference.preference = preference
    teacher_preference.teacher_id = teacher_id
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_teacher_preferences)

@app.route('/teacher-preferences/<id>', methods=['DELETE'])
def delete_cur_teacher_preferences(id):
    """Discipline API.
    ---
    delete:
      description: Get discipline by id
      parameters:
      - in: path
        schema: IDParameter
      responses:
        200:
          description: Return discipline
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Discipline
    """
    teacher_preference = Teacher_preference.query.filter_by(id = id).first()
    db.session.delete(teacher_preference)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_teacher_preferences)