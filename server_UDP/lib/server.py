import socket
import os
import sys
import json
import queue
import pickle

from threading import Thread, Lock

from lib.request_entities import request_factory as request_factory
from lib import errors_provider as error

from lib.db.db_connection import DataBase

from lib.request_handler import RequestHandler

QUEUE_SIZE = 20
RECEIVE_TIMEOUT = 1


class ReceivePackagesThread(Thread):
    def __init__(self, sock, q, max_package):
        Thread.__init__(self)
        self.__socket = sock
        self.__queue = q
        self.__max_package = max_package
        self.__running = True

    def stop(self):
        self.__running = False

    def run(self):
        self.__socket.settimeout(RECEIVE_TIMEOUT)
        while self.__running:
            self.__get_package()

    def __get_package(self):
        try:
            package = self.__socket.recvfrom(self.__max_package)
            if package:
                self.__put_message(package)
        except socket.timeout:
            pass
        except Exception as e:
            print(f'Error receiving data from clients {e}')

    def __put_message(self, package):
        self.__queue.put(package)


class SendPackagesThread(Thread):
    def __init__(self, sock, q):
        Thread.__init__(self)
        self.__socket = sock
        self.__queue = q
        self.__running = True

    def stop(self):
        self.__running = False

    def run(self):
        while self.__running:
            self.__send_package()

    def __send_package(self):
        while not self.__queue.empty():
            data, address = self.__queue.get()
            self.__socket.sendto(data, address)


class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__IP_ADDRESS = None
        self.__PORT_NUMBER = None
        self.__MAX_HOSTS = None
        self.__MAX_PACKAGE = None
        self.__socket = None
        self.__received_packages = queue.Queue(QUEUE_SIZE)
        self.__packages_to_send = queue.Queue(QUEUE_SIZE)
        self.__connected_clients = []
        self.__config_file = 'config/server_config.json'
        self.__read_config()
        self.__db = DataBase()
        self.__requests_dictionary = request_factory.get_request_dictionary(self.__db)
        self.__bind_socket()
        self.__stopped = False
        self.__stop_signal_lock = Lock()
        self.__client_list_lock = Lock()
        self.__receiving_thread = ReceivePackagesThread(self.__socket, self.__received_packages, self.__MAX_PACKAGE)
        self.__receiving_thread.start()
        self.__sending_thread = SendPackagesThread(self.__socket, self.__packages_to_send)
        self.__sending_thread.start()
        self.__request_handler = RequestHandler()
        print('Server initialized')

    def stop(self):
        self.__stop_signal_lock.acquire()
        self.__stopped = True
        self.__stop_signal_lock.release()

    def run(self):
        while not self.__check_stop():
            self.__check_received_packages()
        self.__close_server()

    def __check_stop(self):
        self.__stop_signal_lock.acquire()
        result = self.__stopped
        self.__stop_signal_lock.release()
        return result

    def __read_config(self):
        if os.path.isfile(self.__config_file):
            with open(self.__config_file) as json_file:
                config_file = json.load(json_file)
                self.__IP_ADDRESS = config_file['ipAddress']
                self.__PORT_NUMBER = config_file['portNumber']
                self.__MAX_HOSTS = config_file['maxHosts']
                self.__MAX_PACKAGE = config_file['maxPackage']
        else:
            self.__handle_config_from_console()

    def __handle_config_from_console(self):
        print('There is no config file for server! Pass me interface, port number and max hosts')
        self.__IP_ADDRESS = input('Enter host IP x.x.x.x: ')
        self.__PORT_NUMBER = int(input('Enter port number: '))
        self.__MAX_HOSTS = int(input('Enter max hosts to connect with: '))

    def __bind_socket(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__socket.bind((self.__IP_ADDRESS, self.__PORT_NUMBER))
        except socket.error as msg:
            print(f'Failed binding specified interface {self.__IP_ADDRESS} and port {self.__PORT_NUMBER} error {msg}')
            sys.exit(error.WRONG_SOCKET)

    def __close_server(self):
        self.__inform_clients_about_close()
        self.__stop_receiving_thread()
        self.__stop_sending_thread()
        self.__db.close_connection()
        print("DEBUG end server thread")

    def __stop_receiving_thread(self):
        print(f'Stopping receiving thread...')
        self.__receiving_thread.stop()
        self.__receiving_thread.join(timeout=8)
        if self.__receiving_thread.isAlive():
            print('Receiving thread cannot be stopped')
        else:
            print("Receiving thread stopped")

    def __stop_sending_thread(self):
        print(f'Stopping sending thread...')
        self.__sending_thread.stop()
        self.__sending_thread.join(timeout=8)
        if self.__sending_thread.isAlive():
            print('Sending thread cannot be stopped')
        else:
            print("Sending thread stopped")

    def __inform_clients_about_close(self):
        self.__client_list_lock.acquire()
        print("Sending information to clients about closing server...")
        for client in self.__connected_clients:
            pass
        self.__client_list_lock.release()

    def __check_received_packages(self):
        if not self.__received_packages.empty():
            message = self.__received_packages.get()
            self.__handle_package(message)

    def __handle_package(self, package):
        print(package)
        data, address = package
        deserialized_data = self.__deserialize_object(package)
        request_type = self.__get_request_type(deserialized_data)
        package_to_send = self.__request_handler.handle_request(request_type, deserialized_data)
        self.__put_package_to_queue((package_to_send, address)),

    def __put_package_to_queue(self, package):
        self.__packages_to_send.put(package)

    @staticmethod
    def __get_request_type(data):
        try:
            return data['requestType']
        except KeyError as e:
            print(f'Exception in parsing json file {e}')
            return None

    @staticmethod
    def __serialize_object(sending_object):
        return pickle.dumps(json.dumps(sending_object))

    @staticmethod
    def __deserialize_object(sending_object):
        return json.loads(pickle.loads(sending_object))
