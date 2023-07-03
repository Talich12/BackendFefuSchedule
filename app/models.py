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
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    discipline = db.relationship("Discipline", backref="work_plan")
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroup.id'))
    subgroup = db.relationship("Subgroup", backref="work_plan")


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auditorium_number = db.Column(db.Integer, db.ForeignKey('auditorium.number'))
    auditorium = db.relationship("Auditorium", backref="shedule")
    pair_number_id = db.Column(db.Integer, db.ForeignKey('pair_number.id'))
    pair_number = db.relationship("Pair_number", backref="shedule")
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroup.id'))
    subgroup = db.relationship("Subgroup", backref="shedule")
    teacher_discipline_id = db.Column(db.Integer, db.ForeignKey('teacher_discipline.id'))
    teacher_discipline = db.relationship("Teacher_discipline", backref="shedule")
    day_of_week = db.Column(db.Integer) # от 0 до 6


class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(), unique=True)
    type = db.Column(db.String())
    number_of_seats = db.Column(db.Integer)


class Pair_number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String())
    end = db.Column(db.String())


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sername = db.Column(db.String())
    lastname = db.Column(db.String())
    position = db.Column(db.String())


class Teacher_preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.String())
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship("Teacher", backref="preference")

class Teacher_discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship("Teacher", backref="teacher_discipline")
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    discipline = db.relationship("Discipline", backref="teacher_discipline")

class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    reporting_form = db.Column(db.String())


class Subgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship("Group", backref="subgroup")
    size = db.Column(db.Integer)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    flow_id = db.Column(db.Integer, db.ForeignKey('flow.id'))
    flow = db.relationship("Flow", backref="group")
    size = db.Column(db.Integer)


class Flow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    size = db.Column(db.Integer, default=0)

class DisciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Discipline
        load_instance = True

    id = auto_field()
    name = auto_field()
    reporting_form = auto_field()

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
    
    number = auto_field()
    type = auto_field()
    number_of_seats = auto_field()

class Pair_numberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pair_number
        load_instance = True
    
    id = auto_field()
    start = auto_field()
    end = auto_field()

class PostPair_numberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pair_number
        load_instance = True
    
    start = auto_field()
    end = auto_field()

class FlowSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Flow
        load_instance = True

    id = auto_field()
    code = auto_field()
    size = auto_field()
    
class PostFlowSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Flow
        load_instance = True

    code = auto_field()
    size = auto_field()

class GroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field()
    name = auto_field()
    size = auto_field()  
    flow_id = auto_field()

    flow = fields.Nested(FlowSchema)

class PostGroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    name = auto_field()
    size = auto_field()  
    flow_id = auto_field()

    flow = fields.Nested(FlowSchema)  

class SubgroupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subgroup
        load_instance = True

    id = auto_field()
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

    group = fields.Nested(GroupSchema)

class TeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    position = auto_field()

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

    id = auto_field()
    preference = auto_field()
    teacher_id = auto_field()

    teacher = fields.Nested(TeacherSchema)

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

    id = auto_field()
    discipline_id = auto_field()
    teacher_id = auto_field()

    discipline = fields.Nested(DisciplineSchema)
    teacher = fields.Nested(TeacherSchema)

class PostTeacher_disciplineSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher_discipline
        load_instance = True

    discipline_id = auto_field()
    teacher_id = auto_field()

    discipline = fields.Nested(DisciplineSchema)
    teacher = fields.Nested(TeacherSchema)

class SuccessSchema(Schema):
    message = fields.Str(default='Success')

class IDParameter(Schema):
    id = fields.Int()