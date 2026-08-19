import socket
import ssl
import re


def putkhanection(IP, port):

    def http_probe():

        s = socket.socket()
        s.settimeout(2)

        try:
            s.connect((IP, port))

            request = f"GET / HTTP/1.1\r\nHost: {IP}\r\nConnection: close\r\n\r\n"

            s.send(request.encode())

            response = s.recv(4096).decode(errors="replace")

            if response.startswith("HTTP/"):

                server = re.findall(r'Server:\s*(.*)', response)

                print(f"    Service: HTTP")

                if server:
                    print(f"    Server: {server[0].strip()}")

                return True

            return False

        except:
            return False

        finally:
            s.close()

    def https_probe():

        s = socket.socket()
        s.settimeout(2)

        try:
            context = ssl.create_default_context()

            s = context.wrap_socket(
                s,
                server_hostname=IP
            )

            s.connect((IP, port))

            request = f"GET / HTTP/1.1\r\nHost: {IP}\r\nConnection: close\r\n\r\n"

            s.send(request.encode())

            response = s.recv(4096).decode(errors="replace")

            if response.startswith("HTTP/"):

                server = re.findall(r'Server:\s*(.*)', response)

                print(f"    Service: HTTPS")

                if server:
                    print(f"    Server: {server[0].strip()}")

                return True

            return False

        except:
            return False

        finally:
            s.close()

    def ssh_probe():

        s = socket.socket()
        s.settimeout(2)

        try:
            s.connect((IP, port))

            response = s.recv(1024).decode(errors="replace")

            if response.startswith("SSH-"):

                print("    Service: SSH")

                print(f"    Banner: {response.strip()}")

                return True

            return False

        except:
            return False

        finally:
            s.close()


    s = socket.socket()
    s.settimeout(0.2)

    try:

        s.connect((IP, port))

        print(f"Port {port}: connection was successful")

    except (ConnectionRefusedError, TimeoutError, OSError):

        s.close()
        return

    finally:
        s.close()


    if http_probe():
        return

    if https_probe():
        return
    if ssh_probe():
        return

    print("    Service: Unknown")


IP = input("Enter IP: ")

for i in range(1, 100):
    putkhanection(IP, i)
