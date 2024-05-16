from sdk.send_message import send_group_message
from sdk.message import text_message, instant_image_message # , web_image_message
from typing import List, Tuple
import random
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump, random_key
import time
from sdk.timer import Timer

from PIL import Image

import requests
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def combine_images(images):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return new_image

folder = {
    "0p": "9f", "1p": "b1", "2p": "65", "3p": "1b", "4p": "b8", "5p": "2a", "6p": "07", "7p": "3b", "8p": "36", "9p": "88",
    "0s": "a8", "1s": "c0", "2s": "b9", "3s": "fe", "4s": "1f", "5s": "2a", "6s": "a9", "7s": "f2", "8s": "e9", "9s": "60",
    "0m": "da", "1m": "40", "2m": "51", "3m": "0b", "4m": "f2", "5m": "b5", "6m": "32", "7m": "f4", "8m": "d0", "9m": "75",
    "1z": "2b", "2z": "d6", "3z": "27", "4z": "5f", "5z": "0c", "6z": "04", "7z": "ca"
}

def url(pai: str) -> str:
    f = folder[pai]
    return f"https://wiki.lingshangkaihua.com/mediawiki/images/thumb/{f[0]}/{f}/{pai}.png/41px-{pai}.png"

def hupai(pai: List[int]) -> bool:
    if sum(pai) == 0:
        return True
    if sum(pai) % 3 == 2:
        for i in range(1, 10):
            if pai[i] >= 2:
                new_pai = pai[:]
                new_pai[i] -= 2
                if hupai(new_pai):
                    return True
        return False
    for i in range(1, 8):
        if pai[i] >= 1 and pai[i+1] >= 1 and pai[i+2] >= 1:
            new_pai = pai[:]
            new_pai[i] -= 1
            new_pai[i+1] -= 1
            new_pai[i+2] -= 1
            if hupai(new_pai):
                return True
    for i in range(1, 10):
        if pai[i] >= 3:
            new_pai = pai[:]
            new_pai[i] -= 3
            if hupai(new_pai):
                return True
    return False

def ting(pai: List[int]) -> List[int]:
    ret = []
    for i in range(1, 10):
        if pai[i] != 4:
            new_pai = pai[:]
            new_pai[i] += 1
            if hupai(new_pai):
                ret.append(i)
    return ret

def make_exercise(difficulty: int = 1, num: int = 13) -> Tuple[List[int], List[int]]:
    a = list(range(1, 10)) * 4
    while True:
        random.shuffle(a)
        count = [0] * 10
        for i in range(num):
            count[a[i]] += 1
        tp = ting(count)
        if len(tp) >= difficulty:
            return sorted(a[:num]), tp

def to_message(pai: List[int], mps: str) -> List[str]:
    # return "".join(map(str, pai))
    # return [web_image_message(url(f"{i}{mps}")) for i in pai]
    if len(pai) == 13 and 5 in pai and random.random() <= 0.25 * pai.count(5):
        for i in range(len(pai)):
            if pai[i] == 5:
                pai[i] = 0
                break
            
    return instant_image_message(combine_images([download_image(url(f"{i}{mps}")) for i in pai]))

async def handler(session: str, group_id: int, sender_id: int, message):
    key = f"tingpai_{group_id}"
    
    data = fetch(key)
    assert data != None

    if message[0] == "结束游戏":
        await send_group_message(session, group_id, text_message(f"游戏结束，答案是 "), to_message(data['answer'], data['mps']))
        dump(key)
        return
    
    message = "".join(sorted(message[0]))
    # print("get message", message)

    if message == "".join([str(i) for i in data['answer']]):
        await send_group_message(session, group_id, text_message(f"答对咯，答案是 "), to_message(data['answer'], data['mps']))
        dump(key)
        return
    else:
        await send_group_message(session, group_id, text_message(f"回答错了喵，请继续回答喵~"))
        return

async def no_reply(session: str, group_id: int, key: str):
    data = fetch(f"tingpai_{group_id}")
    if data == None or data["key"] != key:
        return
    await send_group_message(session, group_id, text_message(f"游戏超时结束，答案是 "), to_message(data['answer'], data['mps']))
    dump(f"tingpai_{group_id}")

def checker(group_id: int, sender_id: int, message):
    return message[0] == "结束游戏" or all([i in "123456789" for i in message[0]])

async def startup_handler(session: str, group_id: int, sender_id: int, message):
    key = f"tingpai_{group_id}"
    
    if fetch(key) != None:
        await send_group_message(session, group_id, text_message("请先猜对当前听牌，或输入“结束游戏”"))
        return

    if message[1] == "清一色":
        exercise, answer = make_exercise()
    elif message[1] == "清一色hard":
        exercise, answer = make_exercise(4)
    elif message[1] == "清一色lunatic":
        exercise, answer = make_exercise(5)
    elif message[1] == "清一色superhard":
        exercise, answer = make_exercise(4, 16)
    elif message[1] == "清一色extrahard":
        exercise, answer = make_exercise(5, 19)

    game_key = random_key()

    mps = random.choice(['m', 'p', 's'])

    alloc(key, {
        "exercise": exercise,
        "answer": answer,
        "key": game_key,
        "mps": mps
    })

    await send_group_message(session, group_id, to_message(exercise, mps), text_message("听牌是？"))
    tingpai.register_timer(Timer(15), no_reply, session, group_id, game_key)

def startup_checker(group_id: int, sender_id: int, message):
    return message[1] in ["清一色", "清一色hard", "清一色lunatic", "清一色superhard", "清一色extrahard"]

tingpai = Plugin('tingpai')
tingpai.register_callback('group.@fumoP', startup_handler, startup_checker)
tingpai.register_callback('group.P', handler, checker)
