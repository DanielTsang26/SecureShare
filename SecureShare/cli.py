import argparse
import asyncio
from sender import Sender
from tcp_server import TCPServer
from receiver import Receiver

async def main():
         parser = argparse.ArgumentParser(description="EncryptShare: All in one file transfer.")
         subparsers = parser.add_subparsers(dest="command", help="Avaiable commands")

         server_parser = subparsers.add_parser("server", help="Start the relay server.")
         server_parser.add_argument("--port", type=int, default=8080)
         
         sender_parser = subparsers.add_parser("send", help="send file.")
         sender_parser.add_argument("file", help="Path to the file you want to send.")
         sender_parser.add_argument("code", help="6-digit transfer code.")
         sender_parser.add_argument("--host", default="127.0.0.1", help ="Relay server IP.")
         sender_parser.add_argument("--port", type=int, default=8080, help="Server port (Assigned by ngrok)")
         
         receiver_parser = subparsers.add_parser("receive", help="receive file.")
         receiver_parser.add_argument("code", help="6-digit transfer code.")
         receiver_parser.add_argument("--host", default="127.0.0.1", help ="(e.g. 0.tcp.ngrok.io)")
         receiver_parser.add_argument("--port", type=int, default=8080, help="Server port(e.g. 12345)")

         args = parser.parse_args()

         if args.command == "server":
              s = TCPServer()
              await s.start()
         elif args.command == "send":
              await Sender().start_sender(args.file, args.host, args.port, args.code)
         elif args.command == "receive":
              await Receiver().start_receiver(args.host,args.port, args.code)
         else:
              parser.print_help()


if __name__ == '__main__':
   
   try: 
       asyncio.run(main())
   except KeyboardInterrupt:
       print("\nServer shutting down.")

