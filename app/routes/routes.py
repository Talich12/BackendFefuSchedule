
import uuid
from app import app, db, spec
from flask import jsonify, request
from marshmallow import Schema, fields
from app.models import Teacher, TeacherSchema, Discipline, DisciplineSchema, Auditorium, AuditoriumSchema, Flow, FlowSchema,\
    Group, GroupSchema, Subgroup, SubgroupSchema, Teacher_preference, Teacher_preferenceSchema, Teacher_discipline, Teacher_disciplineSchema,\
    Pair_number, Pair_numberSchema, PostDisciplineSchema, PostFlowSchema, PostGroupSchema, PostPair_numberSchema, PostSubgroupSchema,\
    PostTeacher_disciplineSchema, PostTeacher_preferenceSchema, PostTeacherSchema

class GistParameter(Schema):
    gist_id = fields.Int()


class GistSchema(Schema):
    id = fields.Int()
    content = fields.Str()

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class PetSchema(Schema):
    categories = fields.List(fields.Nested(CategorySchema))
    name = fields.Str()
    
@app.route("/random")
def random_pet():
    """A cute furry animal endpoint.
    ---
    get:
      description: Get a random pet
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: PetSchema
    """
    # Hardcoded example data
    pet_data = {
        "name": "sample_pet_" + str(uuid.uuid1()),
        "categories": [{"id": 1, "name": "sample_category"}],
    }
    return PetSchema().dump(pet_data)


@app.route("/gists/<gist_id>")
def gist_detail(gist_id):
    """Gist detail view.
    ---
    get:
      description: Get a random pet
      parameters:
      - in: path
        schema: GistParameter
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: GistSchema
    """
    return "details about gist {}".format(gist_id)

@app.route("/swagger")
def swagger():
    return spec.to_dict()
