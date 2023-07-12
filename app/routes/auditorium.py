from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Auditorium, AuditoriumSchema, SuccessSchema, NumberParameter

@app.route('/auditoriums', methods=['GET'])
def get_auditoriums():
    """Auditoriums API.
    ---
    get:
      description: Get all auditoriums
      responses:
        200:
          description: Return all auditoriums
          content:
            application/json:
              schema: 
                type: array
                items: AuditoriumSchema
      tags:
        - Auditorium
    """
    auditorium_schema = AuditoriumSchema(many = True)
    req = Auditorium.query.all()
    output = auditorium_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_auditoriums)


@app.route('/auditoriums', methods=['POST'])
def post_auditoriums():
    """Auditoriums API
    ---
    post:
      description: Create a auditorium
      requestBody:
        description: Request data for auditorium
        required: true
        content:
          application/json:
            schema: AuditoriumSchema
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: If pet is created
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Auditorium
    """
    data = request.get_json(silent=True)
    number = data['number']
    type = data['type']
    number_of_seats = data['number_of_seats']

    auditorium = Auditorium(number = number, type = type, number_of_seats = number_of_seats)
    db.session.add(auditorium)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_auditoriums)

@app.route('/auditoriums/<number>', methods=['GET'])
def get_cur_auditorium(number):
    """Auditoriums API.
    ---
    get:
      description: Get auditorium by id
      parameters:
      - in: path
        schema: NumberParameter
      responses:
        200:
          description: Return teacher
          content:
            application/json:
              schema: AuditoriumSchema
      tags:
        - Auditorium
    """
    auditorium_schema = AuditoriumSchema(many = False)

    req = Auditorium.query.filter_by(number = number).first()
    output = auditorium_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_auditorium)


@app.route('/auditoriums/<number>', methods=['POST'])
def edit_cur_auditorium(number):
    """Auditoriums API.
    ---
    post:
      description: Edit a auditorium
      parameters:
      - in: path
        schema: NumberParameter
      requestBody:
        description: Request data for auditorium
        required: true
        content:
          application/json:
            schema: AuditoriumSchema
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: If pet is created
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Auditorium
    """
    data = request.get_json(silent=True)
    number_data = data['number_data']
    type = data['type']
    number_of_seats = data['number_of_seats']

    auditorium = Auditorium.query.filter_by(number = number).first()
    auditorium.number_data = number_data
    auditorium.type = type
    auditorium.number_of_seats = number_of_seats
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_auditorium)

@app.route('/auditoriums/<number>', methods=['DELETE'])
def delete_cur_auditorium(number):
    """Auditoriums API.
    ---
    delete:
      description: Get auditorium by id
      parameters:
      - in: path
        schema: NumberParameter
      responses:
        200:
          description: Return teacher
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Auditorium
    """
    auditorium = Auditorium.query.filter_by(number = number).first()
    db.session.delete(auditorium)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_auditorium)