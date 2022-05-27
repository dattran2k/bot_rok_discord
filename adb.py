from ppadb.client import Client as AdbClient
# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
print(client.version())

# Default is "127.0.0.1" and 5037
device = client.device("127.0.0.1:5615")
# Default is "127.0.0.1" and 5037

def dump_logcat(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode('utf-8'))

    connection.close()
device.shell("logcat", handler=dump_logcat)