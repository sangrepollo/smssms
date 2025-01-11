import re
import asyncio
import random
from telethon import TelegramClient, events

# Credenciales de la API de Telegram
api_id = 10306772
api_hash = '2eb2d4541e00ba2796116dad693a9798'

# Crear el cliente de Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Expresión regular para detectar los números en el formato especificado
cc_regex = re.compile(r'\d{16}\|\d{2}\|\d{4}\|\d{3}')

# Lista de alias permitidos
allowed_aliases = ['Netfliut', 'Yelinety']

# Lista de prefijos rotativos
prefixes = ["/os", "/af", "/su", "/po", "/ze"]

# Variable global para la tarea actual y el estado del bot
current_task = None  # Referencia a la tarea de procesamiento actual
is_running = True    # Controla si el bot debe continuar procesando


async def process_cc_lines(event, cc_lines):
    """
    Procesar y enviar líneas de CC con un prefijo rotativo aleatorio.
    """
    global is_running

    for cc in cc_lines:
        if not is_running:  # Detener el proceso si se interrumpe
            print("🚫 Proceso interrumpido. Deteniendo el envío.")
            break

        # Seleccionar un prefijo aleatorio
        random_prefix = random.choice(prefixes)

        # Enviar el mensaje con el prefijo seleccionado
        await event.respond(f"{random_prefix} {cc}")
        print(f"Enviado: {random_prefix} {cc}")  # Log para verificar en consola

        # Generar un intervalo aleatorio entre 30 y 60 segundos
        random_interval = random.randint(30, 60)
        print(f"Esperando {random_interval} segundos antes del próximo mensaje...")
        await asyncio.sleep(random_interval)

    if is_running:
        print("✅ Terminó de procesar las líneas. Esperando otro mensaje...")


@client.on(events.NewMessage)
async def handler(event):
    global current_task, is_running  # Usamos las variables globales

    # Obtener información completa del remitente
    sender = await event.get_sender()

    # Verificar si el mensaje proviene de un chat privado y de un alias permitido
    if event.is_private and sender.username in allowed_aliases:
        # Comando para detener el proceso
        if event.raw_text.strip() == ".cmds":
            is_running = False  # Marcar que el bot no está procesando
            if current_task and not current_task.done():
                current_task.cancel()  # Cancelar la tarea actual
                print("🚫 Proceso y tareas anteriores detenidos.")
            return  # Detener cualquier acción adicional

        # Verificar si el mensaje contiene "CC Generator"
        if "CC Generator" in event.raw_text:
            # Reactivar el bot antes de procesar si estaba detenido
            is_running = True

            # Extraer las líneas que coincidan con el formato
            cc_lines = cc_regex.findall(event.raw_text)

            # Cancelar cualquier tarea en ejecución antes de comenzar una nueva
            if current_task and not current_task.done():
                current_task.cancel()
                print("⚠️ Tarea anterior cancelada. Iniciando nueva tarea...")

            # Iniciar una nueva tarea para procesar las líneas
            current_task = asyncio.create_task(process_cc_lines(event, cc_lines))


async def main():
    print("🤖 Bot iniciado. Escuchando mensajes...")
    await client.start()
    await client.run_until_disconnected()


# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())
