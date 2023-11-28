"""Runs and Handles Client Connection"""
import asyncio

from settings import HOST, PORT, TERMINATION_COMMAND, AUTHENTICATION_SUCCESSFUL

async def main():
    """Runs and Handles Client Connection"""
    # Connection
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Authentication
    authenticated = False
    while not authenticated:
        print('1. Login')
        print('2. Register')
        try:
            chosen_option = int(input('Choose 1/2 : '))
            if chosen_option not in [1, 2]:
                raise ValueError('Invalid Choice')

            username = input('Username: ')
            password = input('Passwod: ')

            command = 'login' if chosen_option == 1 else 'register'
            command += f' {username} {password}'

            writer.write(command.encode())
            message_bytes = await reader.read(1000)
            message = message_bytes.decode()
            print(message)
            authenticated = message == AUTHENTICATION_SUCCESSFUL
        except ValueError as error:
            print('Invalid Input ' + str(error))

    # Commands
    while True:
        command = input('$ ')
        writer.write(command.encode())

        if command == TERMINATION_COMMAND:
            break

        output_bytes = await reader.read(1000)
        output = output_bytes.decode()
        print(output)

    writer.close()

if __name__ == '__main__':
    asyncio.run(main())
