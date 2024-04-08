import os
import socket
import math
import json

class Function:
    @classmethod
    def function(cls, function: str, params: list):
        if function == "floor":
            return Function.floor(params)
        elif function == "nroot":
            return Function.nroot(params)
        elif function == 'reverse':
            return Function.reverse(params)
        elif function == "validAnagram":
            return Function.validAnagram(params)
        else:
            return Function.sort(params)
        
    @staticmethod
    def floor(params: list) -> float:
        x = params[0]
        return math.ceil(x)
    
    @staticmethod
    def nroot(params: list) -> float:
        x = params[0]
        n = params[1]
        return math.pow(x, 1/n)
    
    @staticmethod
    def reverse(params: list) -> str:
        str = params[0]
        return str[::-1]
    
    @staticmethod
    def validAnagram(params: list) -> bool:
        str1 = params[0]
        str2 = params[1]
        return str1 == str2[::-1]
    
    @staticmethod
    def sort(strList: list[str]) -> list[str]:
        return strList.sort()

class UnixServer:
    def __init__(self, timeout: int=60, buffer: int=1024):
        self.socket = None
        self.timeout = timeout
        self.buffer = buffer
        self.close()

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def delete(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def accept(self, address: str="/tmp/socket.sock", family :int=socket.AF_UNIX, type: int = socket.SOCK_STREAM, proto: int=0):
        self.path = address
        self.delete()
        self.socket = socket.socket(family, type, proto)
        self.socket.bind(self.path)
        print('Wating for connection with client')
        self.socket.listen(1)

        try:
            connection, _ = self.socket.accept()
            print('Successfully connected!!!')

            while True:
                json_recv = connection.recv(self.buffer).decode('utf-8')

                if json_recv:
                    resp = self.resp(json_recv)
                    connection.sendall(resp.encode('utf-8'))
                else:
                    break
        
        except TimeoutError as e:
            print(e)
        except BrokenPipeError as e:
            print(e)
        except ConnectionResetError as e:
            print(e)
        finally:
            print('Closing current connection.')
            self.close()

    def resp(self, json_recv: str):
        print(f'Input json: {json_recv}')

        json_dict = json.loads(json_recv)

        function = json_dict['function']
        params = json_dict['params']
        id = json_dict['id']

        result = Function.function(function, params)
        result_type = str(type(result))
        result_id: int = id

        results = {
            "result": result,
            "result_type": result_type,
            "result_id": result_id
        }

        resp = json.dumps(results)

        return resp
        
        
if __name__ == "__main__":
    server = UnixServer()
    server.accept()