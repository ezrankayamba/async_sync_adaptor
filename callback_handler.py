import socket
import threading
import os
import mylogging as logging
from utils import response, request
from kafka import KafkaProducer

logger = logging.getLogger(__name__)


class CallbackHandler(threading.Thread):
    def __init__(self, host: str = '127.0.0.1', port: int = 5002) -> None:
        super(CallbackHandler, self).__init__()
        self.port = port
        self.host = host

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
            new_data = clnt.recv(1024).decode()
            logger.debug(('Received data: ', new_data))
            req: request.Request = request.Request()
            req.from_raw(new_data)
            topic = req.text
            try:
                producer: KafkaProducer = KafkaProducer(bootstrap_servers=['localhost:9092'])
                producer.send(topic, b'Callback here')
                data: response.Response = response.Response(text='Callback processed successfully')
                logger.debug(('Response: ', data.to_raw()))
                clnt.send(bytes(data.to_raw(), 'utf-8'))
                clnt.close()
            except Exception as ex:
                data: response.Response = response.Response(res_code=400, reason='Bad Request', text=f'Error handling callback: {ex}')
                logger.debug(('Response: ', data.to_raw()))
                clnt.send(bytes(data.to_raw(), 'utf-8'))
                clnt.close()


if __name__ == '__main__':
    handler: CallbackHandler = CallbackHandler()
    handler.start()
    pid = os.getpid()
    try:
        input()
    except KeyboardInterrupt:
        os.kill(pid, 9)
    except:
        os.kill(pid, 9)
