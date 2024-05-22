import pandas as pd
import asyncio
import serial_asyncio
import time
import random


df = pd.read_csv('data_Sat.csv')



async def datosGraficar():
    reader, writer = await serial_asyncio.open_serial_connection(url='COM3', baudrate=115200)
    writer.write(("AT+PARAMETER=7,7,1,4\r\n").encode())
    await writer.drain()
    global df
    try:
        while True:
            data = await reader.read(400)
            await asyncio.sleep(0.8)
            if data:
                if len(data) > 140 and data.decode().startswith("+RCV=1"):
                    datos = data.decode()
                    lista = datos.split(',')
                    # Verificar que la longitud de la lista sea al menos 17
                    if len(lista) >= 17:
                        conjunto = [{"Temperatura": lista[2], "Presion": lista[3], "Altitud": lista[4],
                                     "AclX": lista[5], "AclY": lista[6], "AclZ": lista[7],
                                     "GiroX": lista[8], "GiroY": lista[9], "GiroZ": lista[10],
                                     "Velocidad": lista[11], "Aceleracion": lista[12],
                                     "Lat": lista[13], "Long": lista[14], "Altgps": lista[15],
                                     "Tiempo": lista[16]}]
                        df_conjunto = pd.DataFrame(conjunto)
                        df = pd.concat([df, df_conjunto], ignore_index=True)
                        df.to_csv('data_Sat.csv', index=False)
                        print(df)
                    else:
                        print("Datos incompletos recibidos:", lista)
    except Exception as e:
        print(e)                

    
   
async def main():
    task = asyncio.create_task(datosGraficar())
    await task

asyncio.run(main())

