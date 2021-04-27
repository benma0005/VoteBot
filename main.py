"""

 * Created by benma05 on 27.04.2021 / 12:11
 * github.com/benma0005
 * © benma05 2021
 
"""
import discord
from discord.ext import commands

token = 'Discord Token'
preifx = '!'
embed_colour = 0x0073b5
embed_error_colour = 0xb50000

client = commands.Bot(command_prefix=preifx)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')


@client.command()
async def vote(ctx, opt=None, *args: str):
    channel: discord.TextChannel = ctx.channel

    async def send_help():
        help_description = 'To create a vote use `{}vote create <title> | <question> | <answer1> | <answer2> | ... | <answer10>`\n' \
                           'You can create a Vote with 2-10 answers!'.format(preifx)
        help_embed = discord.Embed(title='Help', description=help_description, colour=embed_colour)
        await channel.send(embed=help_embed)

    if opt == 'create':
        cnt = ' '.join(args).split('|')

        if len(cnt) <= 1:
            description = 'You need a title, question and at least two answers to create a vote.\nFor help `{}vote help`.'.format(preifx)
            embed = discord.Embed(title='Error', description=description, colour=embed_error_colour)
            await channel.send(embed=embed)
            return

        title = cnt[0]
        question = cnt[1]
        answers = cnt[2:]

        for n, answer in enumerate(answers):
            if answer[0] == ' ':
                answers[n] = answer[1:]
        for n, answer in enumerate(answers):
            if answer[-1] == ' ':
                answers[n] = answer[:-1]

        if len(answers) <= 1:
            description = 'You need at least two answers to create a vote.\nFor help `{}vote help`.'.format(
                preifx)
            embed = discord.Embed(title='Error', description=description, colour=embed_error_colour)
            await channel.send(embed=embed)
            return

        if len(answers) > 10:
            description = 'You can\'t create a vote with more than 10 answers.\nFor help `{}vote help`.'.format(
                preifx)
            embed = discord.Embed(title='Error', description=description, colour=embed_error_colour)
            await channel.send(embed=embed)
            return

        if len(answers) == 2 and answers[0] == 'yes' and answers[1] == 'no':
            reactions = ['✅', '❎']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = question + '\n'

        for i in range(len(answers)):
            description += '\n {} {}'.format(reactions[i], answers[i])
        embed = discord.Embed(title=title, description=description)
        await ctx.message.delete()
        send_message = await channel.send(embed=embed)
        for reaction in reactions[:len(answers)]:
            await send_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(send_message.id))
        embed.colour = embed_colour
        await send_message.edit(embed=embed)
        return

    if opt == 'help':
        await send_help()
        return

    else:
        await send_help()
        return


client.run(token)
