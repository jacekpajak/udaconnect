from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from app.location.models import Location
from app.location.schemas import LocationSchema
from app.location.services import LocationService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("location", description="Connections via geolocation.")  # noqa


@api.route("/locations")
@accepts(schema=LocationSchema)
@responds(schema=LocationSchema)
class LocationResource(Resource):
    """
    REST resource for managing locations.
    """

    def post(self) -> Location:
        """
        Create a new location.

        :return: The newly created location.
        """
        location = LocationService.create(request.get_json())
        return location

    def get(self):
        """
        Get all locations.

        :return: A list of all locations.
        """
        locations = LocationService.retrieve_all()
        return locations


@api.route("/locations/<location_id>")
@responds(schema=LocationSchema)
class LocationResource(Resource):
    """
    REST resource for managing individual locations.
    """

    def get(self, location_id: int) -> Location:
        """
        Get a specific location by ID.

        :param location_id: The ID of the location to retrieve.
        :return: The requested location.
        """
        location = LocationService.retrieve(location_id)
        return location

    def put(self, location_id: int) -> Location:
        """
        Update a specific location by ID.

        :param location_id: The ID of the location to update.
        :return: The updated location.
        """
        location = LocationService.update(location_id, request.get_json())
        return location

    def delete(self, location_id: int) -> None:
        """
        Delete a specific location by ID.

        :param location_id: The ID of the location to delete.
        """
        LocationService.delete(location_id)
