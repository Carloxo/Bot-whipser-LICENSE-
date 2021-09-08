import discord
from discord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix="=", description="Carlo")
bot.remove_command('help')


@bot.command()
async def help(ctx):
	embed = discord.Embed(title="Commande de Whipser", description="Prefix : =", color=0xffffff)
	embed.set_thumbnail(
		url="https://static.wixstatic.com/media/c1a99c_c063e7c1d846465c96d764baafb838a4~mv2.jpg/v1/fill/w_1000,h_840,al_c,q_90,usm_0.66_1.00_0.01/c1a99c_c063e7c1d846465c96d764baafb838a4~mv2.jpg")
	embed.add_field(name="=clear", value="nividick", inline=True)
	embed.add_field(name="=mute", value="=unmute", inline=True)
	embed.add_field(name="=user", value="=info", inline=True)
	embed.add_field(name="=kick", value="=ban", inline=True)
	embed.add_field(name="Bientot", value="Bientot", inline=True)
	embed.add_field(name="Bientot", value="Bientot", inline=True)
	await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members = True)
async def clear(ctx , amount=5):
	await ctx.channel.purge(limit=amount + 1000)
	await ctx.channel.send(f"j'ai suprimer {amount} messages")

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


@bot.command()
@commands.has_permissions(kick_members = True)
async def user(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"informations utilisateur - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Demandé par {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nom:", value=member.display_name)

    embed.add_field(name="Compte créé le:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Date de join:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Rôles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Rôle haut grader:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)


@bot.command()
@commands.has_permissions(ban_members = True)
async def mute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !")


@bot.command()
@commands.has_permissions(ban_members = True)
async def info(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Il manque un argument.")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("Oups vous ne pouvez Utiliser cette commande.")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")


@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

#c'est mon code ( carlo#1930 hé hé hé hé )

@bot.command()
@commands.has_permissions(ban_members = True)
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")


def isOwner(ctx):
	return ctx.message.author.id == 787723436595478549


def Friend(ctx):
	return ctx.message.author.id == 481557920920764446

@bot.command()
@commands.check(Friend)
async def monamibmg(ctx):
	await ctx.send("https://www.meme-arsenal.com/memes/f4c5354f84f1ca3e226fac496d1e0581.jpg")

@bot.command()
@commands.check(isOwner)
async def dit(ctx, *texte):
	await ctx.send(" ".join(texte))


@bot.command()
@commands.check(isOwner)
async def china(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))


@bot.command()
@commands.check(isOwner)
async def fromage(ctx):

    await ctx.channel.send(f"Harold sexy")
    await ctx.channel.send(f"https://hungarytoday.hu/wp-content/uploads/2018/02/18ps27.jpg")

bot.run("ODU3MzczNDkwMTQyNzczMzI5.YNOpSQ.3447AaG4gAkf2DzK73Yj8mgIVm4")