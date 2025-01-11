import re
import asyncio
import random
from telethon import TelegramClient, events

# Credenciales de la API de Telegram
api_id = 28134569
api_hash = 'c96cb975695fdc8dbefdef68c5d50779'

# Crear el cliente de Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Expresión regular para detectar los números en el formato especificado
cc_regex = re.compile(r'\d{16}\|\d{2}\|\d{4}\|\d{3}')

# Lista de alias permitidos
allowed_aliases = ['Netfliut', 'Remchkbot']

# Variable global para el prefijo actual y para controlar el estado del bot
current_prefix = "/os"
is_running = True  # Controla si el bot debe continuar procesando

@client.on(events.NewMessage)
async def handler(event):
    global current_prefix, is_running  # Usamos las variables globales

    # Obtener información completa del remitente
    sender = await event.get_sender()

    # Verificar si el mensaje proviene de un chat privado y de un alias permitido
    if event.is_private and sender.username in allowed_aliases:
        # Comando para detener el proceso
        if event.raw_text.strip() == ".cmds":
            is_running = False
            print("🚫 Proceso detenido. Escuchando nuevos mensajes...")  # Log solo en consola
            return  # Detenemos cualquier acción en curso

        # Cambiar el prefijo si el mensaje es un comando (empieza con '/')
        if event.raw_text.startswith("/"):
            new_prefix = event.raw_text.strip()  # Quitar espacios en blanco
            if len(new_prefix) > 1:  # Asegurar que no sea solo "/"
                current_prefix = new_prefix
                print(f"Prefijo actualizado a: {current_prefix}")  # Log solo en consola
                return  # Salir después de cambiar el prefijo

        # Verificar si el mensaje contiene "CC Generator"
        if "CC Generator" in event.raw_text:
            # Reactivar el bot antes de procesar si estaba detenido
            is_running = True

            # Extraer las líneas que coincidan con el formato
            cc_lines = cc_regex.findall(event.raw_text)

            # Enviar cada línea con el prefijo actual
            for cc in cc_lines:
                if not is_running:  # Verificar si el bot fue detenido
                    print("Proceso interrumpido. Deteniendo el envío.")
                    break

                await event.respond(f"{current_prefix} {cc}")  # Enviar mensaje
                print(f"Enviado: {current_prefix} {cc}")  # Log para verificar en consola

                # Generar un intervalo aleatorio entre 30 y 60 segundos
                random_interval = random.randint(30, 60)
                print(f"Esperando {random_interval} segundos antes del próximo mensaje...")
                await asyncio.sleep(random_interval)  # Esperar el tiempo aleatorio

            # Mensaje final después de procesar las líneas
            if is_running:
                print("Terminó de procesar las líneas. Esperando otro mensaje.")

async def main():
    print("Bot iniciado. Escuchando mensajes...")
    await client.start()
    await client.run_until_disconnected()

# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())
