import socket
import threading
import os
import mylogging as logging
from utils import response
from kafka import KafkaConsumer
from random import randint

logger = logging.getLogger(__name__)


class RequestHandler(threading.Thread):
    def __init__(self, host: str = '127.0.0.1', port: int = 5001) -> None:
        super(RequestHandler, self).__init__()
        self.port = port
        self.host = host
        self.kafka_servers = ['localhost:9092']
        self.request_timeout_ms = 20000

    def get_trans_id(self, n: int = 10):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def run(self):
        self.start_server()

    def start_server(self):
        logger.debug('Starting server')
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        while True:
            clnt, addr = s.accept()
            new_data = clnt.recv(1024)
            logger.debug(('Received data: ', new_data))
            trans_id = self.get_trans_id()
            topic = f'ASYNC-{trans_id}'
            print(f'Trans ID: {trans_id}, Topic: {topic}')
            consumer = KafkaConsumer(topic, bootstrap_servers=self.kafka_servers, consumer_timeout_ms=self.request_timeout_ms)
            for message in consumer:
                msg = message.value.decode()
                logger.debug(('Callback message: ', msg))
                data: response.Response = response.Response(text=msg)
                logger.debug(('Response: ', data.to_raw()))
                clnt.send(bytes(data.to_raw(), 'utf-8'))
                clnt.close()
                break
            else:
                logger.error(f'Timed out!....: {trans_id}')
                data: response.Response = response.Response(reason='Request timedout', res_code=400, text=f'No response from 3rd party for {self.request_timeout_ms} ms')
                logger.debug(('Response: ', data.to_raw()))
                clnt.send(bytes(data.to_raw(), 'utf-8'))
                clnt.close()


if __name__ == '__main__':
    handler: RequestHandler = RequestHandler()
    handler.start()
    pid = os.getpid()
    try:
        input()
    except KeyboardInterrupt:
        os.kill(pid, 9)
    except:
        os.kill(pid, 9)
