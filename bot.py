# coding: utf-8

import discord
import menu
import datetime

bot = discord.Client()
bot_id = None
bot_mention_a = None
bot_mention_b = None
aegide_avatar_url = None
aegide_url = "https://github.com/Aegide"


current_menu = None
current_timestamp = None


def get_timestamp():
    now = datetime.datetime.now()
    return str(now.day) + "/" + str(now.month)
     

def update_current_timestamp():
    global current_timestamp
    current_timestamp = get_timestamp()


def is_menu_outdated():
    global current_timestamp
    timestamp_now = get_timestamp()
    print("is_menu_outdated()", current_timestamp != timestamp_now, current_timestamp, timestamp_now)
    return current_timestamp != timestamp_now

def is_missing_menu():
    print("is_missing_menu()", current_menu is None)
    return current_menu is None


@bot.event
async def on_ready():
    global bot_id, bot_mention_a, bot_mention_b
    
    app_info = await bot.application_info()
    bot_id = app_info.id
    bot_mention_a = f"<@!{bot_id}>"
    bot_mention_b = f"<@{bot_id}>"

    permission_id = "2048"  # Send message
    # permission_id = "0"  # Nothing

    global aegide_avatar_url
    aegide = app_info.owner
    aegide_avatar_url = aegide.avatar_url_as(static_format='png', size=256)

    print("\n\n")
    print("Ready! bot invite:\n\nhttps://discordapp.com/api/oauth2/authorize?client_id=" + str(bot_id) + "&permissions=" + permission_id + "&scope=bot")
    print("\n\n")


def get_content():
    return current_menu.day


def get_embed(desktop_friendly=False):

    if desktop_friendly:
        extra_format = '\u200b'
    else:
        extra_format = ""

    embed = discord.Embed(
        color=discord.Color(14812434),
        )

    embed.set_footer(
        text="github.com/aegide",
        icon_url=aegide_avatar_url
        )

    embed.add_field(
        name = "🍽️ CHAINE TRADITIONNELLE",
        value = f"{current_menu.classic}{extra_format}",
        inline=desktop_friendly
    )
    if(desktop_friendly):
        embed.add_field(
            name = '\u200b',
            value = '\u200b',
            inline=True
        )
    embed.add_field(
        name = "🍟 CHAINE FRITERIE",
        value = f"{current_menu.fries}{extra_format}",
        inline=desktop_friendly
    )
    
    embed.add_field(
        name = "🐟 CHAINE POISSON VEGE",
        value = f"{current_menu.fish}",
        inline=desktop_friendly
    )
    if(desktop_friendly):
        embed.add_field(
            name = '\u200b',
            value = '\u200b',
            inline=True
        )
    embed.add_field(
        name = "🌴 CHAINE TOURISTE",
        value = f"{current_menu.tourist}",
        inline=desktop_friendly
    )
    return embed


# TODO : improve this
def is_mention(message):
    return message.content==bot_mention_a or message.content==bot_mention_b


def log_activity(message):
    if message.guild is None:
        print(f"\n{message.author} : DirectMessage")
    else:
        print(f"\n{message.author} : [{message.guild}]#{message.channel} ")


def update_menu():
    if is_missing_menu() or is_menu_outdated():
        print("UPDATE MENU")
        global current_menu
        current_menu = menu.get_menu()
        update_current_timestamp()
    else:
        print("RE-USE MENU")


async def handle_message(message):
    update_menu()
    await message.channel.send(embed=get_embed(desktop_friendly=False), content=get_content())


@bot.event
async def on_message(message: discord.Message):
    if is_mention(message):
        log_activity(message)
        await handle_message(message)


@bot.event
async def on_command_error(ctx, error):
    print(ctx.author, ":", ctx.message.content, ":", error)


# The token of the bot is stored inside a file
token = open("token.txt").read().rstrip()


bot.run(token)
