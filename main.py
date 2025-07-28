import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio
import math
import json
from discord import ui  
import re
import datetime


from bottoken import token  


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
        synced = await bot.tree.sync()
        command_names = [f"/{cmd.name}" for cmd in synced]
        print(f"🌐 Globally synced {len(synced)} slash commands as: {', '.join(command_names)} ✅")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    # Start background task for clearing expired warns
    if not hasattr(bot, "warn_task") or bot.warn_task.done():
        bot.warn_task = bot.loop.create_task(remove_expired_warns())











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








kiss_file = "kiss_counts.json"

# Load kiss data from file or init empty dict
if os.path.exists(kiss_file):
    with open(kiss_file, "r") as f:
        kiss_counts = json.load(f)
else:
    kiss_counts = {}

def save_kiss_counts():
    with open(kiss_file, "w") as f:
        json.dump(kiss_counts, f)

def update_kiss_count(kisser_id, kissed_id):
    # Convert IDs to str for JSON keys
    kisser = str(kisser_id)
    kissed = str(kissed_id)

    if kisser not in kiss_counts:
        kiss_counts[kisser] = {}

    if kissed not in kiss_counts[kisser]:
        kiss_counts[kisser][kissed] = 0

    kiss_counts[kisser][kissed] += 1
    save_kiss_counts()
    return kiss_counts[kisser][kissed]


@bot.tree.command(name="kiss", description="Kiss someone")
@app_commands.describe(user="The user you want to kiss")
async def kiss_slash(interaction: discord.Interaction, user: discord.User):
    count = update_kiss_count(interaction.user.id, user.id)
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** kissed **{user.display_name}**\n  -# They have kissed **{count}** times 😘"
    )

@bot.command(name="kiss")
async def kiss(ctx, user: discord.User):
    count = update_kiss_count(ctx.author.id, user.id)
    await ctx.send(
        f"**{ctx.author.display_name}** kissed **{user.display_name}**\n-# They have kissed **{count}** times 😘"
    )










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
        await interaction.response.send_message("❌ do NOT kill yourself", ephemeral=True)
        return

    if user.id == bot.user.id:
        await interaction.response.send_message("Nice try Diddy", ephemeral=True)
        return

    if user.name == "_cookie.mp3":
        await interaction.response.send_message("WHY R U TRYING TO KILL COOKIE MY POOKIE I **WILL** FIND YOU", ephemeral=True)
        return
    elif user.name == "lyrics.loop":
        await interaction.response.send_message("Nice try Diddy", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(
        f"**{interaction.user.display_name}** killed **{user.display_name}** 💀☠️"
    )


@bot.command(name="kill")
async def kill(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send("❌ do NOT kill yourself")
        return

    if user.id == bot.user.id:
        await ctx.send("Nice try Diddy")
        return

    if user.name == "_cookie.mp3":
        await ctx.send("WHY R U TRYING TO KILL COOKIE MY POOKIE I **WILL** FIND YOU")
        return
    elif user.name == "lyrics.loop":
        await ctx.send("Nice try Diddy")
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








# --- Your custom IQ map based on usernames (lowercase) ---
special_iq_scores = {
    "lyrics.loop": "Infinity",
    "_cookie.mp3": 124,
    "invortr45": 0,
    "idk": 15  # example entry
}

# --- Flavor texts ---
def get_flavor(iq_score):
    if iq_score < 70:
        return "💀 bro's legally a microwave"
    elif iq_score > 150:
        return "🧠 certified giga brain"
    elif iq_score > 110:
        return "😎 above average, not bad"
    elif iq_score < 90:
        return "🤔 yikes..."
    return ""

# --- Shared logic ---
def calculate_iq(user: discord.User):
    username = user.name.lower()
    iq_score = special_iq_scores.get(username, random.randint(20, 200))
    flavor = get_flavor(iq_score)
    return iq_score, flavor

# --- Slash Command ---
@bot.tree.command(name="iq", description="Check someone's IQ (for real... trust me bro)")
@app_commands.describe(user="The user you wanna IQ test")
async def iq_slash(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user

    iq_score, flavor = calculate_iq(user)

    await interaction.response.send_message(
        f"🧪 **{user.display_name}** has an IQ of **{iq_score}**. {flavor}"
    )

# --- Prefix Command ---
@bot.command(name="iq", help="Check someone's IQ (for real... trust me bro)")
async def iq_prefix(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    iq_score, flavor = calculate_iq(user)

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
    elif pair == {"lyrics.loop", "liaedwards"}:
        percentage = random.randint(99, 100)
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
    elif pair == {"lyrics.loop", "liaedwards"}:
        percentage = random.randint(99, 100)
    else:
        percentage = random.randint(0, 100)

    await ctx.send(f"💖 Compatibility between **{user1.display_name}** and **{user2.display_name}** is **{percentage}%**")








@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "anyways" in message.content.lower():
        try:
            await message.add_reaction("❌")
            await message.add_reaction("©️")
        except discord.errors.Forbidden:
            print("Missing reaction permissions!")

    await bot.process_commands(message)





@bot.tree.command(name="ghostping", description="Ghost ping a user!")
@app_commands.describe(user="User to ghost ping")
async def ghostping_slash(interaction: discord.Interaction, user: discord.User):
    try:
        ghost = await interaction.channel.send(f"<@{user.id}>")
        await asyncio.sleep(1)
        await ghost.delete()
        await interaction.response.send_message(f"Ghost pinged {user.mention} 👻", ephemeral=True)
    except discord.errors.Forbidden:
        await interaction.response.send_message("I don't have permissions to do that.", ephemeral=True)


@bot.command(name="ghostping")
@commands.has_permissions(manage_messages=True)
async def ghostping_prefix(ctx, user: discord.User):
    try:
        ghost = await ctx.channel.send(f"<@{user.id}>")
        await asyncio.sleep(1)
        await ghost.delete()
        await ctx.message.delete()
    except discord.errors.Forbidden:
        await ctx.send("I don't have permissions to do that.")








@bot.tree.command(name="fuck", description="Fuck someone sexually")
@app_commands.describe(user="The user you want to fuck")
async def fuck_slash(interaction: discord.Interaction, user: discord.User):          #fuck
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** fucked **{user.display_name}** 🍆🍑🍒💦"
    )

@bot.command(name="fuck")
async def fuck(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** fucked **{user.display_name}** 🍆🍑🍒💦")






@bot.tree.command(name="rape", description="Rape someone")
@app_commands.describe(user="The user you want to Rape")
async def Rape_slash(interaction: discord.Interaction, user: discord.User):          #Rape
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** Raped **{user.display_name}** 🍆🍑💦"
    )

@bot.command(name="rape")
async def rape(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** Raped **{user.display_name}** 🍆🍑💦")






@bot.tree.command(name="makenaked", description="make someone naked")
@app_commands.describe(user="The user you want to Make naked")
async def makenaked_slash(interaction: discord.Interaction, user: discord.User):          #makenaked
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** made **{user.display_name}** naked 🍆💦"
    )

@bot.command(name="makenaked")
async def makenaked(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** made **{user.display_name}** naked 🍆💦")






@bot.tree.command(name="wearcloths", description="make someone wear cloths")
@app_commands.describe(user="The user you want to Make Wear Cloths")
async def wearcloths_slash(interaction: discord.Interaction, user: discord.User):          #wearcloths
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** made **{user.display_name}** Wear cloths"
    )

@bot.command(name="wearcloths")
async def wearcloths(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** made **{user.display_name}** wear cloths")







@bot.tree.command(name="respect", description="respect someone")
@app_commands.describe(user="The user you want respect")
async def respect_slash(interaction: discord.Interaction, user: discord.User):          #respect
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** respected **{user.display_name}**"
    )

@bot.command(name="respect")
async def respect(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** respected **{user.display_name}**")






@bot.tree.command(name="disrespect", description="disrespect someone")
@app_commands.describe(user="The user you want disrespect")
async def disrespect_slash(interaction: discord.Interaction, user: discord.User):          #disrespect
    await interaction.response.send_message(
        f"**{interaction.user.display_name}** disrespected **{user.display_name}**"
    )
 
@bot.command(name="disrespect")
async def disrespect(ctx, user: discord.User):
    await ctx.send(f"**{ctx.author.display_name}** disrespected **{user.display_name}**")







# Slash command
@bot.tree.command(name="test", description="test")  # Slash: /test
async def test_slash(interaction: discord.Interaction):
    await interaction.response.send_message("works")

# Prefix command
@bot.command(name="test")  # Prefix: >test or whatever your prefix is
async def test_prefix(ctx):
    await ctx.send("works")











globalAFK_file = "globalAFK.json"
serverAFK_file = "serverAFK.json"

# Load data from JSON or init empty dicts
if os.path.exists(globalAFK_file):
    with open(globalAFK_file, "r") as f:
        globalAFK_users = json.load(f)
else:
    globalAFK_users = {}

if os.path.exists(serverAFK_file):
    with open(serverAFK_file, "r") as f:
        serverAFK_users = json.load(f)
else:
    serverAFK_users = {}

def save_globalAFK():
    with open(globalAFK_file, "w") as f:
        json.dump(globalAFK_users, f)

def save_serverAFK():
    with open(serverAFK_file, "w") as f:
        json.dump(serverAFK_users, f)

# --- Global AFK Slash Command ---
@bot.tree.command(name="globalafk", description="Set your AFK status globally")
@app_commands.describe(reason="Why are you AFK?")
async def globalAFK_slash(interaction: discord.Interaction, reason: str = "AFK"):
    globalAFK_users[str(interaction.user.id)] = reason
    save_globalAFK()
    await interaction.response.send_message(f"🌐 You are now globally AFK: {reason}")

# --- Global AFK Prefix Command ---
@bot.command(name="globalafk")
async def globalAFK_prefix(ctx, *, reason: str = "AFK"):
    globalAFK_users[str(ctx.author.id)] = reason
    save_globalAFK()
    await ctx.send(f"🌐 **{ctx.author.display_name}** is now globally AFK: {reason}")

# --- Server AFK Slash Command ---
@bot.tree.command(name="afk", description="Set your AFK status for this server only")
@app_commands.describe(reason="Why are you AFK?")
async def serverAFK_slash(interaction: discord.Interaction, reason: str = "AFK"):
    guild_id = str(interaction.guild.id)
    if guild_id not in serverAFK_users:
        serverAFK_users[guild_id] = {}
    serverAFK_users[guild_id][str(interaction.user.id)] = reason
    save_serverAFK()
    await interaction.response.send_message(f"🌍 You are now AFK in this server: {reason}")

# --- Server AFK Prefix Command ---
@bot.command(name="afk")
async def serverAFK_prefix(ctx, *, reason: str = "AFK"):
    guild_id = str(ctx.guild.id)
    if guild_id not in serverAFK_users:
        serverAFK_users[guild_id] = {}
    serverAFK_users[guild_id][str(ctx.author.id)] = reason
    save_serverAFK()
    await ctx.send(f"🌍 **{ctx.author.display_name}** is now AFK in this server: {reason}")

# --- Handle Mentions + Message Events ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check mentions for GLOBAL AFK
    for user in message.mentions:
        if str(user.id) in globalAFK_users:
            await message.channel.send(f"🌐 **{user.display_name}** is globally AFK: {globalAFK_users[str(user.id)]}")
            break

    # Check mentions for SERVER AFK
    if message.guild and message.mentions:
        guild_id = str(message.guild.id)
        for user in message.mentions:
            if guild_id in serverAFK_users and str(user.id) in serverAFK_users[guild_id]:
                await message.channel.send(f"🌍 **{user.display_name}** is AFK in this server: {serverAFK_users[guild_id][str(user.id)]}")
                break

    # Remove GLOBAL AFK if they talk
    author_id = str(message.author.id)
    if author_id in globalAFK_users:
        del globalAFK_users[author_id]
        save_globalAFK()
        await message.channel.send(f"✅ Welcome back **{message.author.display_name}**, your global AFK is removed.")

    # Remove SERVER AFK if they talk
    if message.guild:
        guild_id = str(message.guild.id)
        if guild_id in serverAFK_users and author_id in serverAFK_users[guild_id]:
            del serverAFK_users[guild_id][author_id]
            save_serverAFK()
            await message.channel.send(f"✅ Welcome back **{message.author.display_name}**, your server AFK is removed.")

    await bot.process_commands(message)








@bot.tree.command(name="sacrifice", description="Sacrifice someone dramatically")
@app_commands.describe(user="The user you want to sacrifice")
async def sacrifice_slash(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.send_message("❌ do NOT sacrifice yourself", ephemeral=True)
        return

    if user.id == bot.user.id:
        await interaction.response.send_message("Nice try Diddy", ephemeral=True)
        return

    if user.name == "_cookie.mp3":
        await interaction.response.send_message("WHY R U TRYING TO SACRIFICE COOKIE MY POOKIE I **WILL** FIND YOU", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(
        f"**{interaction.user.display_name}** sacrificed **{user.display_name}** 🔥🕯️"
    )


@bot.command(name="sacrifice")
async def sacrifice(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send("❌ do NOT sacrifice yourself")
        return

    if user.id == bot.user.id:
        await ctx.send("Nice try Diddy")
        return

    if user.name == "_cookie.mp3":
        await ctx.send("WHY R U TRYING TO SACRIFICE COOKIE MY POOKIE I **WILL** FIND YOU")
        return

    await ctx.send(f"**{ctx.author.display_name}** sacrificed **{user.display_name}** 🔥🕯️")






@bot.tree.command(name="gayrate", description="Check how gay someone is 🌈")
@app_commands.describe(user="The user you want to scan")
async def gayrate_slash(interaction: discord.Interaction, user: discord.User):
    username = user.name.lower()

    if username == "lyrics.loop":
        rate = -100
    elif username == "_cookie.mp3":
        rate = 50
    elif username == "invortr45":
        rate = 'infinite'
    elif username == "_a_random_account_":
        rate = -1
    elif username == "themeyt":
        rate = 100
    else:
        rate = random.randint(0, 100)

    await interaction.response.send_message(
        f"🏳️‍🌈 **{user.display_name}** is **{rate}%** gay!"
    )



@bot.command(name="gayrate")
async def gayrate_prefix(ctx, user: discord.User):
    username = user.name.lower()

    if username == "lyrics.loop":
        rate = -100
    elif username == "_cookie.mp3":
        rate = 50
    elif username == "invortr45":
        rate = 'infinite'
    elif username == "_a_random_account_":
        rate = -1
    elif username == "themeyt":
        rate = 100
    else:
        import random
        rate = random.randint(0, 100)

    await ctx.send(
        f"🏳️‍🌈 **{user.display_name}** is **{rate}%** gay!"
    )










# --- Your custom asexual rate map based on usernames (lowercase) ---
special_asexual_rates = {
    "lyrics.loop": 2,
    "_cookie.mp3": 0,
    "invortr45": random.randint(80, 99),
    "idk": 25  # example
}

# --- Flavor texts ---
def get_flavor(rate):
    if rate == 100:
        return "💅 100% asexual frfr"
    elif rate >= 75:
        return "🌈 pretty dang ace"
    elif rate >= 50:
        return "🤔 maybe questioning??"
    elif rate >= 25:
        return "😏 lil fruity... but not quite"
    else:
        return "💀 bro's down bad 💀"

# --- Shared logic ---
def calculate_asexual_rate(user: discord.User):
    username = user.name.lower()
    rate = special_asexual_rates.get(username, random.randint(0, 100))
    flavor = get_flavor(rate)
    return rate, flavor

# --- Slash Command ---
@bot.tree.command(name="asexualrate", description="Check someone's asexual rate")
@app_commands.describe(user="The user you wanna scan for asexual energy")
async def asexualrate_slash(interaction: discord.Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user

    rate, flavor = calculate_asexual_rate(user)

    await interaction.response.send_message(
        f"🧪 **{user.display_name}** is **{rate}%** asexual. {flavor}"
    )

# --- Prefix Command ---
@bot.command(name="asexualrate", help="Check someone's asexual rate")
async def asexualrate_prefix(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    rate, flavor = calculate_asexual_rate(user)

    await ctx.send(f"🧪 **{user.display_name}** is **{rate}%** asexual. {flavor}")

























import string
import asyncio
import datetime
import re

WARN_FILE = "warnings.json"

# Load warnings from file or create empty dict
if os.path.exists(WARN_FILE):
    with open(WARN_FILE, "r") as f:
        warns = json.load(f)
else:
    warns = {}

# Base62 chars for 4 digit code
BASE62 = string.ascii_uppercase + string.ascii_lowercase + string.digits

def generate_warn_id():
    return ''.join(random.choice(BASE62) for _ in range(4))

def save_warns():
    with open(WARN_FILE, "w") as f:
        json.dump(warns, f, indent=4)

def parse_time(timestr):
    if not timestr:
        return None
    match = re.match(r"(\d+(\.\d+)?)([smhd])", timestr.lower())
    if not match:
        return None
    num = float(match.group(1))
    unit = match.group(3)
    seconds = 0
    if unit == 's':
        seconds = num
    elif unit == 'm':
        seconds = num * 60
    elif unit == 'h':
        seconds = num * 3600
    elif unit == 'd':
        seconds = num * 86400
    return int(seconds)

def time_to_str(seconds):
    if seconds is None:
        return "Permanent"
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds//60}m"
    if seconds < 86400:
        return f"{seconds//3600}h"
    return f"{seconds//86400}d"

async def remove_expired_warns():
    # Runs every 60 seconds to remove expired warns
    while True:
        changed = False
        now_ts = datetime.datetime.utcnow().timestamp()
        for guild_id in list(warns.keys()):
            for user_id in list(warns[guild_id].keys()):
                new_warn_list = []
                for warn in warns[guild_id][user_id]:
                    if warn["expires_at"] is None or warn["expires_at"] > now_ts:
                        new_warn_list.append(warn)
                    else:
                        changed = True
                if new_warn_list:
                    warns[guild_id][user_id] = new_warn_list
                else:
                    del warns[guild_id][user_id]
            if not warns[guild_id]:
                del warns[guild_id]
        if changed:
            save_warns()
        await asyncio.sleep(60)


# Unified warning function to add a warn
async def add_warn(ctx_or_interaction, user: discord.Member, time_str=None, reason=None):
    guild_id = str(user.guild.id)
    user_id = str(user.id)
    warn_id = generate_warn_id()
    duration = parse_time(time_str)
    now_ts = datetime.datetime.utcnow().timestamp()
    expires_at = now_ts + duration if duration else None
    warn_entry = {
        "id": warn_id,
        "time_warned": now_ts,
        "warned_by": str(ctx_or_interaction.user.id if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author.id),
        "reason": reason if reason else "No reason provided",
        "duration": duration,
        "expires_at": expires_at
    }
    if guild_id not in warns:
        warns[guild_id] = {}
    if user_id not in warns[guild_id]:
        warns[guild_id][user_id] = []
    warns[guild_id][user_id].append(warn_entry)
    save_warns()

    time_readable = time_to_str(duration)
    display_name = user.display_name

    reply = f"Warned user **{display_name}** for **{time_readable}**. Reason: **{warn_entry['reason']}**. ID: `{warn_id}`"
    if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
        await ctx_or_interaction.response.send_message(reply)
    else:
        await ctx_or_interaction.send(reply)

# Unified unwarn function
async def remove_warns(ctx_or_interaction, user: discord.Member = None, warn_id: str = None):
    guild_id = str(ctx_or_interaction.guild.id if hasattr(ctx_or_interaction, "guild") else ctx_or_interaction.message.guild.id)

    if guild_id not in warns:
        msg = "No warnings found for this server."
        if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else:
            await ctx_or_interaction.send(msg)
        return

    if user:
        user_id = str(user.id)
        if user_id not in warns[guild_id]:
            msg = f"No warnings found for user {user.display_name}."
            if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_interaction.send(msg)
            return

        if warn_id:
            # Remove specific warn by id
            before_count = len(warns[guild_id][user_id])
            warns[guild_id][user_id] = [w for w in warns[guild_id][user_id] if w["id"] != warn_id]
            after_count = len(warns[guild_id][user_id])
            if before_count == after_count:
                msg = f"No warning found with ID `{warn_id}` for user {user.display_name}."
            else:
                msg = f"Removed warning `{warn_id}` for user {user.display_name}."
            if not warns[guild_id][user_id]:
                del warns[guild_id][user_id]
            save_warns()
            if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(msg)
            else:
                await ctx_or_interaction.send(msg)
        else:
            # Remove all warns for user
            del warns[guild_id][user_id]
            save_warns()
            msg = f"Removed **all warnings** for user {user.display_name}."
            if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(msg)
            else:
                await ctx_or_interaction.send(msg)
    else:
        msg = "You must specify a user or a warning ID to remove warns."
        if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else:
            await ctx_or_interaction.send(msg)

# Unified warns listing
async def list_warns(ctx_or_interaction, user: discord.Member = None):
    guild_id = str(ctx_or_interaction.guild.id if hasattr(ctx_or_interaction, "guild") else ctx_or_interaction.message.guild.id)
    if not user:
        # Show warns for invoking user
        if hasattr(ctx_or_interaction, "user"):
            user = ctx_or_interaction.user
        else:
            user = ctx_or_interaction.author
    user_id = str(user.id)
    if guild_id not in warns or user_id not in warns[guild_id] or len(warns[guild_id][user_id]) == 0:
        msg = f"User {user.display_name} has no warnings."
        if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else:
            await ctx_or_interaction.send(msg)
        return

    now_ts = datetime.datetime.utcnow().timestamp()
    lines = []
    for w in warns[guild_id][user_id]:
        warn_id = w["id"]
        reason = w["reason"]
        time_warned = datetime.datetime.utcfromtimestamp(w["time_warned"]).strftime("%Y-%m-%d %H:%M UTC")
        dur_str = time_to_str(w["duration"])
        expires = w["expires_at"]
        if expires and expires < now_ts:
            continue
        lines.append(f"ID: `{warn_id}` | Warned at: {time_warned} | Duration: {dur_str} | Reason: {reason}")

    if not lines:
        msg = f"User {user.display_name} has no active warnings."
        if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else:
            await ctx_or_interaction.send(msg)
        return

    embed = discord.Embed(title=f"Warnings for {user.display_name}", description="\n".join(lines), color=discord.Color.orange())
    if hasattr(ctx_or_interaction, "response") and isinstance(ctx_or_interaction, discord.Interaction):
        await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await ctx_or_interaction.send(embed=embed)

# --------- PREFIX COMMANDS -----------

@bot.command(name="warn")
@commands.has_guild_permissions(kick_members=True)
async def warn_cmd(ctx, user: discord.Member, time: str = None, *, reason: str = None):
    """Warn someone with optional time and reason"""
    await add_warn(ctx, user, time, reason)

@bot.command(name="unwarn")
@commands.has_guild_permissions(kick_members=True)
async def unwarn_cmd(ctx, target: str = None, warn_id: str = None):
    """
    Remove warns by user mention or warn ID.
    Usage:
    >unwarn @user
    >unwarn ID1234
    """
    if not target:
        await ctx.send("You must specify a user mention or a warning ID.")
        return

    # Check if target is a user mention
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]

    if user:
        # remove all warns or specific warn if warn_id given
        await remove_warns(ctx, user, warn_id)
    else:
        # treat target as warn id, find user who has that warn id in guild
        guild_id = str(ctx.guild.id)
        if guild_id in warns:
            found = False
            for user_id, warn_list in warns[guild_id].items():
                for w in warn_list:
                    if w["id"] == target:
                        member = ctx.guild.get_member(int(user_id))
                        if member:
                            await remove_warns(ctx, member, target)
                            found = True
                            break
                if found:
                    break
            if not found:
                await ctx.send(f"No warning with ID `{target}` found in this server.")
        else:
            await ctx.send("No warnings stored in this server.")

@bot.command(name="warns")
async def warns_cmd(ctx, user: discord.Member = None):
    """List warns of a user or yourself"""
    await list_warns(ctx, user)

# --------- SLASH COMMANDS -----------

@bot.tree.command(name="warn", description="Warn someone with optional time and reason")
@app_commands.describe(user="User to warn", time="Duration (e.g., 1h, 3d)", reason="Reason for warning")
@commands.has_guild_permissions(kick_members=True)
async def warn_slash(interaction: discord.Interaction, user: discord.Member, time: str = None, reason: str = None):
    await add_warn(interaction, user, time, reason)

@bot.tree.command(name="unwarn", description="Remove warnings from user or by warn ID")
@app_commands.describe(user="User to remove warns from", id="Warning ID to remove")
@commands.has_guild_permissions(kick_members=True)
async def unwarn_slash(interaction: discord.Interaction, user: discord.Member = None, id: str = None):
    if not user and not id:
        await interaction.response.send_message("You must specify a user or warning ID.", ephemeral=True)
        return
    if user:
        await remove_warns(interaction, user, id)
    else:
        # Remove by ID only
        guild_id = str(interaction.guild.id)
        if guild_id in warns:
            found = False
            for user_id, warn_list in warns[guild_id].items():
                for w in warn_list:
                    if w["id"] == id:
                        member = interaction.guild.get_member(int(user_id))
                        if member:
                            await remove_warns(interaction, member, id)
                            found = True
                            break
                if found:
                    break
            if not found:
                await interaction.response.send_message(f"No warning with ID `{id}` found.", ephemeral=True)
        else:
            await interaction.response.send_message("No warnings stored for this server.", ephemeral=True)

@bot.tree.command(name="warns", description="List warnings of a user or yourself")
@app_commands.describe(user="User to check warnings for")
async def warns_slash(interaction: discord.Interaction, user: discord.Member = None):
    await list_warns(interaction, user)





print("🔁 Running bot...")
bot.run(token)