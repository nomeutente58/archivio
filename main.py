import discord
from discord.ext import commands

# Sostituisci 'YOUR_BOT_TOKEN' con il token del tuo bot
TOKEN = 'MTI1MDczNTgxMzc0NzE1MDg4OA.GaViWW.XC1-8K2SKVCbFAA1JTbfPMQp06_OW3P3WtHvBE'

# Intents sono necessari per accedere a certi eventi e dati
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Prefisso per i comandi del bot
bot = commands.Bot(command_prefix='+', intents=intents)

# Dizionario per memorizzare i vouch per server
vouches = {}

@bot.event
async def on_ready():
    print(f'{bot.user} si è connesso a Discord!')

@bot.command(name='rep', help='Conferma per un utente e prodotto')
async def vouch(ctx, member: discord.Member, *, product: str):
    server_id = ctx.guild.id
    if server_id not in vouches:
        vouches[server_id] = {}
    if member.id not in vouches[server_id]:
        vouches[server_id][member.id] = []
    vouches[server_id][member.id].append(product)
    await ctx.send(
        f'{member.mention} ha ricevuto una conferma per il prodotto "{product}"! Totale conferme: {len(vouches[server_id][member.id])}',
        delete_after=5  # Cancella il messaggio dopo 5 secondi
    )

@bot.command(name='vouches', help='Controlla il numero di conferme e i prodotti di un utente')
async def check_vouches(ctx, member: discord.Member):
    server_id = ctx.guild.id
    products = vouches.get(server_id, {}).get(member.id, [])
    count = len(products)
    product_list = "\n".join(products) if products else "Nessuno"
    await ctx.send(
        f'{member.mention} ha {count} conferme.\nProdotti:\n{product_list}',
        delete_after=10  # Cancella il messaggio dopo 10 secondi
    )

@bot.command(name='reset_vouches', help='Resetta le conferme di un utente (solo Admin)')
@commands.has_permissions(administrator=True)
async def reset_vouches(ctx, member: discord.Member):
    server_id = ctx.guild.id
    if server_id in vouches and member.id in vouches[server_id]:
        vouches[server_id][member.id] = []
    await ctx.send(
        f'Le conferme di {member.mention} sono state resettate.',
        delete_after=5  # Cancella il messaggio dopo 5 secondi
    )

bot.run(TOKEN)
