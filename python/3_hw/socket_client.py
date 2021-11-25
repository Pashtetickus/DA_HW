import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
        except socket.error as err:
            raise ClientError(err)

    def put(self, metric_key, metric_value, timestamp=None):
        timestamp = str(timestamp or int(time.time()))
        data_to_send = f'put {metric_key} {metric_value} {timestamp}\n'.encode()

        try:
            self.sock.sendall(data_to_send)
            response = self.sock.recv(1024)
            if b'ok' not in response:
                raise ClientError(response)
        except Exception:
            raise ClientError

    def get(self, key):
        response_dict = {}
        data_to_send = f'get {key}\n'.encode()

        try:
            self.sock.sendall(data_to_send)
            response = self.sock.recv(1024)

            result, data = response.decode().split('\n', 1)
            if 'ok' not in result:
                raise ClientError(response.decode())

            data = data.strip().split('\n')
            for row in data:
                metric_key, metric_value, metric_timestamp = row.split(' ')
                metric_list = response_dict.get(metric_key, [])
                metric_list.append((int(metric_timestamp), float(metric_value)))
                response_dict.update({metric_key: sorted(metric_list)})

            return response_dict

        except Exception as err:
            raise ClientError(err)


if __name__ == '__main__':
    client = Client('127.0.0.1', 8888, timeout=15)
    client.put('palm.cpu', 0.5, timestamp=123456789)
    print(client.get('*'))
