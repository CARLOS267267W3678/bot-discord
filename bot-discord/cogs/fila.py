import discord
from discord.ext import commands
from views.fila_view import FilaView


class Fila(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.participantes: list[discord.Member] = []
        self.max_vagas = 50
        self.aberta = True
        self.mensagem_fila: discord.Message | None = None

    def criar_embed(self, guild: discord.Guild):
        embed = discord.Embed(
            title="🔥 The Creative League — FILA OFICIAL",
            description=(
                "🚀 Quer participar desse projeto **INSANO**?\n\n"
                "👉 Clique em **Entrar na fila** abaixo.\n"
                "⚠️ As vagas são limitadas."
            ),
            color=discord.Color.red()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        status = "🟢 ABERTA" if self.aberta else "🔴 FECHADA"

        embed.add_field(name="📌 Status da fila", value=status, inline=False)
        embed.add_field(
            name="👥 Vagas",
            value=f"{len(self.participantes)}/{self.max_vagas}",
            inline=False
        )

        lista = "\n".join(m.mention for m in self.participantes)
        embed.add_field(
            name="📋 Participantes",
            value=lista if lista else "Ninguém ainda",
            inline=False
        )

        embed.set_footer(text="© Todos os direitos reservados • bot")
        return embed

    @commands.command(name="fila")
    async def fila(self, ctx: commands.Context):
        await ctx.message.delete()

        view = FilaView(self)
        embed = self.criar_embed(ctx.guild)

        self.mensagem_fila = await ctx.send(embed=embed, view=view)

    @commands.command(name="fecharfila")
    @commands.has_permissions(administrator=True)
    async def fechar_fila(self, ctx: commands.Context):
        self.aberta = False

        if self.mensagem_fila:
            await self.mensagem_fila.edit(
                embed=self.criar_embed(ctx.guild),
                view=None
            )

        await ctx.message.delete()

    @commands.command(name="abrirfila")
    @commands.has_permissions(administrator=True)
    async def abrir_fila(self, ctx: commands.Context):
        self.aberta = True

        if self.mensagem_fila:
            view = FilaView(self)
            await self.mensagem_fila.edit(
                embed=self.criar_embed(ctx.guild),
                view=view
            )

        await ctx.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Fila(bot))