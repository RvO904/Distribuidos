import xmlrpc.client

# Conectarse al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://127.0.0.1:12345/")

# Llamar a las funciones remotas
result_add = server.add(5, 3)
print("5 + 3 =", result_add)

result_subtract = server.subtract(10, 4)
print("10 - 4 =", result_subtract)