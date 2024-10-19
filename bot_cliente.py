import discord
from discord.ext import commands
from comandos.manejar_mensaje import manejar_mensaje
from comandos.manejar_variables import manejar_let, manejar_get, limpiar_variables_temporales
from comandos.manejar_condicional import manejar_si
from comandos.manejar_embeds import manejar_embeds  # Importa manejar_embeds
from comandos.manejar_texto_suelto import manejar_texto_suelto

class BotCliente(commands.Bot):
    def __init__(self, command_prefix="!"):
        super().__init__(command_prefix=command_prefix, intents=discord.Intents().all())
        self.commands_data = []  # Aquí almacenaremos los comandos creados
    
    def nuevo_comando(self, nombre, tipo="enviar", codigo=""):
        """
        Crear un nuevo comando dinámico con el nombre, tipo y código proporcionados.
        """
        async def dynamic_command(ctx, *args):
            # 1. Procesar $let para establecer variables temporales
            codigo_procesado = manejar_let(codigo)
            
            # 2. Procesar $get para obtener valores de variables temporales
            codigo_procesado = manejar_get(codigo_procesado)
            
            # 3. Procesar $si para evaluar las condiciones
            codigo_procesado = manejar_si(codigo_procesado)
            
            # 4. Procesar títulos y descripciones para crear embeds
            embeds = manejar_embeds(codigo_procesado)
            
            # 5. Procesar el texto suelto (fuera de las funciones)
            texto_suelto = manejar_texto_suelto(codigo_procesado)
            
            # 6. Enviar los embeds y el texto suelto, si existen
            if tipo == "enviar":
                if texto_suelto:
                    await ctx.send(texto_suelto)
                for embed in embeds:
                    await ctx.send(embed=embed)
            
            # Limpiar las variables temporales después de la ejecución
            limpiar_variables_temporales()

        # Registrar el comando dinámico en el bot
        self.add_command(commands.Command(dynamic_command, name=nombre))
        # Guardar los detalles del comando
        self.commands_data.append({'nombre': nombre, 'tipo': tipo, 'codigo': codigo})
    
    def run(self, token):
        """
        Ejecutar el bot con el token proporcionado.
        """
        super().run(token)
