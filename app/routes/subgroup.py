from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Subgroup, SubgroupSchema, PostSubgroupSchema, SuccessSchema, IDParameter

@app.route('/subgroups', methods=['GET'])
def get_pair_subgroups():
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
    subgroup_schema = SubgroupSchema(many = True)
    req = Subgroup.query.all()
    output = subgroup_schema.dump(req)
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_pair_subgroups)


@app.route('/subgroups', methods=['POST'])
def post_pair_subgroups():
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
    number = data['number']
    size = data['size']
    group_id = data['group_id']

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


@app.route('/subgroups/<id>', methods=['POST'])
def edit_cur_subgroup(id):
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
    number = data['number']
    size = data['size']
    group_id = data['group_id']

    subgroup = Subgroup.query.filter_by(id = id).first()
    subgroup.number = number
    subgroup.size = size
    subgroup.group_id = group_id
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=edit_cur_subgroup)

@app.route('/subgroups/<id>', methods=['DELETE'])
def delete_cur_subgroup(id):
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
    subgroup = Subgroup.query.filter_by(id = id).first()
    db.session.delete(subgroup)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_cur_subgroup)