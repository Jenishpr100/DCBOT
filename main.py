import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import random


load_dotenv()
token = os.getenv("token")
if token is None:
    raise ValueError("❌ Token not found in .env file")


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True  # Needed for text commands
intents.members = True


prefixes = {}

def get_prefix(bot, message):
    # Return the saved prefix for the guild, or default "!!" if none set
    return prefixes.get(message.guild.id, ">")

bot = commands.Bot(command_prefix=get_prefix, intents=intents)




@bot.tree.command(name="prefix", description="Change the bot's command prefix for this server")
@app_commands.describe(prefix="New prefix to set")
async def prefix_slash(interaction: discord.Interaction, prefix: str):
    guild_id = interaction.guild.id
    prefixes[guild_id] = prefix
    await interaction.response.send_message(f"✅ Prefix changed to `{prefix}` for this server!", ephemeral=False)


@bot.command(name="prefix", help="Change the command prefix for this server")
@commands.has_guild_permissions(administrator=True)  # Only admins can change prefix
async def prefix_cmd(ctx, *, new_prefix: str):
    prefixes[ctx.guild.id] = new_prefix
    await ctx.send(f"✅ Prefix changed to `{new_prefix}` for this server!")









@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    
    try:
        synced = await bot.tree.sync()  # Global sync for slash commands
        print(f"🌐 Globally synced {len(synced)} slash commands ✅")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")



@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Globally synced {len(synced)} slash commands: {[cmd.name for cmd in synced]} ✅")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")










@bot.tree.command(name="raid", description="Send a message multiple times (max 100)")
@app_commands.describe(message="The message to spam", amount="Number of times to send (max 100)")
async def raid_slash(interaction: discord.Interaction, message: str, amount: int):
    if amount > 100:
        await interaction.response.send_message("❌ Amount can't be more than 100!", ephemeral=True)
        return

    await interaction.response.send_message(f"🚀 Raiding with {amount} messages!")

    for _ in range(amount):
        await interaction.channel.send(message)

@bot.command(name="raid")
async def raid(ctx, message: str, amount: int):
    if amount > 100:
        await ctx.send("❌ Amount can't be more than 100!")
        return
    for _ in range(amount):
        await ctx.send(message)










@bot.tree.command(name="kiss", description="Kiss someone")
@app_commands.describe(user="The user you want to kiss")                                #kiss
async def kiss_slash(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** kissed **{user.display_name}** 😘"
    )

@bot.command(name="kiss")
async def kiss(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** kissed **{user.display_name}** 😘")








@bot.tree.command(name="hit", description="Hit another user 👊")
@app_commands.describe(user="The user you want to hit")
async def hit_slash(interaction: discord.Interaction, user: discord.User):              #hit
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** hit **{user.display_name}** 💥"
    )

@bot.command(name="hit")
async def hit(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** hit **{user.display_name}** 💥")








@bot.tree.command(name="hug", description="Hug someone warmly")
@app_commands.describe(user="The user you want to hug")
async def hug_slash(interaction: discord.Interaction, user: discord.User):          #hug
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** hugged **{user.display_name}** 🤗"
    )

@bot.command(name="hug")
async def hug(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** hugged **{user.display_name}** 🤗")








@bot.tree.command(name="kill", description="Eliminate someone dramatically")
@app_commands.describe(user="The user you want to kill")
async def kill_slash(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        # Reply with a private message (ephemeral)
        await interaction.response.send_message("❌ do NOT kill yourself", ephemeral=True)
        return

    # Acknowledge the command silently so Discord doesn't error
    await interaction.response.defer(ephemeral=True)

    # Then send a public message like ctx.send()
    await interaction.channel.send(
        f"**{interaction.user.display_name}** killed **{user.display_name}** 💀☠️"
    )



@bot.command(name="kill")
async def kill(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send("❌ do NOT kill yourself")
        return

    await ctx.send(f"**{ctx.author.display_name}** killed **{user.display_name}** 💀☠️")










@bot.tree.command(name="slap", description="Slap someone randomly")
@app_commands.describe(user="The user you want to slap")
async def slap_slash(interaction: discord.Interaction, user: discord.User):
    slaps = [
        "slapped **{user}** with a fish 🐟",
        "slapped **{user}** into another dimension 🌌",                                 #slap
        "slapped **{user}** using the force 💥",
        "casually slapped **{user}** 😐"
    ]
    msg = random.choice(slaps).format(user=user.display_name)
    await interaction.response.send_message(f"**{interaction.user.display_name}** {msg}")



@bot.command(name="slap")
async def slap(ctx, user: discord.User):
    slaps = [
        f"slapped **{user.display_name}** with a fish 🐟",
        f"slapped **{user.display_name}** into another dimension 🌌",
        f"slapped **{user.display_name}** using the force 💥",
        f"casually slapped **{user.display_name}** 😐"
    ]
    msg = random.choice(slaps)
    await ctx.send(f"**{ctx.author.display_name}** {msg}")









@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip_slash(interaction: discord.Interaction):                              # coinflip
    result = random.choice(["Heads", "Tails"])                  
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** flipped the coin... **{result}**!"
    )

@bot.command(name="coinflip")
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"**{ctx.author.display_name}** flipped the coin... **{result}**!")










@bot.tree.command(name="dice", description="Roll a dice with a custom number of sides")
@app_commands.describe(sides="Number of sides on the dice (must be at least 2)")
async def dice_slash(interaction: discord.Interaction, sides: int):
    if sides < 2:
        await interaction.response.send_message("❌ Dice must have at least 2 sides.", ephemeral=True)      #dice
        return

    result = random.randint(1, sides)
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** rolled a **{result}** on a {sides}-sided die 🎲"
    )

@bot.command(name="dice")
async def dice(ctx, sides: int):
    if sides < 2:
        await ctx.send("❌ Dice must have at least 2 sides.")
        return

    result = random.randint(1, sides)
    await ctx.send(f"**{ctx.author.display_name}** rolled a **{result}** on a {sides}-sided die 🎲")











@bot.tree.command(name="random", description="Get a random number between minimum and maximum")
@app_commands.describe(
    minimum="The lowest number you want",
    maximum="The highest number you want"
)
async def random_slash(interaction: discord.Interaction, minimum: int, maximum: int):
    if maximum < minimum:
        await interaction.response.send_message(                                                        #random
            "❌ Maximum must be greater than or equal to minimum.", ephemeral=True
        )
        return

    result = random.randint(minimum, maximum)
    await interaction.response.send_message(
        f"**{interaction.user.display_name}**, your random number between {minimum} and {maximum} is: **{result}** 🎲"
    )


@bot.command(name="random")
async def random_number(ctx, minimum: int, maximum: int):
    if maximum < minimum:
        await ctx.send("❌ Maximum must be greater than or equal to minimum.")
        return

    result = random.randint(minimum, maximum)
    await ctx.send(f"**{ctx.author.display_name}**, your random number between {minimum} and {maximum} is: **{result}** 🎲")










@bot.tree.command(name="ban", description="Ban a user with a reason")
@app_commands.describe(
    user="The user you want to ban",
    reason="The reason for banning"
)
async def ban_slash(interaction: discord.Interaction, user: discord.User, reason: str):
    # Check if the command user has ban permissions
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don’t have permission to ban members.", ephemeral=True)
        return

    # Check if the bot has ban permissions
    if not interaction.guild.me.guild_permissions.ban_members:                                                      #banning
        await interaction.response.send_message("❌ I don’t have permission to ban members.", ephemeral=True)
        return

    try:
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(
            f"✅ Banned **{user.display_name}** for: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to ban **{user.display_name}**. Error: {e}",
            ephemeral=True
        )


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason: str = "No reason provided"):
    # Check if bot has ban permissions
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("❌ I don’t have permission to ban members.")
        return

    try:
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"✅ Banned **{user.display_name}** for: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to ban **{user.display_name}**. Error: {e}")










@bot.tree.command(name="kick", description="Kick a user with a reason")
@app_commands.describe(
    user="The user you want to kick",
    reason="The reason for kicking"
)
async def kick_slash(interaction: discord.Interaction, user: discord.User, reason: str):
    # Check if the command user has kick permissions
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ You don’t have permission to kick members.", ephemeral=True)
        return

    # Check if the bot has kick permissions
    if not interaction.guild.me.guild_permissions.kick_members:
        await interaction.response.send_message("❌ I don’t have permission to kick members.", ephemeral=True)              #kick
        return

    try:
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(
            f"✅ Kicked **{user.display_name}** for: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to kick **{user.display_name}**. Error: {e}",
            ephemeral=True
        )


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason: str = "No reason provided"):
    # Check if bot has kick permissions
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("❌ I don’t have permission to kick members.")
        return

    try:
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"✅ Kicked **{user.display_name}** for: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to kick **{user.display_name}**. Error: {e}")










from datetime import timedelta

@bot.tree.command(name="mute", description="Timeout (mute) a user for a set duration")
@app_commands.describe(
    user="The user you want to timeout",
    duration="Duration of the timeout in minutes",
    reason="Reason for timeout"
)
async def mute_slash(interaction: discord.Interaction, user: discord.Member, duration: int, reason: str):
    # Permission checks
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don’t have permission to timeout members.", ephemeral=True)
        return

    if not interaction.guild.me.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ I don’t have permission to timeout members.", ephemeral=True)               #mute
        return

    try:
        timeout_duration = timedelta(minutes=duration)
        await user.timeout_for(timeout_duration, reason=reason)
        await interaction.response.send_message(
            f"✅ Timed out **{user.display_name}** for {duration} minutes. Reason: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to timeout **{user.display_name}**. Error: {e}",
            ephemeral=True
        )

from datetime import timedelta

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, user: discord.Member, duration: int, *, reason: str = "No reason provided"):
    if not ctx.guild.me.guild_permissions.moderate_members:
        await ctx.send("❌ I don’t have permission to timeout members.")
        return

    try:
        timeout_duration = timedelta(minutes=duration)
        await user.timeout(timeout_duration, reason=reason)
        await ctx.send(f"✅ Timed out **{user.display_name}** for {duration} minutes. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to timeout **{user.display_name}**. Error: {e}")











@bot.tree.command(name="assign", description="Assign a role to a user")
@app_commands.describe(
    user="The user to assign the role to",
    role="The role you want to assign"
)
async def assign_slash(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    # Check if command user has manage_roles permission
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don’t have permission to manage roles.", ephemeral=True)
        return

    # Check if bot has manage_roles permission
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ I don’t have permission to manage roles.", ephemeral=True)
        return

    # Check role hierarchy
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ I cannot assign a role higher or equal to my highest role.", ephemeral=True)        #role
        return

    if role >= interaction.user.top_role:
        await interaction.response.send_message("❌ You cannot assign a role higher or equal to your highest role.", ephemeral=True)
        return

    try:
        await user.add_roles(role, reason=f"Role assigned by {interaction.user}")
        await interaction.response.send_message(f"✅ Assigned role **{role.name}** to **{user.display_name}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Failed to assign role. Error: {e}", ephemeral=True)


@bot.command(name="assign")
@commands.has_permissions(manage_roles=True)
async def assign(ctx, user: discord.Member, role: discord.Role):
    # Check if bot has manage_roles permission
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send("❌ I don’t have permission to manage roles.")
        return

    # Role hierarchy checks
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ I cannot assign a role higher or equal to my highest role.")
        return

    if role >= ctx.author.top_role:
        await ctx.send("❌ You cannot assign a role higher or equal to your highest role.")
        return

    try:
        await user.add_roles(role, reason=f"Role assigned by {ctx.author}")
        await ctx.send(f"✅ Assigned role **{role.name}** to **{user.display_name}**.")
    except Exception as e:
        await ctx.send(f"❌ Failed to assign role. Error: {e}")










@bot.tree.command(name="demote", description="Remove a role from a user")
@app_commands.describe(
    user="The user to remove the role from",
    role="The role you want to remove"
)
async def demote_slash(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    # Check if command user has manage_roles permission
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don’t have permission to manage roles.", ephemeral=True)
        return

    # Check if bot has manage_roles permission
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ I don’t have permission to manage roles.", ephemeral=True)
        return

    # Check role hierarchy
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ I cannot remove a role higher or equal to my highest role.", ephemeral=True)    #anyyrole
        return

    if role >= interaction.user.top_role:
        await interaction.response.send_message("❌ You cannot remove a role higher or equal to your highest role.", ephemeral=True)
        return

    try:
        await user.remove_roles(role, reason=f"Role removed by {interaction.user}")
        await interaction.response.send_message(f"✅ Removed role **{role.name}** from **{user.display_name}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Failed to remove role. Error: {e}", ephemeral=True)

@bot.command(name="demote")
@commands.has_permissions(manage_roles=True)
async def demote(ctx, user: discord.Member, role: discord.Role):
    # Check if bot has manage_roles permission
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send("❌ I don’t have permission to manage roles.")
        return

    # Role hierarchy checks
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ I cannot remove a role higher or equal to my highest role.")
        return

    if role >= ctx.author.top_role:
        await ctx.send("❌ You cannot remove a role higher or equal to your highest role.")
        return

    try:
        await user.remove_roles(role, reason=f"Role removed by {ctx.author}")
        await ctx.send(f"✅ Removed role **{role.name}** from **{user.display_name}**.")
    except Exception as e:
        await ctx.send(f"❌ Failed to remove role. Error: {e}")










@bot.tree.command(name="unban", description="Unban a user by their ID")
@app_commands.describe(
    user_id="The ID of the user to unban (as a string)",
    reason="Reason for unbanning"
)
async def unban_slash(interaction: discord.Interaction, user_id: str, reason: str):
    # Permission checks
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don’t have permission to unban members.", ephemeral=True)
        return

    if not interaction.guild.me.guild_permissions.ban_members:                                                              #uunban
        await interaction.response.send_message("❌ I don’t have permission to unban members.", ephemeral=True)
        return

    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(
            f"✅ Unbanned **{user}**. Reason: {reason}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to unban user with ID {user_id}. Error: {e}",
            ephemeral=True
        )

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: str, *, reason: str = "No reason provided"):
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("❌ I don’t have permission to unban members.")
        return

    try:
        user = await bot.fetch_user(int(user_id))
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ Unbanned **{user}**. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to unban user with ID {user_id}. Error: {e}")










@bot.tree.command(name="lock", description="Lock the current channel for @everyone")
async def lock_slash(interaction: discord.Interaction):
    channel = interaction.channel
    everyone_role = interaction.guild.default_role

    try:
        await channel.set_permissions(everyone_role, send_messages=False)                                               #lock
        await interaction.response.send_message(f"🔒 Locked {channel.mention} for @everyone", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don’t have permission to lock this channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)


@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    channel = ctx.channel
    everyone_role = ctx.guild.default_role

    try:
        await channel.set_permissions(everyone_role, send_messages=False)
        await ctx.send(f"🔒 Locked {channel.mention} for @everyone")
    except discord.Forbidden:
        await ctx.send("❌ I don’t have permission to lock this channel.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")








@bot.tree.command(name="unlock", description="Unlock the current channel for @everyone")
async def unlock_slash(interaction: discord.Interaction):
    channel = interaction.channel
    everyone_role = interaction.guild.default_role

    try:
        await channel.set_permissions(everyone_role, send_messages=True)                                            #unlock
        await interaction.response.send_message(f"🔓 Unlocked {channel.mention} for @everyone", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don’t have permission to unlock this channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)


@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    channel = ctx.channel
    everyone_role = ctx.guild.default_role

    try:
        await channel.set_permissions(everyone_role, send_messages=True)
        await ctx.send(f"🔓 Unlocked {channel.mention} for @everyone")
    except discord.Forbidden:
        await ctx.send("❌ I don’t have permission to unlock this channel.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")










@bot.tree.command(name="nick", description="Change a user's nickname")
@app_commands.describe(user="The user you want to rename", nickname="The new nickname to give them")
async def nick_slash(interaction: discord.Interaction, user: discord.Member, nickname: str):
    # Check if the bot can actually change this user's nickname
    if interaction.guild.me.top_role <= user.top_role:
        await interaction.response.send_message(
            f"❌ I can't change **{user.display_name}**'s nickname because their role is higher than mine.",
            ephemeral=True
        )                                                                                                           #nickname
        return

    try:
        await user.edit(nick=nickname)
        await interaction.response.send_message(
            f"✅ Changed **{user.display_name}**'s nickname to **{nickname}**!"
        )
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to change nicknames.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Failed to change nickname: `{e}`", ephemeral=True)


@bot.command(name="nick")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, user: discord.Member, *, nickname: str):
    if ctx.guild.me.top_role <= user.top_role:
        await ctx.send(f"❌ I can't change **{user.display_name}**'s nickname because their role is higher than mine.")
        return

    try:
        await user.edit(nick=nickname)
        await ctx.send(f"✅ Changed **{user.display_name}**'s nickname to **{nickname}**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change nicknames.")
    except Exception as e:
        await ctx.send(f"❌ Failed to change nickname: `{e}`")









@bot.tree.command(name="lockall", description="Lock ALL text channels for @everyone")
async def lockall_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🔒 Locking all channels...", ephemeral=True)
    everyone = interaction.guild.default_role
    locked = 0

    for channel in interaction.guild.text_channels:                                                             #loclall
        try:
            await channel.set_permissions(everyone, send_messages=False)
            locked += 1
        except:
            continue

    await interaction.followup.send(f"✅ Locked `{locked}` channels for @everyone.")

@bot.command(name="lockall")
@commands.has_permissions(manage_channels=True)
async def lockall(ctx):
    await ctx.send("🔒 Locking all channels...", delete_after=5)
    everyone = ctx.guild.default_role
    locked = 0

    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(everyone, send_messages=False)
            locked += 1
        except:
            continue

    await ctx.send(f"✅ Locked `{locked}` channels for @everyone.")









@bot.tree.command(name="unlockall", description="Unlock ALL text channels for @everyone")
async def unlockall_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🔓 Unlocking all channels...", ephemeral=True)
    everyone = interaction.guild.default_role
    unlocked = 0

    for channel in interaction.guild.text_channels:                                             #unlockall
        try:
            await channel.set_permissions(everyone, send_messages=True)
            unlocked += 1
        except:
            continue

    await interaction.followup.send(f"✅ Unlocked `{unlocked}` channels for @everyone.")

@bot.command(name="unlockall")
@commands.has_permissions(manage_channels=True)
async def unlockall(ctx):
    await ctx.send("🔓 Unlocking all channels...", delete_after=5)
    everyone = ctx.guild.default_role
    unlocked = 0

    for channel in ctx.guild.text_channels:
        try:
            await channel.set_permissions(everyone, send_messages=True)
            unlocked += 1
        except:
            continue

    await ctx.send(f"✅ Unlocked `{unlocked}` channels for @everyone.")







@bot.tree.command(name="purge", description="Delete a number of messages from the current channel")
@app_commands.describe(amount="Number of messages to delete (max 100)")
async def purge_slash(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Amount must be between 1 and 100.", ephemeral=True)             #purge
        return

    await interaction.response.defer(ephemeral=True)  # avoid timeout
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Purged {len(deleted)} messages from {interaction.channel.mention}")

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount < 1 or amount > 100:
        await ctx.send("❌ Amount must be between 1 and 100.")
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Purged {len(deleted)} messages from {ctx.channel.mention}", delete_after=5)









from discord import Colour

color_names = {
    "red": 0xFF0000,
    "blue": 0x0000FF,
    "green": 0x00FF00,
    "purple": 0x800080,
    "yellow": 0xFFFF00,
    "orange": 0xFFA500,
    "pink": 0xFFC0CB,
    "black": 0x000000,
    "white": 0xFFFFFF,
    "gray": 0x808080,
    "grey": 0x808080,
    "cyan": 0x00FFFF,
    "teal": 0x008080,
    "brown": 0xA52A2A,
}

@bot.tree.command(name="addrole", description="Create a role with name and color")
@app_commands.describe(rolename="The name of the role", color="Color name or HEX (without #)")
async def addrole_slash(interaction: discord.Interaction, rolename: str, color: str):
    # Color logic
    try:
        color_lower = color.lower()
        if color_lower in color_names:
            role_color = Colour(color_names[color_lower])
        else:
            if len(color) == 6:
                role_color = Colour(int(color, 16))
            else:                                                                                   #addrole
                raise ValueError("Invalid HEX")
    except Exception:
        await interaction.response.send_message("❌ Invalid color. Use common names or HEX codes (6 digits, no #).", ephemeral=True)
        return

    try:
        new_role = await interaction.guild.create_role(name=rolename, colour=role_color)
        await interaction.response.send_message(f"✅ Created role **{new_role.name}** with color `{color}`")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to create roles.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)

from discord import Colour

color_names = {
    "red": 0xFF0000,
    "blue": 0x0000FF,
    "green": 0x00FF00,
    "purple": 0x800080,
    "yellow": 0xFFFF00,
    "orange": 0xFFA500,
    "pink": 0xFFC0CB,
    "black": 0x000000,
    "white": 0xFFFFFF,
    "gray": 0x808080,
    "grey": 0x808080,
    "cyan": 0x00FFFF,
    "teal": 0x008080,
    "brown": 0xA52A2A,
}

@bot.command(name="addrole")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, rolename: str, color: str):
    # Color logic
    try:
        color_lower = color.lower()
        if color_lower in color_names:
            role_color = Colour(color_names[color_lower])
        else:
            if len(color) == 6:
                role_color = Colour(int(color, 16))
            else:
                raise ValueError("Invalid HEX")
    except Exception:
        await ctx.send("❌ Invalid color. Use common names or HEX codes (6 digits, no #).")
        return

    try:
        new_role = await ctx.guild.create_role(name=rolename, colour=role_color)
        await ctx.send(f"✅ Created role **{new_role.name}** with color `{color}`")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create roles.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")











@bot.tree.command(name="roleall", description="Give a role to every member in the server")
@app_commands.describe(role="The role you want to give to everyone")
async def roleall_slash(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don't have permission to manage roles.", ephemeral=True)
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ I can't assign a role that's higher or equal to my top role.", ephemeral=True)  #roleall
        return

    await interaction.response.send_message("⏳ Giving the role to everyone... This might take a bit!")

    success = 0
    fail = 0

    for member in interaction.guild.members:
        try:
            await member.add_roles(role)
            success += 1
        except Exception:
            fail += 1

    await interaction.followup.send(
        f"✅ Done!\n**Given to:** `{success}` members\n**Failed on:** `{fail}` members"
    )












@bot.tree.command(name="roleremoveall", description="Remove a role from everyone in the server")
@app_commands.describe(role="The role you want to remove from everyone")
async def roleremoveall_slash(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don't have permission to manage roles.", ephemeral=True)
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ I can't remove a role that's higher or equal to my top role.", ephemeral=True)  #antirollall
        return

    await interaction.response.send_message("⏳ Removing the role from everyone... This might take a bit!")

    success = 0
    fail = 0

    for member in interaction.guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                success += 1
            except Exception:
                fail += 1

    await interaction.followup.send(
        f"🧹 Done!\n**Removed from:** `{success}` members\n**Failed on:** `{fail}` members"
    )

@bot.command(name="roleremoveall")
@commands.has_permissions(manage_roles=True)
async def roleremoveall(ctx, role: discord.Role):
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ I can't remove a role that's higher or equal to my top role.")
        return

    await ctx.send("⏳ Removing the role from everyone... This might take a bit!")

    success = 0
    fail = 0

    for member in ctx.guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                success += 1
            except:
                fail += 1

    await ctx.send(f"🧹 Done!\n**Removed from:** `{success}` members\n**Failed on:** `{fail}` members")









@bot.tree.command(name="makealive", description="Bring someone back to life 💫")
@app_commands.describe(user="The user you want to revive")
async def makealive_slash(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("🫣 You can't revive yourself... that's illegal.")                                   #alive
        return

    await interaction.response.defer(ephemeral=True)

    await interaction.channel.send(
        f"**{interaction.user.display_name}** brought **{user.display_name}** back to life 🧬✨"
    )

@bot.command(name="makealive", help="Bring someone back to life 💫")
async def makealive_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send("🫣 You can't revive yourself... that's illegal.")
        return

    await ctx.send(f"**{ctx.author.display_name}** brought **{user.display_name}** back to life 🧬✨")





from roast import roasts  # ← pull the roast list from your other file

@bot.tree.command(name="roast", description="Roast someone into ashes 🔥")
@app_commands.describe(user="The person you wanna roast")
async def roast_slash(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("🚫 You can't roast yourself... but nice try, diddy.")
        return

    await interaction.response.defer(ephemeral=True)
    roast = random.choice(roasts)
    await interaction.channel.send(f"🔥 **{interaction.user.display_name}** roasted **{user.display_name}**: {roast}")


from roast import roasts

@bot.command(name="roast", help="Roast someone into ashes 🔥")
async def roast_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send("🚫 You can't roast yourself... but nice try, crispy.")
        return

    roast = random.choice(roasts)
    await ctx.send(f"🔥 **{ctx.author.display_name}** roasted **{user.display_name}**: {roast}")









@bot.tree.command(name="iq", description="Check someone's IQ (for real... trust me bro)")
@app_commands.describe(user="The user you wanna IQ test")
async def iq_slash(interaction: discord.Interaction, user: discord.User = None):
    import random

    if user is None:
        user = interaction.user

    iq_score = random.randint(20, 200)

    # Optional spicy messages
    flavor = ""
    if iq_score < 70:
        flavor = "💀 bro's legally a microwave"
    elif iq_score > 150:
        flavor = "🧠 certified giga brain"
    elif iq_score > 110:
        flavor = "😎 above average, not bad"
    elif iq_score < 90:
        flavor = "🤔 yikes..."

    await interaction.response.send_message(
        f"🧪 **{user.display_name}** has an IQ of **{iq_score}**. {flavor}"
    )


@bot.command(name="iq", help="Check someone's IQ (for real... trust me bro)")
async def iq_prefix(ctx, user: discord.User = None):
    import random

    if user is None:
        user = ctx.author

    iq_score = random.randint(20, 200)

    flavor = ""
    if iq_score < 70:
        flavor = "💀 bro's legally a microwave"
    elif iq_score > 150:
        flavor = "🧠 certified giga brain"
    elif iq_score > 110:
        flavor = "😎 above average, not bad"
    elif iq_score < 90:
        flavor = "🤔 yikes..."

    await ctx.send(f"🧪 **{user.display_name}** has an IQ of **{iq_score}**. {flavor}")









@bot.tree.command(name="ship", description="Ship two users and calculate their compatibility ❤️")
@app_commands.describe(user1="First user", user2="Second user (optional)")
async def ship_slash(interaction: discord.Interaction, user1: discord.User, user2: discord.User = None):
    if user2 is None:
        user2 = interaction.user

    pair = {user1.name.lower(), user2.name.lower()}  # usernames lowercased to avoid case issues

    if pair == {"lyrics.loop", "_cookie.mp3"}:
        percentage = 100
    elif pair == {"lyrics.loop", "apples0924"}:
        percentage = 0
    elif pair == {"kimmyluvsrem", "remluvskimmy"}:
        percentage = 100
    elif pair == {"lyrics.loop", "kimmyluvsrem"}:
        percentage = 1
    elif pair == {"lyrics.loop", "_iloveasians"}:
        percentage = random.randint(50, 100)
    else:
        percentage = random.randint(0, 100)

    await interaction.response.send_message(
        f"💖 Compatibility between **{user1.display_name}** and **{user2.display_name}** is **{percentage}%**"
    )


@bot.command(name="ship", help="Ship two users and calculate their compatibility ❤️")
async def ship_prefix(ctx, user1: discord.User, user2: discord.User = None):
    if user2 is None:
        user2 = ctx.author

    pair = {user1.name.lower(), user2.name.lower()}

    if pair == {"lyrics.loop", "_cookie.mp3"}:
        percentage = 100
    elif pair == {"lyrics.loop", "apples0924"}:
        percentage = 0
    elif pair == {"kimmyluvsrem", "remluvskimmy"}:
        percentage = 100
    elif pair == {"lyrics.loop", "kimmyluvsrem"}:
        percentage = 1
    elif pair == {"lyrics.loop", "_iloveasians"}:
        percentage = random.randint(50, 100)
    else:
        percentage = random.randint(0, 100)

    await ctx.send(f"💖 Compatibility between **{user1.display_name}** and **{user2.display_name}** is **{percentage}%**")




# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG) #######