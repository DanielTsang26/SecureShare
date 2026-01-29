import asyncio
import protocol
import session_manager
import ssl
from utils import HOST, PORT



class TCPServer:
    def __init__(self, certifile = None, keyfile = None):
        self.host = HOST
        self.port = PORT
        self.manager = session_manager.SessionManager()
        self.protocol = protocol.Protocol()

        self.ssl_context = None
        if certifile and keyfile:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(certfile = certifile, keyfile = keyfile)
            print("TLS Encryption enabled")




    async def handle_client(self,reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        
            addr = writer.get_extra_info('peername')
            print(f"[{addr}] is connected.")
            try:
                header_bytes = await reader.readexactly(protocol.HEADER_SIZE)
                header_data = self.protocol.unpack_header(header_bytes)

                role = header_data['role']
                code = header_data['code']

                print(f"[{addr}] Protocol Version: {header_data['version']}")
                print(f"[{addr}] Role: {'SENDER' if role == self.protocol.role_sender else ' RECEIVER'}")
                print(f"[{addr}] Code:{code}" )

                role_name = "SENDER" if role == self.protocol.role_sender else "RECEIVER"

                if role in [self.protocol.role_sender, self.protocol.role_receiver]:
                    print(f"[{addr}] Registering as {role_name}...")
                    await self.manager.register_client(role, code, reader, writer)
                else:
                    print(f"[{addr}] Unknown role.")
                    writer.close()
                    await writer.wait_closed()

            except asyncio.IncompleteReadError:
                print(f"[{addr}] Connection dropped.")
            except Exception as e:
                print(f"[{addr}] Error:{e}")
    
    

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port, ssl=self.ssl_context)
        print(f"Server is listening on {self.host} : {self.port} ...")
        async with server:
            await server.serve_forever()






