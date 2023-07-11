import disnake
from disnake.ext import commands
from disnake.utils import get

intents = disnake.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)


client.help_command = MyHelpCommand()


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
    print(f'準備完了！')


# 起動確認コマンド
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # !hello(設定を表示します)
    if message.content == '!hello':
        await message.channel.send('Hello World!\n'
                                   '現在の設定は以下の通りです\n'
                                   'テキストカテゴリー_個別カテゴリー\n'
                                   'ボイスカテゴリー_個人vc\n'
                                   'テキストチャンネルテンプレート_📝｜UserName\n'
                                   'ボイスチャンネルテンプレート_🔈｜UserName')


client.run("You_token")
