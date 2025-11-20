import grpc
import model.api.schedule_pb2
import model.api.schedule_pb2_grpc


class ScheduleApiWrapper:
    
    def __init__(self, api_url: str):
        self.api_url : str = api_url

    def get_schedule_by_date(self, _date):
        with grpc.insecure_channel(self.api_url) as channel:
            stub = model.api.schedule_pb2_grpc.ScheduleStub(channel)
            schedule = model.api.schedule_pb2.Date(date=_date)
            result, call = stub.get_schedule_bydate.with_call(schedule)
        channel.close()
        return result, call.code()
