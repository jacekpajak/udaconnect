import grpc
from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp
import persons_pb2
import persons_pb2_grpc
from datetime import datetime
from app.persons.models import Person, Connection
from app.persons.services import ConnectionService, LocationService, PersonService

class PersonsService(persons_pb2_grpc.PersonsServiceServicer):
    def CreatePerson(self, request, context):
        # Implement the logic to create a person
        try:
            new_person_data = {
                "name": request.name,
                "email": request.email,
                "birthdate": datetime.utcfromtimestamp(request.birthdate.seconds),
            }
            new_person = PersonService.create(new_person_data)
            return persons_pb2.Person(
                id=new_person.id,
                name=new_person.name,
                email=new_person.email,
                birthdate=Timestamp(
                    seconds=int(new_person.birthdate.timestamp())
                ),
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return persons_pb2.Person()

    def RetrieveAllPersons(self, request, context):
        # Implement the logic to retrieve all persons
        try:
            persons = PersonService.retrieve_all()
            for person in persons:
                yield persons_pb2.Person(
                    id=person.id,
                    name=person.name,
                    email=person.email,
                    birthdate=Timestamp(
                        seconds=int(person.birthdate.timestamp())
                    ),
                )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

    def RetrievePerson(self, request, context):
        # Implement the logic to retrieve a person by ID
        try:
            person = PersonService.retrieve(request.id)
            if person:
                return persons_pb2.Person(
                    id=person.id,
                    name=person.name,
                    email=person.email,
                    birthdate=Timestamp(
                        seconds=int(person.birthdate.timestamp())
                    ),
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return persons_pb2.Person()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return persons_pb2.Person()

    def FindConnections(self, request, context):
        # Implement the logic to find connections based on the provided criteria
        try:
            start_date = datetime.utcfromtimestamp(request.start_date.seconds)
            end_date = datetime.utcfromtimestamp(request.end_date.seconds)
            distance = request.distance

            connections = ConnectionService.find_contacts(
                person_id=request.person_id,
                start_date=start_date,
                end_date=end_date,
                meters=distance,
            )

            for connection in connections:
                yield persons_pb2.Connection(
                    id=connection.id,
                    person_id=connection.person_id,
                    date=Timestamp(
                        seconds=int(connection.date.timestamp())
                    ),
                    # Add other fields as needed to match your Connection schema
                )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    persons_pb2_grpc.add_PersonsServiceServicer_to_server(PersonsService(), server)
    server.add_insecure_port('[::]:50051')  # Change the port as needed
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()