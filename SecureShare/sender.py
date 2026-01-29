import asyncio
import argparse
from pathlib import Path
from protocol import Protocol

class Sender:
    async def start_sender(self,file_path_str: str, host: str, port: int, code: str):
              proto = Protocol()
              path = Path(file_path_str)

              if not path.exists():
                     print(f"Error: File {file_path_str} was not found.")
                     return
              
              reader, writer = await asyncio.open_connection(host,port)

              try:
                     header = proto.pack_header(proto.role_sender, code)
                     writer.write(header)
                     await writer.drain()

                     metadata_pack = proto.pack_metadata(path.name, path.stat().st_size)
                     print(f"Sending metadata for :{path.name} {path.stat().st_size} bytes)")
                     writer.write(metadata_pack)
                     await writer.drain()

                     CHUNK_SIZE = 65536
                     with open(path, "rb") as f:
                            while True:
                                   chunk = f.read(CHUNK_SIZE)
                                   if not chunk:
                                     break
                                   writer.write(chunk)

                                   await writer.drain()

                     print("File sent successfully!")

              except Exception as e:
                     print(f"Sender Error: {e}")
              finally:
                     writer.close()


   
      
                     