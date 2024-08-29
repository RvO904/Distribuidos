import zmq

import hashlib

import os

import errno

import sys

from time import sleep





def crearCarpetaDescargas():

    try:

        os.mkdir('descargas')

    except OSError as e:

        if e.errno != errno.EEXIST:

            raise



def menu():

    sleep(1)

    print('---------------Bienvenido----------------')

    print('1. Subir Archivo')

    print('2. Bajar Archivo')

    print('3. Ver Archivos del servidor')

    print('4. Salir')

    operacion = input('Que deseas? ')

    return(operacion)



def obtenerHash(filename):

    md5 = hashlib.md5()

    with open(filename, 'rb') as f:

        for byte_block in iter(lambda: f.read(1024*128), b''):

            md5.update(byte_block)

        hash = md5.hexdigest()

    return(md5.hexdigest())



def main():

    

    IP_PROXY = sys.argv[1]

    PUERTO_PROXY = sys.argv[2]



    crearCarpetaDescargas()

    context = zmq.Context()

    socket_proxy = context.socket(zmq.REQ)

    socket_proxy.connect(f'tcp://{IP_PROXY}:{PUERTO_PROXY}')

    print('Conectando al servidor')



    operacion = menu()

    while operacion != '4':

        

        if operacion == '1':

            print('Enviar Archivos')



            file_name = input('Nombre del archivo a subir: ')

            hash = obtenerHash(file_name)

            print(hash)

            socket_proxy.send_multipart([b'verificarArchivo', hash.encode(), file_name.encode()]) 

            respuesta = socket_proxy.recv().decode()



            if respuesta == 'archivoExiste':

                print('El archivo ya se encuentra en el servidor')

            elif respuesta == 'nombreArchivoExiste':

                print('El nombre de archivo ya existe. Por favor cambia el nombre del archivo antes de intentar de nuevo.')

            elif respuesta == 'subidaAceptada':

                print('Subiendo el archivo al servidor...')

                archivo = open(file_name, 'rb')

                cant_lectura = 1024*128  #cantidad de bytes a enviar#

                info = archivo.read(cant_lectura)

                fragmento_actual = 1

                file_name_parts = file_name.split('.')



                while info != b'': #Si no hay informacion a enviar termina el envio

                    file_name_fragmento = file_name_parts[0]+'_'+str(fragmento_actual)



                    socket_proxy.send_multipart(['subirArchivo'.encode(), hash.encode()]) 

                    direccion_server = socket_proxy.recv().decode()



                    print(f'El fragmento {file_name_fragmento} se subira al servidor [{direccion_server}]')

                    

                    socket_server = context.socket(zmq.REQ)

                    socket_server.connect(f'tcp://{direccion_server}')

                    socket_server.send_multipart(['subirArchivo'.encode(), info, file_name_fragmento.encode()])

                    print(socket_server.recv())

                    socket_server.close()

                    

                    info = archivo.read(cant_lectura) 

                    fragmento_actual+=1



                socket_proxy.send_multipart(['exitoSubirArchivo'.encode()]) 

                if socket_proxy.recv().decode() == 'archivoSubidoConExito':

                    print('Exito al subir el archivo al servidor.')

                else:

                    print('Error al subir el archivo.')



                archivo.close()

                

            else:

                print('Error desconocido al subir el archivo.')



            operacion = menu()



        elif operacion == '2':

            print('NOTA: PARA DESCARGAR ARCHIVOS POR FAVOR ASEGURARSE DE QUE EL ARCHIVO NO EXISTA EN EL DIRECTORIO DESCARGAS')

            file_name = input('Nombre del archivo a bajar: ')

            socket_proxy.send_multipart(['bajarArchivo'.encode(), file_name.encode()]) 

            respuesta = socket_proxy.recv_multipart()

            if respuesta[0].decode() == 'archivoNoExiste':

                print('El archivo NO se encuentra en el servidor')

            else:

                ubicacion_archivo = respuesta[1].decode().split()

                hash_archivo = respuesta[0].decode()



                file_name_parts = file_name.split('.')

                fragmento_actual = 1

                for direccion_server in ubicacion_archivo:

                    file_name_fragmento = file_name_parts[0]+'_'+str(fragmento_actual)

                    

                    socket_server = context.socket(zmq.REQ)

                    socket_server.connect(f'tcp://{direccion_server}')

                    socket_server.send_multipart(['bajarArchivo'.encode(), file_name_fragmento.encode()])

                    info = socket_server.recv()

                    socket_server.close()



                    archivo = open(f'descargas/{file_name}', 'ab')

                    archivo.write(info)

                    archivo.close()

                    fragmento_actual +=1



                hash_nuevo = obtenerHash(f'descargas/{file_name}')

                if hash_nuevo == hash_archivo:

                    print('LOS ARCHIVOS SON IGUALES')

                else:

                    print('ERROR: LOS ARCHIVOS NO SON IGUALES')



            operacion = menu()



        elif operacion == '3':

            print('Archivos Disponibles en el servidor:')

            socket_proxy.send_multipart([b'verArchivos']) 

            respuesta = socket_proxy.recv().decode()

            print(respuesta)

            operacion = menu()



        else:

            print('La operacion digitada no existe.')

            operacion = menu()





if __name__ == "__main__":

    main()
