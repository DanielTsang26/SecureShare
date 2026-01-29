import json
import asyncio
import argparse
from protocol import Protocol
from pathlib import Path

class Receiver:
    async def start_receiver(self, host: str, port: int, code: str):
             proto = Protocol()
             download_dir = Path.home() / "Desktop" / "SecureShare_Downloads"
             download_dir.mkdir(parents=True, exist_ok=True)

             reader, writer = await asyncio.open_connection(host,port)

             try:
                    header = proto.pack_header(proto.role_receiver, code)
                    writer.write(header)
                    await writer.drain()
                    print(f"Connected to relay code: {code}. Waiting for Sender...")

                    length_bytes = await reader.readexactly(4)
                    metadata_len = proto.unpack_metadata_length(length_bytes)

                    # Read actual JSON
                    metadata_json_bytes = await reader.readexactly(metadata_len)
                    metadata = json.loads(metadata_json_bytes.decode('utf-8'))

                    filename = Path(metadata['filename']).name
                    filesize = metadata['filesize']

                    save_path = download_dir / filename

                    print(f"Match found! Preparing to receive: {filename} ")
                    print(f"Total size: {filesize} bytes.")

                    with open(save_path,"wb") as f:
                           bytes_received = 0
                           while bytes_received < filesize:
                                  remaining = filesize - bytes_received
                                  chunk = await reader.read(min(65536, remaining))

                                  if not chunk:
                                         break
                                  f.write(chunk)
                                  bytes_received += len(chunk)
                           print(f"\nFile saved to: {save_path}")
                           print(f"{save_path}")

             except Exception as e:
                    print(f"Receiver Error: {e}")
             finally:
                    writer.close()



       


