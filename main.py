from core.app import App
# from plugins.kobe.kobe import kobe
# from plugins.happiness.happiness import happiness
# from plugins.battle.battle import battle
# from plugins.stopwatch.stopwatch import stopwatch
# from plugins.pray.pray import pray

from plugins.pat.pat import pat
from plugins.httpcat.httpcat import httpcat
from plugins.httpdog.httpdog import httpdog
from plugins.mahjong.mahjong import mahjong
from plugins.answer.answer import answer
from plugins.guess_npc.guess_npc import guess_npc
from plugins.tingpai.tingpai import tingpai
from plugins.coin.coin import coin
# from plugins.repeat.repeat import repeat
from plugins.score.score import score
from plugins.essence.essence import essence
from plugins.nudge.nudge import nudge
from plugins.chatgpt.chatgpt import chatgpt

from plugins.image.image import image
from plugins.genshin.genshin import genshin
from plugins.choosing_helper.choosing_helper import choosing_helper
from plugins.rua.rua import rua
from plugins.playmaze.playmaze import playmaze
from plugins.aidraw.aidraw import aidraw
from plugins.setu.setu import setu
from plugins.chinese_mahjong.chinese_mahjong import chinese_mahjong

bot = App()

# bot.register_plugin(kobe)
# bot.register_plugin(happiness)
# bot.register_plugin(stopwatch)
# bot.register_plugin(pray)

bot.register_plugin(pat)
bot.register_plugin(httpcat)
bot.register_plugin(httpdog)
bot.register_plugin(mahjong)
bot.register_plugin(answer)
bot.register_plugin(guess_npc)
bot.register_plugin(tingpai)
bot.register_plugin(coin)
# bot.register_plugin(repeat)
bot.register_plugin(score)
bot.register_plugin(essence)
bot.register_plugin(nudge)
bot.register_plugin(chatgpt)

bot.register_plugin(image)
bot.register_plugin(genshin)
bot.register_plugin(choosing_helper)
bot.register_plugin(rua)
bot.register_plugin(playmaze)

bot.register_plugin(aidraw)
bot.register_plugin(setu)
bot.register_plugin(chinese_mahjong)

bot.run()