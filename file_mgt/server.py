"""handles and creates server"""
import asyncio

from executor import Executor
from settings import HOST, PORT, TERMINATION_COMMAND
from globals import users

async def server_handler(reader, writer):
    """handles server using reader and writer objects"""
    ip_addr, _ = writer.get_extra_info('peername')
    print(f'Connected with {ip_addr}')

    executor = Executor()
    while True:
        read_bytes = await reader.read(150)
        command = read_bytes.decode()

        if command == TERMINATION_COMMAND:
            if executor.username:
                users[executor.username]['logged_in'] = False
            break

        output = executor.execute(command)
        writer.write(output.encode())

    print(f'Disconnected from {ip_addr}')
    writer.close()


async def main():
    """creates server and runs it."""
    server = await asyncio.start_server(server_handler, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
