import discord, os, random, requests, webserver
from discord.ext import commands #soluccion: py -3.11 -m pip install -U discord.py
from bot_logic import gen_pass, imagenes_de_perros, get_duck, videos_choice, buscar_avion
from bs4 import BeautifulSoup # forma correcta de instalar: py -3.11 -m pip install bs4
from urllib.parse import quote

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix= '$' , intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(1258921236688404533)
    if channel:
        await channel.send("El bot está en línea.")

#comandos
@bot.command(name='password')
async def password(ctx):
    await ctx.send(f"Tu contraseña generada es: {gen_pass(16)}")
    
@bot.command(name='sumar')
async def sumar(ctx,a,b):
    response = int(a) + int(b)
    await ctx.send(f"la suma de {a} + {b} es: {response}")

#imagenes de perros aleatorios, (API)
@bot.command(name="perros")
async def duck(ctx):
    image_url = imagenes_de_perros()
    await ctx.send(f"imagenes de perros: {image_url}")

@bot.command(name = "patos")
async def duck(ctx):
    img = get_duck()
    await ctx.send(f"imagenes de patos: {img}")

@bot.command(name='contaminacion_auditiva')
async def videos_de_contaminacion(ctx):
    video = videos_choice()
    await ctx.send(f"aqui hay unos videos que hablan sobre la contaminacion auditiva: {video}")

@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge()
    await ctx.send("Mensajes eliminados", delete_after = 3)

@bot.command()
async def avion(ctx, *, arg):
    try:
        # Llama a la función buscar_avion para obtener el nombre correcto o enlace similar
        avion = buscar_avion(arg)

        # Si buscar_avion devuelve None o un mensaje de error
        if not avion or not avion.startswith("https://wiki.warthunder.com/unit/"):
            await ctx.send("✈️ No se encontró un avión similar. Intenta con otro nombre.")
            return

        # Realiza la solicitud a la URL obtenida
        result = requests.get(avion)
        if result.status_code == 404:
            await ctx.send("✈️ Avión no encontrado.")
            return

        # Analiza el HTML para extraer información del avión
        bs = BeautifulSoup(result.text, "lxml")
        temp = bs.find_all("div", "game-unit_card-info_value")

        # Maneja posibles datos faltantes
        rank = temp[0].text.strip() if len(temp) > 0 else "Desconocido"
        battle_rating = " ".join(temp[1].text.split()) if len(temp) > 1 else "Desconocido"
        nation = temp[4].text.strip() if len(temp) > 4 else "Desconocido"
        unit = temp[5].text.strip() if len(temp) > 5 else "Desconocido"
        operator = temp[6].text.strip() if len(temp) > 6 else "Desconocido"

        # Construye el mensaje de respuesta
        message = f"""
        **Información del avión:** 
        **Rango:** {rank}
        **Battle Rating:** {battle_rating}
        **Nación:** {nation}
        **Unidad:** {unit}
        **País Operador:** {operator}
        """

        # Envía los resultados al canal de Discord
        await ctx.send(f"Imagen del avión: {avion}")
        await ctx.send(message)

    except Exception as e:
        await ctx.send("⚠️ Ocurrió un error al procesar tu solicitud. Inténtalo de nuevo.")
        print("Error:", e)

@avion.error
async def error_type(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Tienes que darme el nombre del avión. Usa: `$avion <nombre>`")


webserver.keep_alive()
bot.run(DISCORD_TOKEN)
