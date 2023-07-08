from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Discipline, DisciplineSchema, CurrentDisciplineSchema, PostDisciplineSchema,\
    Teacher_discipline, CurrentTeacherDisciplineSchema, SuccessSchema, IDParameter, Teacher_discipline

@app.route('/disciplines', methods=['GET'])
def get_disciplines():
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
                items: DisciplineSchema
      tags:
        - Discipline
    """
    discipline_schema = DisciplineSchema(many = True)
    req = Discipline.query.all()
    output = discipline_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_disciplines)


@app.route('/disciplines', methods=['POST'])
def post_disciplines():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostDisciplineSchema
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
    name = data['name']
    reporting_form = data['reporting_form']

    discipline = Discipline(name = name, reporting_form = reporting_form)
    db.session.add(discipline)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_disciplines)

@app.route('/disciplines/<id>', methods=['GET'])
def get_cur_discipline(id):
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
              schema: CurrentDisciplineSchema
      tags:
        - Discipline
    """
    discipline_schema = CurrentDisciplineSchema(many = False)
    teacher_discipline_schema = CurrentTeacherDisciplineSchema(many = True)

    teachers = Teacher_discipline.query.filter_by(discipline_id = id).all()
    teachers = teacher_discipline_schema.dump(teachers)

    req = Discipline.query.filter_by(id = id).first()
    output = discipline_schema.dump(req)
    output['teachers'] = teachers
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_discipline)


@app.route('/disciplines/<id>', methods=['POST'])
def edit_cur_discipline(id):
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
            schema: PostDisciplineSchema
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
    name = data['name']
    reporting_form = data['reporting_form']

    discipline = Discipline.query.filter_by(id = id).first()
    discipline.name = name
    discipline.reporting_form = reporting_form
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_discipline)

@app.route('/disciplines/<id>', methods=['DELETE'])
def delete_cur_discipline(id):
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
        - Auditorium
    """
    discipline = Discipline.query.filter_by(id = id).first()
    find_teacher_disciplines = Teacher_discipline.query.filter_by(discipline_id = id).all()
    for item in find_teacher_disciplines:
        db.session.delete(item)
    db.session.delete(discipline)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_discipline)