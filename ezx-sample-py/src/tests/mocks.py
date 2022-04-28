from iserver.EzxMsg import EzxMsg
from iserver.net import ApiClient
from tests import test_data_factory

class MockClient(ApiClient):
    def __init__(self):
        super().__init__(test_data_factory.create_connection_info())
        self.sent = []

    def send_message(self, api_msg_object:EzxMsg):
        self.sent.append(api_msg_object)
        
    def first(self):
        if len(self.sent) > 0:
            return self.sent[0]
        

    def __len__(self):
        return len(self.sent)
