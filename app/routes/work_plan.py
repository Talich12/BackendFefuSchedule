from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Work_plan, WorkPlanSchema, PostWorkPlanSchema, AllWorkPlanSchema, DisciplineSchema, CurrentDisciplineTeacherSchema

@app.route('/work-plan/<subgroup_id>', methods=['GET'])
def get_work_plan(subgroup_id):
    """Discipline API.
    ---
    get:
      description: Get all discipline
      parameters:
      - in: path
        schema: SheduleIDParameter
      responses:
        200:
          description: Return all discipline
          content:
            application/json:
              schema: AllWorkPlanSchema
      tags:
        - Discipline
    """
    output = {}
    schema = CurrentDisciplineTeacherSchema(many = True)

    req = Work_plan.query.filter_by(subgroup_id = subgroup_id).all()
    output["disciplines"] = schema.dump(req)

    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_work_plan)

@app.route('/work-plan', methods=['POST'])
def post_work_plan():
    """Discipline API.
    ---
    post:
      description: Get all discipline
      requestBody:
        description: Request data for teacher
        required: true
        content:
          application/json:
            schema: PostWorkPlanSchema
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
    subgroup_id = data['subgroup_id']
    discipline_id = data['discipline_id']

    work_plan = Work_plan(subgroup_id = subgroup_id, discipline_id = discipline_id)

    db.session.add(work_plan)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_work_plan)

@app.route('/work-plan/<subgroup_id>/discipline/<discipline_id>', methods=['DELETE'])
def delete_work_plan(subgroup_id, discipline_id):
    """Discipline API.
    ---
    get:
      description: Get all discipline
      parameters:
      - in: path
        schema: PostWorkPlanSchema
      responses:
        200:
          description: Return discipline
          content:
            application/json:
              schema: SuccessSchema
      tags:
        - Discipline
    """
    req = Work_plan.query.filter_by(subgroup_id = subgroup_id, discipline_id = discipline_id).first()

    db.session.delete(req)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_work_plan)