import pandas as pd
import asyncio
import random
import time
import serial_asyncio


def generate_data():
    time.sleep(1)
    # Generar números aleatorios para cada campo
    temperatura = round(random.uniform(20, 30), 2)
    presion = round(random.uniform(900, 1100), 2)
    altitud = round(random.uniform(0, 100), 2)
    acl_x = round(random.uniform(-10, 10), 2)
    acl_y = round(random.uniform(-10, 10), 2)
    acl_z = round(random.uniform(-10, 10), 2)
    giro_x = round(random.uniform(-180, 180), 2)
    giro_y = round(random.uniform(-180, 180), 2)
    giro_z = round(random.uniform(-180, 180), 2)
    velocidad = round(random.uniform(0, 100), 2)
    aceleracion = round(random.uniform(0, 10), 2)
    latitud = round(random.uniform(-90, 90), 6)
    longitud = round(random.uniform(-180, 180), 6)
    alt_gps = round(random.uniform(0, 100), 2)
    tiempo = round(random.uniform(0, 100), 2)
    
    # Devolver lista de datos
    return [temperatura, presion, altitud, acl_x, acl_y, acl_z,
            giro_x, giro_y, giro_z, velocidad, aceleracion,
            latitud, longitud, alt_gps, tiempo]


df = pd.read_csv('C:/Users/jairo/Desktop/InterfazScor/data_Sat.csv')

async def datosGraficar():
    reader, writer = await serial_asyncio.open_serial_connection(url='COM3', baudrate=115200)    
    writer.write(("AT+PARAMETER=7,7,1,4\r\n").encode())
    await writer.drain()
    global df
    while True:
        data = await reader.read(400)
        await asyncio.sleep(1)
        if data:
            #print(data.decode())
            if len(data) > 140 and data.decode().startswith("+RCV=1"):
                datos = data.decode()
                lista = datos.split(',')
                #Altitud,Presion,Temperatura,Velocidad,Aceleracion,Tiempo,AclX,AclY,AclZ,GiroX,GiroY,GiroZ,Lat,Long,Altgps
                conjunto = [{"Temperatura": lista[2], "Presion": lista[3], "Altitud": lista[4],
                                "AclX": lista[5], "AclY": lista[6], "AclZ": lista[7],
                                "GiroX": lista[8], "GiroY": lista[9], "GiroZ": lista[10],
                                "Velocidad": lista[11], "Aceleracion": lista[12],
                                "Lat": lista[13], "Long": lista[14], "Altgps": lista[15],
                                "Tiempo": lista[16]}]
                
                df_conjunto = pd.DataFrame(conjunto)
                df = pd.concat([df, df_conjunto], ignore_index=True)
                df.to_csv('C:/Users/jairo/Desktop/InterfazScor/data_Sat.csv', index=False)
                print(df)
                


# async def datosGraficar():
#     global df
#     while True:
#         data = generate_data()
#         await asyncio.sleep(1)
#         # Procesar y agregar datos al DataFrame
#         conjunto = [{"Temperatura": data[0], "Presion": data[1], "Altitud": data[2],
#                         "AclX": data[3], "AclY": data[4], "AclZ": data[5],
#                         "GiroX": data[6], "GiroY": data[7], "GiroZ": data[8],
#                         "Velocidad": data[9], "Aceleracion": data[10],
#                         "Lat": data[11], "Long": data[12], "Altgps": data[13],
#                         "Tiempo": data[14]}]
#         df_conjunto = pd.DataFrame(conjunto)
#         df = pd.concat([df, df_conjunto], ignore_index=True)
#         df.to_csv('C:/Users/jairo/Desktop/InterfazScor/data_Sat.csv', index=False)
    
        
        
async def main():
    task = asyncio.create_task(datosGraficar())
    await task

asyncio.run(main())

