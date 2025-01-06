from sdk.send_message import send_group_message
from core.plugin import Plugin
from sdk.nudge import group_nudge
from sdk.user import group_user_list
import time

async def handler(session: str, group_id: int, sender_id: int, message):
    if message[1] == "戳我":
        await group_nudge(session, group_id, sender_id)
    if message[1] == "戳所有人" and sender_id == 2530469979:
        user_list = group_user_list(session, group_id)
        for user in user_list:
            await group_nudge(session, group_id, user)
            time.sleep(0.5)

def checker(group_id: int, sender_id: int, message):
    return message[1][0] == "戳"


async def handler2(session: str, group_id: int, sender_id: int, message):
    await group_nudge(session, group_id, message[2])

def checker2(group_id: int, sender_id: int, message):
    return message[1] == "戳"

nudge = Plugin('nudge')
nudge.register_callback('group.@fumoP', handler, checker)
nudge.register_callback('group.@fumoP@', handler2, checker2)
nudge.register_callback('group.@fumoP@fumo', handler2, checker2)