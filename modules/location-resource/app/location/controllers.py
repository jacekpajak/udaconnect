from app.location.models import Location
from app.location.schemas import LocationSchema
from app.location.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("Locations", description="Endpoints for managing locations.")  # noqa

@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        data = request.get_json()
        location: Location = LocationService.create(data)
        return location, 201

    @responds(schema=LocationSchema, many=True)
    def get(self) -> List[Location]:
        locations: List[Location] = LocationService.list()
        return locations, 200

@api.route("/locations/<int:location_id>")
@api.param("location_id", "Unique ID for a given Location")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id: int) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location, 200