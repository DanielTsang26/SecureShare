import asyncio
import protocol

class SessionManager:
    def __init__(self):
        self.waiting_sessions = {}
        self.lock = asyncio.Lock()

    async def register_client(self, role, code, reader, writer):
            addr = writer.get_extra_info('peername')

            async with self.lock:
                    if code in self.waiting_sessions:
                        partner_role,p_reader,p_writer, = self.waiting_sessions.pop(code)
                        print(f"[MANAGER] Match found for code {code}. Starting up client.")

                        if role == protocol.ROLE_RECEIVER and partner_role == protocol.ROLE_SENDER:
                          await self.start_data_pipe(p_reader,p_writer,reader, writer)
                        else:
                            await self.start_data_pipe(reader,writer,p_reader,p_writer)
                    else:
                         self.waiting_sessions[code] = (role, reader, writer)
                         print(f"[{addr}] Waiting for partner with code: {code}")
                         pass
                    
    async def wait_for_person(self,code, writer):
               addr = writer.get_extra_info('peername')
               try:
                    await asyncio.sleep(3600)
               except asyncio.CancelledError:
                    print(f" [{addr}]Wait task cancelled. Match found for code {code}")
                    raise
               except Exception as e:
                    print(f"Unexpected error has occurred: {e}")

               finally:
                    async with self.lock:
                         if code in self.waiting_sessions:
                              print(f"[{addr}]Cleaning up session {code} from registry.")
                              del self.waiting_sessions[code]
                


    async def start_data_pipe(self,sender_reader: asyncio.StreamReader, 
                              sender_writer: asyncio.StreamWriter, 
                              receiver_reader: asyncio.StreamReader, 
                              receiver_writer: asyncio.StreamWriter):
    
            sender_addr = sender_writer.get_extra_info('peername')
            receiver_addr = receiver_writer.get_extra_info('peername')
            print(f"[PIPE_LINE] Intiated transfer from {sender_addr} to {receiver_addr}")
            CHUNK_SIZE = 65536

            async def data_pipe():
                try:
                  while True:
                    chunk = await sender_reader.read(CHUNK_SIZE)
                    if not chunk: 
                         break
                    receiver_writer.write(chunk)
                    await receiver_writer.drain()
                except Exception as e:
                    print(f"[PIPE] Error during transfer: {e}")

            pipe_task = asyncio.create_task(data_pipe())
            await pipe_task

            
            sender_writer.close()
            receiver_writer.close()
            await sender_writer.wait_closed()
            await receiver_writer.wait_closed()
            print(f"[PIPE] Transfer concluded: {sender_addr} -> {receiver_addr}")
    
           
