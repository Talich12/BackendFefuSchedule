from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Flow, Group, GroupSchema, PostGroupSchema, SuccessSchema, IDParameter

@app.route('/groups', methods=['GET'])
def get_pair_groups():
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
                items: GroupSchema
      tags:
        - Discipline
    """
    group_schema = GroupSchema(many = True)
    req = Group.query.all()
    output = group_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_groups)


@app.route('/groups', methods=['POST'])
def post_pair_groups():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostGroupSchema
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
    size = data['size']
    flow_id = data['flow_id']

    find_flow = Flow.query.filter_by(id = flow_id).first()
    find_flow.size += size

    group = Group(name = name, size = size, flow_id = flow_id)
    db.session.add(group)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_groups)

@app.route('/groups/<id>', methods=['GET'])
def get_cur_group(id):
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
              schema: GroupSchema
      tags:
        - Discipline
    """
    group_schema = GroupSchema(many = False)

    req = Group.query.filter_by(id = id).first()
    output = group_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_group)


@app.route('/groups/<id>', methods=['POST'])
def edit_cur_group(id):
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
            schema: PostGroupSchema
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
    size = data['size']
    flow_id = data['flow_id']

    changed = False

    group = Group.query.filter_by(id = id).first()

    if flow_id != group.flow_id:
        old_flow = Flow.query.filter_by(id = group.flow_id).first()
        old_flow.size -= group.size
        changed = True

    if changed:
        new_flow = Flow.query.filter_by(id = flow_id).first()
        new_flow.size += size
    else:
        new_flow = Flow.query.filter_by(id = flow_id).first()
        new_flow.size += size - group.size

    group.name = name
    group.size = size
    group.flow_id = flow_id
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_group)

@app.route('/groups/<id>', methods=['DELETE'])
def delete_cur_group(id):
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
    group = Group.query.filter_by(id = id).first()

    find_flow = Flow.query.filter_by(id = group.flow_id).first()
    find_flow.size -= group.size
    db.session.delete(group)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_group)