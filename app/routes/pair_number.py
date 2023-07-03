from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Pair_number, Pair_numberSchema, PostPair_numberSchema, SuccessSchema, IDParameter

@app.route('/pair-numbers', methods=['GET'])
def get_pair_numbers():
    """Discipline API.
    ---
    get:
      description: Get all discipline
      responses:
        200:
          description: Return all discipline
          content:
            application/json:
              schema: Pair_numberSchema
      tags:
        - Discipline
    """
    pair_number_schema = Pair_numberSchema(many = True)
    req = Pair_number.query.all()
    output = pair_number_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_numbers)


@app.route('/pair-numbers', methods=['POST'])
def post_pair_numbers():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostPair_numberSchema
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
    start = data['start']
    end = data['end']

    pair = Pair_number(start = start, end = end)
    db.session.add(pair)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_numbers)

@app.route('/pair-numbers/<id>', methods=['GET'])
def get_cur_pair_number(id):
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
              schema: Pair_numberSchema
      tags:
        - Discipline
    """
    pair_number_schema = Pair_numberSchema(many = False)

    req = Pair_number.query.filter_by(id = id).first()
    output = pair_number_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_pair_number)


@app.route('/pair-numbers/<id>', methods=['POST'])
def edit_cur_pair_number(id):
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
            schema: PostPair_numberSchema
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
    start = data['start']
    end = data['end']

    pair = Pair_number.query.filter_by(id = id).first()
    pair.start = start
    pair.end = end
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_pair_number)

@app.route('/pair-numbers/<id>', methods=['DELETE'])
def delete_cur_pair_number(id):
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
    auditorium = Pair_number.query.filter_by(id = id).first()
    db.session.delete(auditorium)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_pair_number)