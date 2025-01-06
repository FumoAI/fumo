import traceback
from sdk.send_message import send_group_message, send_friend_message
from sdk.message import text_message, web_image_message
from core.plugin import Plugin
from sdk.chatgpt import ask, plain_msg
from sdk.history import message_from_id
from sdk.message import convert_message
from sdk.temp_data import fetch, alloc, dump
from sdk.persisted_data import fetch as persist_fetch
from sdk.log import logger
from random import random
import time
from config import QQ, PRIVILEDGED_GROUP, PRIVILEDGED_USER

group_logger = logger("chatgpt", "Group")
friend_logger = logger("chatgpt", "Friend")

def dialog(key: str, message: str, logger, privileged: bool) -> str:
    if message == "结束对话":
        dump(key)
        return "对话结束"

    data = fetch(key)

    if data != None and time.time() - data['time'] > 7200: # 2 hr
        dump(key)
        data = None

    if data == None:
        alloc(key, {
            "history": [{
                "role": "system",
                "content": "You are a helpful assistant."
            }],
            "time": time.time()
        })
        data = fetch(key)

    data["time"] = time.time()

    data["history"].append({
        "role": "user",
        "content": message
    })

    try:
        if len(data["history"]) > 31:
            dump(key)
            return "上下文过长，请回复“结束对话”重新开始"
        resp = ask(data["history"], privileged)
        data["history"].append({
            "role": "assistant",
            "content": resp
        })
    except:
        resp = "网络错误/关键词异常，请更换prompt后重试"
        logger["error"](message)
        logger["error"](traceback.format_exc())

    return resp


async def group_message_handler(session: str, group_id: int, sender_id: int, message):
    key = f"chatgpt_{group_id}_{sender_id}"
    prv = group_id == PRIVILEDGED_GROUP
    resp = dialog(key, message[2], group_logger, prv)
    group_logger["info"](f"{group_id}: {sender_id}: [{prv}] {message[2]}\n{resp}")
    await send_group_message(session, group_id, text_message(resp))
    if random() >= 0.95:
        token = persist_fetch('token_usage').get('usage')
        price = round(token * 0.000617, 2)
        await send_group_message(session, group_id, text_message(f'目前总共消耗token：{token}个，约合￥{price}，GPT-4维护不易，可以对我发电哦~'), web_image_message('https://xhfs5.ztytech.com/CA107011/e6786e279d9a45079ca88e67c77df7b4.jpg'))

async def friend_message_handler(session: str, sender_id: int, message):
    if sender_id == QQ:
        return
    key = f"chatgpt_{sender_id}"
    prv = sender_id == PRIVILEDGED_USER
    resp = dialog(key, message[0], friend_logger, prv)
    friend_logger["info"](f"{sender_id}: {message[0]}\n{resp}")
    await send_friend_message(session, sender_id, text_message(resp))
    if random() >= 0.95:
        token = persist_fetch('token_usage').get('usage')
        price = round(token * 0.000617, 2)
        await send_friend_message(session, sender_id, text_message(f'目前总共消耗token：{token}个，约合￥{price}，GPT-4维护不易，可以对我发电哦~'), web_image_message('https://xhfs5.ztytech.com/CA107011/e6786e279d9a45079ca88e67c77df7b4.jpg'))

chatgpt = Plugin('chatgpt')
chatgpt.register_callback('group.@fumo@fumoP', group_message_handler)

chatgpt.register_callback('friend.P', friend_message_handler)
