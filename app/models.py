from app import db, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import fields, auto_field
from marshmallow import Schema, fields
from hashlib import md5
import base64
from datetime import datetime, timedelta
import os
  

class Work_plan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    discipline = db.relationship("Discipline", backref="work_plan")
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroup.id'), nullable=False)
    subgroup = db.relationship("Subgroup", backref="work_plan")
    hour_count = db.Column(db.Integer, nullable=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    auditorium_number = db.Column(db.Integer, db.ForeignKey('auditorium.number'), nullable=False)
    auditorium = db.relationship("Auditorium", backref="shedule")
    pair_number_id = db.Column(db.Integer, db.ForeignKey('pair_number.id'), nullable=False)
    pair_number = db.relationship("Pair_number", backref="shedule")
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroup.id'), nullable=False)
    subgroup = db.relationship("Subgroup", backref="shedule")
    teacher_discipline_id = db.Column(db.Integer, db.ForeignKey('teacher_discipline.id'), nullable=False)
    teacher_discipline = db.relationship("Teacher_discipline", backref="shedule")
    day_of_week = db.Column(db.Integer, nullable=False) # от 0 до 6


class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    number = db.Column(db.String(), unique=True, nullable=False)
    type = db.Column(db.String(), nullable=False)
    number_of_seats = db.Column(db.Integer, nullable=False)


class Pair_number(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    start = db.Column(db.String(), nullable=False)
    end = db.Column(db.String(), nullable=False)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)


class Teacher_preference(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    preference = db.Column(db.String(), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    teacher = db.relationship("Teacher", backref="preference")

class Teacher_discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    teacher = db.relationship("Teacher", backref="teacher_discipline")
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    discipline = db.relationship("Discipline", backref="teacher_discipline")

class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    reporting_form = db.Column(db.String(), nullable=False)


class Subgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    number = db.Column(db.String(), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship("Group", backref="subgroup")
    size = db.Column(db.Integer, nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    flow_id = db.Column(db.Integer, db.ForeignKey('flow.id'), nullable=False)
    flow = db.relationship("Flow", backref="group")
    size = db.Column(db.Integer, default=0, nullable=True)


class Flow(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(), nullable=False)
    size = db.Column(db.Integer, default=0, nullable=True)

class DisciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Discipline
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    reporting_form = auto_field()

class CurrentDisciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Discipline
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    reporting_form = auto_field()

    teachers = fields.List(fields.Nested(lambda: CurrentTeacherDisciplineSchema()))

class PostDisciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Discipline
        load_instance = True

    name = auto_field()
    reporting_form = auto_field()

class AuditoriumSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Auditorium
        load_instance = True
    
    number = auto_field(required=True)
    type = auto_field()
    number_of_seats = auto_field()

class Pair_numberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pair_number
        load_instance = True
    
    id = auto_field(required=True)
    start = auto_field()
    end = auto_field()

class PostPair_numberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pair_number
        load_instance = True
    
    start = auto_field()
    end = auto_field()

class CurrentFlowSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Flow
        load_instance = True

    id = auto_field(required=True)
    code = auto_field()
    size = auto_field()

    groups = fields.List(fields.Nested(lambda: GroupSchema()))

class FlowSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Flow
        load_instance = True

    id = auto_field(required=True)
    code = auto_field()
    size = auto_field()
    
class PostFlowSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Flow
        load_instance = True

    code = auto_field()

class CurrentGroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    size = auto_field()  
    flow_id = auto_field()

    flow = fields.Nested(FlowSchema)

    subgroups =  fields.List(fields.Nested(lambda: SubgroupSchema()))

class GroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    size = auto_field()  
    flow_id = auto_field()

    flow = fields.Nested(FlowSchema)

class PostGroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    name = auto_field() 
    flow_id = auto_field()


class SubgroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subgroup
        load_instance = True

    id = auto_field(required=True)
    number = auto_field()
    size = auto_field()  
    group_id = auto_field()

    group = fields.Nested(GroupSchema)

class PostSubgroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subgroup
        load_instance = True

    number = auto_field()
    size = auto_field()  
    group_id = auto_field()

class TeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    position = auto_field()

class CurrentTeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        load_instance = True

    id = auto_field(required=True)
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    position = auto_field()

    disciplines = fields.List(fields.Nested(lambda: DisciplineSchema()))
    preferences = fields.List(fields.Nested(lambda: PreferenceSchema()))

class PostTeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        load_instance = True

    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    position = auto_field()

class Teacher_preferenceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_preference
        load_instance = True

    id = auto_field(required=True)
    preference = auto_field()
    teacher_id = auto_field()

    teacher = fields.Nested(TeacherSchema)

class PreferenceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_preference
        load_instance = True

    id = auto_field()
    preference = auto_field()

class PostTeacher_preferenceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_preference
        load_instance = True

    preference = auto_field()
    teacher_id = auto_field()

    teacher = fields.Nested(TeacherSchema)

class Teacher_disciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_discipline
        load_instance = True

    id = auto_field(required=True)

    discipline = fields.Nested(DisciplineSchema)
    teacher = fields.Nested(TeacherSchema)

class CurrentDisciplineTeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_discipline
        load_instance = True

    id = fields.Method('get_id')
    name = fields.Method('get_name')
    reporting_form = fields.Method('get_report')

    def get_id(self, obj):
        return obj.discipline.id
    
    def get_name(self, obj):
        return obj.discipline.name

    def get_report(self, obj):
        return obj.discipline.reporting_form

class CurrentTeacherDisciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_discipline
        load_instance = True

    teacher = fields.Nested(TeacherSchema)

class PostTeacher_disciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_discipline
        load_instance = True

    discipline_id = auto_field()
    teacher_id = auto_field()

class SuccessSchema(Schema):
    message = fields.Str(default='Success')

class IDParameter(Schema):
    id = fields.Int()

class NumberParameter(Schema):
    number = fields.String()