import sys
import socket
import itertools
import string


def brutforce_attack(my_socket, buffer_size=1024, num_of_chars=1):
    # print('Try to brutforce the password...')
    chars = string.ascii_lowercase + string.digits
    response = ''
    while response != 'Connection success!':
        for password in itertools.product(chars, repeat=num_of_chars):
            password = ''.join(password)
            my_socket.send(password.encode())

            response = my_socket.recv(buffer_size)
            response = response.decode()

            if response == 'Connection success!':
                print(password)
                return True
        num_of_chars += 1
        if num_of_chars > 6:
            print('Unsuccessful.')
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

        if not brutforce_attack(my_socket):
            print('\nNo password found!')

main()