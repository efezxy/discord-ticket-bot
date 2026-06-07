import discord
from discord.ext import commands
from discord import ui
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Ticket açma butonu
class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Ticket Aç", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: ui.Button):
        """Ticket açma butonu"""
        guild = interaction.guild
        user = interaction.user
        
        # Daha önce açık ticket'ı var mı kontrol et
        for channel in guild.text_channels:
            if channel.topic and f"user_id: {user.id}" in channel.topic:
                await interaction.response.send_message(
                    "❌ Zaten açık bir ticket'ınız var!",
                    ephemeral=True
                )
                return
        
        # Yetkili rolü ayarla (Admin veya support gibi)
        admin_role = discord.utils.get(guild.roles, name="Admin")
        support_role = discord.utils.get(guild.roles, name="Support")
        
        # Kanal oluştur
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites,
            topic=f"user_id: {user.id}"
        )
        
        # Ticket kapatma mesajı gönder
        embed = discord.Embed(
            title="🎫 Ticket Açıldı",
            description=f"Merhaba {user.mention}! Ticket'ınız başarıyla açıldı.\n\nYetkili bir kişi kısa sürede sizinle iletişime geçecektir.",
            color=discord.Color.green()
        )
        
        await ticket_channel.send(embed=embed, view=CloseTicketView())
        
        await interaction.response.send_message(
            f"✅ Ticket'ınız açıldı! {ticket_channel.mention}",
            ephemeral=True
        )

# Ticket kapatma butonu
class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Ticket Kapat", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: ui.Button):
        """Ticket kapatma butonu"""
        channel = interaction.channel
        
        embed = discord.Embed(
            title="🎫 Ticket Kapatılıyor",
            description="Ticket 5 saniye içinde silinecektir...",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        
        import asyncio
        await asyncio.sleep(5)
        
        try:
            await channel.delete()
        except discord.Forbidden:
            await interaction.followup.send("❌ Kanalı silmek için yeterli iznim yok!")

# Bot komutları
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ticket Sistemi"))

@bot.command(name="ticket_setup")
@commands.has_permissions(administrator=True)
async def ticket_setup(ctx):
    """Ticket mesajını oluştur"""
    embed = discord.Embed(
        title="🎫 Destek Sistemi",
        description="Sorun yaşadığınız zaman aşağıdaki butona basarak ticket açınız.",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed, view=TicketView())
    await ctx.send("✅ Ticket sistemi başarıyla kuruldu!")

# Hata yönetimi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için yeterli izniniz yok!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Eksik parametreler!")
    else:
        await ctx.send(f"❌ Hata: {error}")

bot.run(TOKEN)