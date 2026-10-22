import discord
from discord import app_commands
from collections import deque
from random import randint
import sqlite3
import json

db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    user_id INTEGER PRIMARY KEY,
    character_name TEXT DEFAULT "미정",
    sex TEXT DEFAULT "미정",
    age INTEGER DEFAULT 0,
    dormitory TEXT DEFAULT "미정",
    grade INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_spells (
    user_id INTEGER PRIMARY KEY,
    spells TEXT NOT NULL DEFAULT '{}'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS magic_point (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    max_points INTEGER DEFAULT 0
)
""")

from config import TOKEN, GM_id# , role_id

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")

classification = [
    '일반마법(Charm)',
    '변형마법(Transfiguration)',
    '어둠의 마법(Dark arts) - 희롱마법(Hex)',
    '어둠의 마법(Dark arts) - 악행마법(Jinx)',
    '어둠의 마법(Dark arts) - 저주(Curse)',
    '방해 마법(Counter-spell)', '해제 마법(Counter-curse)',
    '치유 주문(Healing Spell)'
]
spell_choices = [
    app_commands.Choice(name = name, value = name)
    for name in classification
]
dormitory_choices = [
    app_commands.Choice(name = name, value = name)
    for name in ['그리핀도르(Gryffindor)', '슬리데린(Slytherin)', '후플푸프(Hufflepuff)', '래번클로(Ravenclaw)']
]
sex_choices = [
    app_commands.Choice(name = name, value = name)
    for name in ['남', '여']
]

@bot.tree.command(
    name = '마법추가',
    description = '사용 가능한 마법을 추가합니다.'
)
@app_commands.describe(
    마법이름 = '기본 : 미정',
    마법설명 = '기본 : 없음',
    숙련도 = '1~10 사이의 값'
)
@app_commands.choices(마법분류 = spell_choices)
async def 마법추가(interaction: discord.Interaction, 마법이름: str, 마법설명: str, 마법분류: app_commands.Choice[str], 숙련도: app_commands.Range[int, 1, 10]) :
    embed = discord.Embed(title = '사용 가능한 마법 추가')
    user_id = interaction.user.id
    category = 마법분류.value

    cursor.execute(
        "SELECT spells FROM user_spells WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result is not None :
        magic_list = json.loads(result[0])
    else :
        magic_list = {}
    
    if 마법이름 in magic_list :
        embed.add_field(
            name = '',
            value = '이미 보유 중인 마법입니다.',
            inline = False
        )
        await interaction.response.send_message(
            embed = embed,
            ephemeral = True
        )
    else :
        magic_list[마법이름] = {
            'description' : 마법설명,
            'classification' : category,
            'mastery' : 숙련도
        }
        cursor.execute("""
        INSERT INTO user_spells (user_id, spells)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET spells = excluded.spells
        """, (
            user_id,
            json.dumps(magic_list, ensure_ascii = False)
        ))

        db.commit()

        embed.add_field(
            name = f'마법이름 : {마법이름}',
            value = f'마법설명 : {마법설명}',
            inline = False
        )
        embed.add_field(
            name = '마법분류',
            value = category,
            inline = False
        )
        embed.add_field(
            name = '숙련도',
            value = f'{숙련도}LV',
            inline = False
        )
        await interaction.response.send_message(embed = embed)

@bot.tree.command(
    name = '상태창',
    description = '자신의 스탯을 조회합니다.'
)
async def 상태창(interaction: discord.Interaction) :
    user_id = interaction.user.id

    cursor.execute(
        "SELECT character_name, sex, age, dormitory, grade FROM status WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result is None:
        await interaction.response.send_message(
            "등록된 캐릭터 정보가 없습니다.",
            ephemeral = True
        )
        return

    pc_name, pc_sex, pc_age, pc_dormitory, pc_grade = result

    embed = discord.Embed(title = f'{pc_name}')

    embed.add_field(
        name = '기본정보',
        value = f"""
성별 : {pc_sex}성
나이 : {pc_age}
학년 : {pc_grade}학년
기숙사 : {pc_dormitory}
""",
        inline = False
    )

    cursor.execute(
        "SELECT spells FROM user_spells WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result is not None:
        user_spell = json.loads(result[0])
    else:
        user_spell = {}

    for i in classification :
        current_spell = []
        for magic in user_spell :
            if user_spell[magic]['classification'] == i :
                mastery = user_spell[magic]['mastery']
                if mastery == 10 :
                    current_spell.append(f'**{magic}({mastery}LV)**')
                else :
                    current_spell.append(f'{magic}({mastery}LV)')
        embed.add_field(
            name = f'**{i}**',
            value = ", ".join(current_spell) or '없음',
            inline = False
        )
    
    await interaction.response.send_message(embed = embed)

@bot.tree.command(
    name = '상태등록',
    description = '새로운 상태창을 등록합니다.'
)
@app_commands.describe(
    이름 = '캐릭터 이름을 입력해주세요.',
    성별 = '캐릭터의 성별을 선택해주세요.',
    나이 = '캐릭터 나이를 입력해주세요.',
    기숙사 = '4개의 기숙사 중에서 선택해주세요.',
    학년 = '7개의 학년 중에서 선택해주세요.'
)
@app_commands.choices(기숙사 = dormitory_choices, 성별 = sex_choices)
async def 상태등록(interaction: discord.Interaction, 이름: str, 성별: app_commands.Choice[str], 나이: app_commands.Range[int, 1, 100], 기숙사: app_commands.Choice[str], 학년: app_commands.Range[int, 1, 7]) :
    user_id = interaction.user.id
    selected_dormitory = 기숙사.value
    selected_sex = 성별.value
    embed = discord.Embed(title = f'**{이름}**')

    cursor.execute("""
    INSERT INTO status (
        user_id,
        character_name,
        sex,
        age,
        dormitory,
        grade
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET
        character_name = excluded.character_name,
        sex = excluded.sex,
        age = excluded.age,
        dormitory = excluded.dormitory,
        grade = excluded.grade
    """, (
        user_id,
        이름,
        selected_sex,
        나이,
        selected_dormitory,
        학년
    ))
    
    db.commit()

    embed.add_field(
        name = '기본정보',
        value = f"""
성별 : {selected_sex}성
나이 : {나이}세
학년 : {학년}학년
기숙사 : {selected_dormitory}
""",
        inline = False
    )

    await interaction.response.send_message(embed = embed)

@bot.tree.command(
    name = '남은마력',
    description = '현재 남은 마력을 확인합니다.'
)
async def 남은마력(interaction: discord.Interaction) :
    user_id = interaction.user.id

    cursor.execute(
        "SELECT character_name FROM status WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    if result is None:
        await interaction.response.send_message(
            "등록된 캐릭터 정보가 없습니다.",
            ephemeral = True
        )
        return

    character_name, = result

    embed = discord.Embed(title = character_name)

    cursor.execute(
        "SELECT points, max_points FROM magic_point WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result is None:
        await interaction.response.send_message(
            "현재 마력이 설정되어있지 않습니다.",
            ephemeral = True
        )
        return

    current_points, max_points = result

    embed.add_field(
        name = '현재 남은 마력',
        value = f"**{current_points} / {max_points}**" if current_points == max_points or current_points == 0 else f"{current_points} / {max_points}",
        inline = False
    )

    await interaction.response.send_message(embed = embed)

@bot.tree.command(
    name = '마력설정',
    description = '현재 마력 및 최대 마력을 설정합니다.'
)
@app_commands.describe(
    현재마력 = '현재 마력의 값을 설정합니다.',
    최대마력 = '자신의 최대 마력의 값을 설정합니다.'
)
async def 마력설정(interaction: discord.Interaction, 현재마력: int, 최대마력: int) :
    user_id = interaction.user.id

    cursor.execute(
        "SELECT character_name FROM status WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result is None:
        await interaction.response.send_message(
            "등록된 캐릭터 정보가 없습니다.",
            ephemeral = True
        )
        return
    
    character_name, = result
    
    embed = discord.Embed(title = character_name)

    if 현재마력 > 최대마력 :
        현재마력 = 최대마력
    
    cursor.execute("""
        INSERT INTO magic_point (user_id, max_points, points)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            points = excluded.max_points,
            max_points = excluded.points
        """, (
            user_id, 현재마력, 최대마력
        ))
    db.commit()
    
    embed.add_field(
        name = '상태 설정',
        value = f"**{현재마력} / {최대마력}**" if 현재마력 == 최대마력 or 현재마력 == 0 else f"{현재마력} / {최대마력}",
        inline = False
    )

    await interaction.response.send_message(embed = embed)

@bot.tree.command(
    name = '마력회복',
    description = '수치만큼 마력을 회복합니다. (기본값 1)'
)
@app_commands.describe(
    count = '수치만큼 마력을 회복합니다. 음수값이라면 차감됩니다. (생략시 1)'
)
async def 마력회복(interaction: discord.Interaction, count: int = 1) :
    user_id = interaction.user.id

    cursor.execute(
        "SELECT points, max_points FROM magic_point WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()

    if result is None:
        await interaction.response.send_message(
            "현재 마력이 설정되어있지 않습니다.",
            ephemeral = True
        )
        return
    
    points, max_points = result

    embed = discord.Embed(title = '마력회복')

    embed.add_field(
        name = '이전상태',
        value = f'{points} / {max_points}',
        inline = False
    )
    embed.add_field(
        name = '',
        value = '↓',
        inline = False
    )

    before_points = points
    points += count
    if points > max_points :
        points = max_points
    elif points < 0 :
        points = 0

    embed.add_field(
        name = '현재상태',
        value = f'{points} / {max_points}',
        inline = False
    )

    embed.add_field(
        name = '',
        value = f'총 {points - before_points}만큼 마력을 회복했습니다.',
        inline = False
    )

    cursor.execute("""
        UPDATE magic_point
        SET points = ?
        WHERE user_id = ?
    """, (points, user_id))
    db.commit()

    await interaction.response.send_message(embed = embed)

bot.run(TOKEN)