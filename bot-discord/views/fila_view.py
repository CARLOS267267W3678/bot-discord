import discord


class FilaView(discord.ui.View):
    def __init__(self, fila):
        super().__init__(timeout=None)
        self.fila = fila

    @discord.ui.button(label="Entrar na fila", style=discord.ButtonStyle.success)
    async def entrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.fila.aberta:
            await interaction.response.send_message(
                "❌ A fila está fechada.", ephemeral=True
            )
            return

        if interaction.user in self.fila.participantes:
            await interaction.response.send_message(
                "⚠️ Você já está na fila.", ephemeral=True
            )
            return

        if len(self.fila.participantes) >= self.fila.max_vagas:
            await interaction.response.send_message(
                "🚫 A fila está cheia.", ephemeral=True
            )
            return

        self.fila.participantes.append(interaction.user)

        await interaction.message.edit(
            embed=self.fila.criar_embed(interaction.guild),
            view=self
        )
        await interaction.response.defer()

    @discord.ui.button(label="Sair da fila", style=discord.ButtonStyle.danger)
    async def sair(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.fila.participantes:
            await interaction.response.send_message(
                "❌ Você não está na fila.", ephemeral=True
            )
            return

        self.fila.participantes.remove(interaction.user)

        await interaction.message.edit(
            embed=self.fila.criar_embed(interaction.guild),
            view=self
        )
        await interaction.response.defer()