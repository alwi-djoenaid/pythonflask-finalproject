"""
This is the record module and supports all the REST actions for the
director records
"""

from flask import make_response, abort
from config import db
from models import Movie, Director, DirectorSchema

# 7114 id director for test
# 48401 movie id

def read_all():
    """
    This function responds to a request for /api/directors
    with the complete list of directors
    :return: json list of  all directors
    """

    directors = Director.query.order_by(Director.id).limit(20)

    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data

def read_one_by_id(director_id):
    """
    This function responds to a request for /api/directors
    with a record of director filtered by their ID
    :return: json of a director record
    """

    director = (
        Director.query.filter(Director.id == director_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    if director is not None:
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data
    
    else:
        abort(404, f"Director not found for ID: {director_id}")

def read_director_by_name(director_name):
    """
    This function responds to a request for /api/directors/director_name
    with a record of director filtered by their name
    :param director_name:  Director name to be filtered
    :return: json of a director record
    """

    search = "%{}%".format(director_name)

    director = (
        Director.query.filter(Director.name.like(search)).all()
    )

    if director is not None:
        director_schema = DirectorSchema(many=True)
        data = director_schema.dump(director)
        return data
    
    else:
        abort(404, f"Director not found for name: {director_name}")

def create(director):
    """
    This function creates a new director record in the directors structure
    based on the passed in director data
    :param director:  director to create in directors structure
    :return:        201 on success, 409 on director exists
    """

    name = director.get('name')
    gender = director.get('gender')
    uid = director.get('uid')
    department = director.get('department')

    print('#############################')
    print(name, gender, uid, department)

    existingDirector = (
        Director.query.filter(Director.name == name)
        .one_or_none()
    )

    if existingDirector is None:
        schema = DirectorSchema()
        newDirector = schema.load(director, session=db.session)

        db.session.add(newDirector)
        db.session.commit()

        data = schema.dump(newDirector)

        return data, 201

    else:
        abort(409, f"Director {director.name} is already exist")

def update(director_id, director):
    """
    This function updates an existing director in the directors structure
    :param director_id:   Id of the director to update in the directors structure
    :param director:      director to update
    :return:            updated director structure
    """
    name = director.get('name')
    gender = director.get('gender')
    uid = director.get('uid')
    department = director.get('department')

    # print('#############################')
    # print(name, gender, uid, department)

    selectDirector = Director.query.filter(Director.id == director_id).one_or_none()

    if selectDirector is not None:
        schema = DirectorSchema()
        updatedDirector = schema.load(director, session=db.session)

        updatedDirector.id = selectDirector.id

        db.session.merge(updatedDirector)
        db.session.commit()

        data = schema.dump(selectDirector)

        return data, 200

    else:
        abort(404, f"Director not found for ID: {director_id}")

def delete(director_id):
    """
    This function deletes a director from the directors structure
    :param director_id:   Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """

    director = Director.query.filter(Director.id == director_id).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {director.name} has been deleted")

    else:
        abort(404, f"Director not found for ID: {director_id}")

