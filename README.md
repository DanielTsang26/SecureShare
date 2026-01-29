# SecureShare
TCP Server File Transfer System

#  SecureShare: Asynchronous TCP Relay

SecureShare is a lightweight, high-performance file transfer utility built with Python's `asyncio`. It enables secure, cross-network file sharing using a custom relay architecture, bypassing NAT restrictions through TCP tunneling.

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/a9ab30c1-96c2-4ddc-892d-61210488d456" />



---

##  Technical Stack

| Component | Technology |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **Concurrency** | `asyncio` (Non-blocking I/O) |
| **Networking** | Custom TCP Sockets |
| **Framing** | `struct` (C-style Binary Packing) |
| **Tunneling** | `ngrok` (NAT Traversal) |

---

## 📂 Project Structure

A modular, flat-folder structure for easy maintenance and zero-config imports.

* `tcp_server.py` — The "Matchmaker" relay that bridges connections.
* `sender.py` — Client for reading and streaming local files.
* `receiver.py` — Client for receiving and writing files to the Desktop.
* `protocol.py` — The shared logic for binary headers and metadata.

---

## Architecture & Protocol
The system uses a Two-Phase Handshake to ensure data integrity:

Handshake: Clients send a packed binary header:

* Role (1 Byte)

* Pairing Code (6 Bytes)

* Metadata: A 4-byte integer defines the size of the incoming JSON metadata (filename, size).

* Stream: The raw data is piped from the Sender socket to the Receiver socket via the Relay.

----

##  How to Run

### 1. Setup the Relay
Start the server and expose it to the internet via ngrok:
```bash
python tcp_server.py --port 8080
# In a second terminal:
ngrok tcp 8080
```
### 2. Send a File
Use the Forwarding URL and Port provided by ngrok:

```bash
python sender.py "my_video.mp4" 123456 --host 0.tcp.ngrok.io --port 12345
```
3. Receive the File
The receiver just needs the same 6-digit pairing code:

```bash
python receiver.py 123456 --host 0.tcp.ngrok.io --port 12345
```
