from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Flow, Group, Subgroup, GroupSchema, PostGroupSchema, SuccessSchema, IDParameter, SubgroupSchema, FlowIDParameter, DeleteGroupSchema

@app.route('/groups/<flow_id>', methods=['GET'])
def get_pair_groups(flow_id):
    """Discipline API.
    ---
    get:
      description: Get all discipline
      parameters:
      - in: path
        schema: FlowIDParameter
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
    req = Group.query.filter_by(flow_id = flow_id).all()
    output = group_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_groups)


@app.route('/groups/<flow_id>', methods=['POST'])
def post_pair_groups(flow_id):
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        parameters:
        - in: path
          schema: FlowIDParameter
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

    group = Group(name = name, flow_id = flow_id)
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
    subgroup_schema = SubgroupSchema(many = True)

    req = Group.query.filter_by(id = id).first()

    find_subgroups = Subgroup.query.filter_by(group_id = id).all()
    find_subgroups = subgroup_schema.dump(find_subgroups)

    output = group_schema.dump(req)
    output['subgroups'] = find_subgroups
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_group)



@app.route('/groups', methods=['DELETE'])
def delete_cur_group():
    """Discipline API.
    ---
    delete:
      description: Get discipline by id
      requestBody:
        description: Request data for auditorium
        required: true
        content:
          application/json:
            schema: DeleteGroupSchema
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
    flow_id = data['flow_id']
    group_id = data['group_id']

    group = Group.query.filter_by(flow_id = flow_id, id = group_id).first()

    find_subgroups = Subgroup.query.filter_by(group_id = group.id).all()
    for subgroup in find_subgroups:
        db.session.delete(subgroup)

    find_flow = Flow.query.filter_by(id = group.flow_id).first()
    find_flow.size -= group.size
    db.session.delete(group)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_group)