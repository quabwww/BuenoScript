from bot_cliente import BotCliente


bot = BotCliente(command_prefix="!")

bot.nuevo_comando(nombre="info", 
                  tipo="enviar", 
                  codigo="""$descripcion[Esto es un mensaje de prueba]
                  $let[pene;pene]
                 $imagen[Este es el pie de página $get[pene];1] 
                $miniatura[ssss0;1]""")


bot.run("")
