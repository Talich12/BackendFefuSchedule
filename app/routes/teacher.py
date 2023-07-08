from app import app, db, spec
from flask import jsonify, request
from app.models import Teacher, TeacherSchema, PostTeacherSchema, CurrentTeacherSchema, PreferenceSchema, Teacher_preference, Teacher_discipline, CurrentDisciplineTeacherSchema,  SuccessSchema, IDParameter


@app.route('/teachers', methods=['GET'])
def get_teahers():
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
                items: TeacherSchema
      tags:
        - Teacher
    """
    teacher_shema = TeacherSchema(many = True)
    req = Teacher.query.all()
    output = teacher_shema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_teahers)


@app.route('/teachers', methods=['POST'])
def post_teachers():
    """Create a cute furry animal endpoint.
    ---
    post:
      description: Create a teacher
      requestBody:
        description: Request data for teacher
        required: true
        content:
          application/json:
            schema: PostTeacherSchema
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
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    position = data['position']

    teacher = Teacher(name = name, sername = sername, lastname = lastname, position = position)
    db.session.add(teacher)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_teachers)

@app.route('/teachers/<id>', methods=['GET'])
def get_cur_teacher(id):
    """Teachers API.
    ---
    get:
      description: Get teacher by id
      parameters:
      - in: path
        schema: IDParameter
      responses:
        200:
          description: Return teacher
          content:
            application/json:
              schema: CurrentTeacherSchema
      tags:
        - Teacher
    """
    teacher_schema = CurrentTeacherSchema(many = False)
    preference_schema = PreferenceSchema(many = True)
    discipline_scheam = CurrentDisciplineTeacherSchema(many=True)

    preference = Teacher_preference.query.filter_by(teacher_id = id).all()
    preference = preference_schema.dump(preference)

    discipline = Teacher_discipline.query.filter_by(teacher_id = id).all()
    discipline = discipline_scheam.dump(discipline)

    req = Teacher.query.filter_by(id = id).first()
    output = teacher_schema.dump(req)
    output['preferences'] = preference
    output['disciplines'] = discipline
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_teacher)


@app.route('/teachers/<id>', methods=['POST'])
def edit_cur_teacher(id):
    """Create a cute furry animal endpoint.
    ---
    post:
      description: Create a teacher
      parameters:
      - in: path
        schema: IDParameter
      requestBody:
        description: Request data for teacher
        required: true
        content:
          application/json:
            schema: PostTeacherSchema
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
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    position = data['position']

    teacher = Teacher.query.filter_by(id = id).first()
    teacher.name = name
    teacher.sername = sername
    teacher.lastname = lastname
    teacher.position = position
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_teacher)

@app.route('/teachers/<id>', methods=['DELETE'])
def delete_cur_teacher(id):
    """Teachers API.
    ---
    delete:
      description: Get teacher by id
      parameters:
      - in: path
        schema: IDParameter
      responses:
        200:
          description: Return teacher
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Teacher
    """
    teacher = Teacher.query.filter_by(id = id).first()
    find_teacher_disciplines = Teacher_discipline.query.filter_by(teacher_id = id).all()
    for item in find_teacher_disciplines:
      db.session.delete(item)

    find_teacher_preferences = Teacher_preference.query.filter_by(teacher_id = id).all()
    for item in find_teacher_preferences:
      db.session.delete(item)
    db.session.delete(teacher)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_teacher)