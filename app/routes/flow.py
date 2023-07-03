from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Flow, FlowSchema, PostFlowSchema, SuccessSchema, IDParameter

@app.route('/flows', methods=['GET'])
def get_pair_flows():
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
                items: FlowSchema
      tags:
        - Discipline
    """
    flow_schema = FlowSchema(many = True)
    req = Flow.query.all()
    output = flow_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_flows)


@app.route('/flows', methods=['POST'])
def post_pair_flows():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostFlowSchema
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
    code = data['code']

    flow = Flow(code = code)
    db.session.add(flow)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_flows)

@app.route('/flows/<id>', methods=['GET'])
def get_cur_flow(id):
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
              schema: FlowSchema
      tags:
        - Discipline
    """
    flow_schema = FlowSchema(many = False)

    req = Flow.query.filter_by(id = id).first()
    output = flow_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_flow)


@app.route('/flows/<id>', methods=['POST'])
def edit_cur_flow(id):
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
            schema: PostFlowSchema
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
    code = data['code']

    flow = Flow.query.filter_by(id = id).first()
    flow.code = code
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_flow)

@app.route('/flows/<id>', methods=['DELETE'])
def delete_cur_flow(id):
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
    flow = Flow.query.filter_by(id = id).first()
    db.session.delete(flow)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_flow)