from app.persons.models import Connection, Location, Person  # noqa
from app.persons.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.persons.controllers import api as persons_api

    api.add_namespace(persons_api, path=f"/{root}")
