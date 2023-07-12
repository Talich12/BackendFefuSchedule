from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Schedule, AllScheduleSchema, DayOfWeekSchema, ScheduleShcema, PostScheduleShcema, SheduleIDParameter, Work_plan, WorkPlanSchema

@app.route('/schedule/<subgroup_id>', methods=['GET'])
def get_schedule(subgroup_id):
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
              schema: 
                type: array
                items: AllScheduleSchema
      tags:
        - Discipline
    """
    even_schedule = []
    odd_schedule = []
    output = {
        "even": {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [],
        },
        "odd":{
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [],
        }
    }
    schedule_schema = ScheduleShcema(many = True)
    work_plan_schema = WorkPlanSchema(many = True)
    disciplines = []
    flag = False

    req = Schedule.query.filter_by(subgroup_id = subgroup_id).all()
    work_plan = Work_plan.query.filter_by(subgroup_id = subgroup_id).all()

    work_plan = work_plan_schema.dump(work_plan)
    schedule = schedule_schema.dump(req)

    print(work_plan)
    print(schedule)

    for discipline in work_plan:
        for pair in schedule:
          if discipline['discipline']['id'] == pair["teacher_discipline"]['discipline']["id"]:
            flag = True
            break
      
        if flag == False:
            disciplines.append(discipline)
        flag = False
          

    for pair in schedule:
        if pair['is_even'] == True:
            even_schedule.append(pair)
        else:
            odd_schedule.append(pair)

    for pair in even_schedule:
        if pair['day_of_week'] == 0:
            output["even"]["monday"].append(pair)
        if pair['day_of_week'] == 1:
            output["even"]["tuesday"].append(pair)
        if pair['day_of_week'] == 2:
            output["even"]["wednesday"].append(pair)
        if pair['day_of_week'] == 3:
            output["even"]["thursday"].append(pair)
        if pair['day_of_week'] == 4:
            output["even"]["friday"].append(pair)
        if pair['day_of_week'] == 5:
            output["even"]["saturday"].append(pair)
        if pair['day_of_week'] == 6:
            output["even"]["sunday"].append(pair)

    for pair in odd_schedule:
        if pair['day_of_week'] == 0:
            output["odd"]["monday"].append(pair)
        if pair['day_of_week'] == 1:
            output["odd"]["tuesday"].append(pair)
        if pair['day_of_week'] == 2:
            output["odd"]["wednesday"].append(pair)
        if pair['day_of_week'] == 3:
            output["odd"]["thursday"].append(pair)
        if pair['day_of_week'] == 4:
            output["odd"]["friday"].append(pair)
        if pair['day_of_week'] == 5:
            output["odd"]["saturday"].append(pair)
        if pair['day_of_week'] == 6:
            output["odd"]["sunday"].append(pair)

    output['disciplines'] = disciplines
    return jsonify(output)

with app.test_request_context():
    spec.path(view=get_schedule)


@app.route('/schedule', methods=['POST'])
def post_schedule():
    """Discipline API
    ---
    post:
      description: Create a discipline
      requestBody:
        description: Request data for discipline
        required: true
        content:
          application/json:
            schema: PostScheduleShcema
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
    auditorium_number = data['auditorium_number']
    pair_number_id = data['pair_number_id']
    subgroup_id = data['subgroup_id']
    teacher_discipline_id = data['teacher_discipline_id']
    day_of_week = data['day_of_week']
    is_even = data['is_even']

    schedule = Schedule(auditorium_number = auditorium_number, pair_number_id = pair_number_id, subgroup_id = subgroup_id,
                        teacher_discipline_id = teacher_discipline_id, day_of_week = day_of_week, is_even = is_even)
    
    db.session.add(schedule)
    db.session.commit()

    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=post_schedule)


@app.route('/schedule/<id>', methods=['DELETE'])
def delete_schedule(id):
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
    schedule = Schedule.query.filter_by(id = id).first()
    db.session.delete(schedule)
    db.session.commit()
    return {"message": "Success"}

with app.test_request_context():
    spec.path(view=delete_schedule)