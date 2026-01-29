import struct
import json
from utils import HEADER_FORMAT, ROLE_SENDER, ROLE_RECEIVER, PROTOCOL_VERSION,HEADER_SIZE

class Protocol:
    def __init__(self):
        self.header_format = HEADER_FORMAT
        self.header_size = HEADER_SIZE
        self.role_sender = ROLE_SENDER
        self.role_receiver = ROLE_RECEIVER
        self.protocol_receiver = PROTOCOL_VERSION

    def pack_header(self,role: int, code: str) -> bytes:
        if len(code) != 6:
            raise ValueError("Transfer code must be exactly 6 character length.")

        return struct.pack(self.header_format,
                       self.protocol_receiver,
                       role,
                       len(code),
                       code.encode('ascii'),
                       0x00
                       )

    def unpack_header(self,data:bytes) -> dict:
        version, role, code_len, code_bytes, reserved = struct.unpack(
            HEADER_FORMAT,
            data
            )

        code = code_bytes.decode('ascii').strip('\x00')

        return {
        "version": version,
        "role": role,
        "code": code
        }

    def pack_metadata(self, filename:str, filesize:int) -> bytes:
        metadata_dict = {
            "filename": filename,
            "filesize": filesize
        }

        metadata_bytes = json.dumps(metadata_dict).encode('utf-8')
        length_prefix = struct.pack("!I", len(metadata_bytes))
    
        return length_prefix + metadata_bytes
    
    def unpack_metadata_length(self, length_bytes: bytes)-> int:
        return struct.unpack("!I", length_bytes)[0]

        





