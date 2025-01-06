from typing import List, Optional, Union
from core.plugin import Plugin
from sdk.send_message import send_group_message
from sdk.message import instant_image_message, text_message
from .emoji_data import dates, emojis
from PIL import Image
from io import BytesIO
import requests

API = "https://www.gstatic.com/android/keyboard/emojikitchen"


def create_url(date: str, emoji1: List[int], emoji2: List[int]) -> str:
    def emoji_code(emoji: List[int]):
        return "-".join(f"u{c:x}" for c in emoji)

    u1 = emoji_code(emoji1)
    u2 = emoji_code(emoji2)
    return f"{API}/{date}/{u1}/{u1}_{u2}.png"


def find_emoji(emoji_code: str) -> Optional[List[int]]:
    emoji_num = ord(emoji_code)
    for e in emojis:
        if emoji_num in e:
            return e
    return None


def mix_emoji(emoji_code1: str, emoji_code2: str) -> Union[str, bytes]:
    emoji1 = find_emoji(emoji_code1)
    emoji2 = find_emoji(emoji_code2)
    if not emoji1:
        return f"不支持的emoji：{emoji_code1}"
    if not emoji2:
        return f"不支持的emoji：{emoji_code2}"

    urls: List[str] = []
    for date in dates:
        urls.append(create_url(date, emoji1, emoji2))
        urls.append(create_url(date, emoji2, emoji1))
    
    for url in urls:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            return image
        except:
            pass
    return f"网络解析错误"
    
async def handler(session: str, group_id: int, sender_id: int, message):
    emoji_1 = message[1].strip()[0]
    emoji_2 = message[1].strip()[2]
    mix = mix_emoji(emoji_1, emoji_2)
    if type(mix) == str:
        await send_group_message(session, group_id, text_message(mix))
    else:
        await send_group_message(session, group_id, instant_image_message(mix))
    

def checker(group_id: int, sender_id: int, message):
    return len(message[1].strip()) == 3 and message[1].strip()[1] == '+'

emoji = Plugin('emoji')
emoji.register_callback('group.@fumoP', handler, checker)