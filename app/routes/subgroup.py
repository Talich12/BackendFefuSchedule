from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Flow, Group, Subgroup, SubgroupSchema, PostSubgroupSchema, SuccessSchema, IDParameter, GroupIDParameter, DeleteSubgroupSchema

@app.route('/subgroups/<group_id>', methods=['GET'])
def get_pair_subgroups(group_id):
    """Discipline API.
    ---
    get:
      description: Get all discipline
      parameters:
      - in: path
        schema: GroupIDParameter
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
    subgroup_schema = SubgroupSchema(many = True)
    req = Subgroup.query.filter_by(group_id = group_id).all()
    output = subgroup_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_subgroups)


@app.route('/subgroups/<group_id>', methods=['POST'])
def post_pair_subgroups(group_id):
    """Discipline API
    ---
    post:
      description: Create a discipline
      parameters:
      - in: path
        schema: GroupIDParameter
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
    number = data['number']
    size = data['size']

    find_group = Group.query.filter_by(id = group_id).first()
    find_group.size += size

    find_flow = Flow.query.filter_by(id = find_group.flow_id).first()
    find_flow.size += size

    subgroup = Subgroup(number = number, size = size, group_id = group_id)
    db.session.add(subgroup)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_pair_subgroups)

@app.route('/subgroups/<id>', methods=['GET'])
def get_cur_subgroup(id):
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
    subgroup_schema = SubgroupSchema(many = False)

    req = Subgroup.query.filter_by(id = id).first()
    output = subgroup_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_cur_subgroup)


@app.route('/subgroups/<subgroup_id>/group/<group_id>', methods=['DELETE'])
def delete_cur_subgroup(subgroup_id, group_id):
    """Discipline API.
    ---
    delete:
      description: Get discipline by id
      parameters:
      - in: path
        schema: DeleteSubgroupSchema
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

    subgroup = Subgroup.query.filter_by(id = subgroup_id, group_id = group_id).first() 

    find_group = Group.query.filter_by(id = group_id).first()
    find_group.size -= subgroup.size

    find_flow = Flow.query.filter_by(id = find_group.flow_id).first()
    find_flow.size -= subgroup.size
    
    db.session.delete(subgroup)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_subgroup)