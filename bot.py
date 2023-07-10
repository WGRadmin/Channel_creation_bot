import disnake
from disnake.ext import commands
from disnake.ext.commands import slash_command
from disnake.utils import get

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_member_join(member):
    guild = member.guild
    text_category = get(guild.categories, name="個別テキスト")
    voice_category = get(guild.categories, name="個人vc")
    role = get(guild.roles, name="指定したロール")
    print(f"Role: {role}")
    overwrites = {
        guild.default_role: disnake.PermissionOverwrite(read_messages=False),
        guild.me: disnake.PermissionOverwrite(read_messages=True),
        role: disnake.PermissionOverwrite(read_messages=True)
    }
    text_channel = await guild.create_text_channel(f"📝｜{member.name}", category=text_category, overwrites=overwrites)
    voice_channel = await guild.create_voice_channel(f"🔈｜{member.name}", category=voice_category, overwrites=overwrites)

    # メンションしてメッセージを送信
    await text_channel.send(f"ようこそ、{member.mention}さん！ {role.mention}の方々もよろしくお願いします。")


# log inメッセージ
@client.event
async def on_ready():
    await client.change_presence(activity=disnake.Game(name="チャンネルを作成"))
    print(f'{client.user}_has log in!')


# /helloコマンド
@slash_command(guild_ids=[1127635219474825326], description="起動を確認するコマンドです！")
async def hello(ctx):
    await ctx.respond("起動完了です！")


client.run("youtoken")
