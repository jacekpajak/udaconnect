import grpc
import persons.persons_pb2_grpc as persons_pb2_grpc
import concurrent.futures as futures


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    persons_pb2_grpc.add_PersonsServiceServicer_to_server(persons_pb2_grpc.PersonsService(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()
