from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

dic = {
    88: "大四喜 大三元 绿一色 九莲宝灯 四杠 连七对 十三幺".split(),
    64: "清幺九 小四喜 小三元 字一色 四暗刻 一色双龙会".split(),
    48: "一色四同顺 一色四节高".split(),
    32: "一色四步高 三杠 混幺九".split(),
    24: "七对 七星不靠 全双刻 清一色 一色三同顺 一色三节高 全大 全中 全小".split(),
    16: "清龙 三色双龙会 一色三步高 全带五 三同刻 三暗刻".split(),
    12: "全不靠 组合龙 大于五 小于五 三风刻".split(),
    8: "花龙 推不倒 三色三同顺 三色三节高 无番和 妙手回春 海底捞月 杠上开花 抢杠和 双暗杠".split(),
    6: "碰碰和 混一色 三色三步高 五门齐 全求人 一明一暗杠 双箭刻".split(),
    4: "全带幺 不求人 双明杠 和绝张".split(),
    2: "箭刻 圈风刻 门风刻 门前清 平和 四归一 双同刻 双暗刻 暗杠 断幺".split(),
    1: "一般高 喜相逢 连六 老少副 幺九刻 明杠 缺一门 无字 边张 坎张 单钓将 自摸 花牌".split(),
}

against = [
    ('大四喜', '自风刻'),
    ('大四喜', '圈风刻'),
    ('大四喜', '碰碰和'),
    ('大三元', '双箭刻'),
    ('大三元', '箭刻'),
    ('大三元', '小三元'),
    ('绿一色', '混一色'),
    ('九莲宝灯', '不求人'),
    ('九莲宝灯', '清一色'),
    ('九莲宝灯', '门前清'),
    ('四杠', '碰碰和'),
    ('四杠', '单钓'),
    ('连七对', '清一色'),
    ('连七对', '七对'),
    ('连七对', '平和'),
    ('十三幺', '五门齐'),
    ('十三幺', '门前清'),
    ('十三幺', '不求人'),
    ('十三幺', '单钓'),
    ('清幺九', '碰碰和'),
    ('清幺九', '混幺九'),
    ('清幺九', '同刻'),
    ('清幺九', '无字'),
    ('小四喜', '自风刻'),
    ('小四喜', '圈风刻'),
    ('小四喜', '三风刻'),
    ('小三元', '箭刻'),
    ('小三元', '双箭刻'),
    ('字一色', '碰碰和'),
    ('四暗刻', '门前清'),
    ('四暗刻', '碰碰和'),
    ('四暗刻', '不求人'),
    ('一色双龙会', '老少副'),
    ('一色双龙会', '一般高'),
    ('一色双龙会', '清一色'),
    ('一色双龙会', '平和'),
    ('一色四同顺', '一般高'),
    ('一色四同顺', '一色三节高'),
    ('一色四同顺', '四归一'),
    ('一色四节高', '一色三同顺'),
    ('一色四节高', '碰碰和'),
    ('混幺九', '碰碰和'),
    ('混幺九', '全带幺'),
    ('七对', '门前清'),
    ('七对', '不求人'),
    ('七对', '单钓'),
    ('七星不靠', '全不靠'),
    ('全双刻', '碰碰和'),
    ('全双刻', '断幺'),
    ('清一色', '无字'),
    ('清一色', '混一色'),
    ('一色三同顺', '一色三节高'),
    ('一色三同顺', '一般高'),
    ('一色三节高', '一色三同顺'),
    ('全大', '大于五'),
    ('全中', '断幺'),
    ('全小', '小于五'),
    ('三色双龙会', '喜相逢'),
    ('三色双龙会', '老少副'),
    ('三色双龙会', '平和'),
    ('全带五', '断幺'),
    ('全不靠', '五门齐'),
    ('全不靠', '不求人'),
    ('全不靠', '门前清'),
    ('大于五', '无字'),
    ('小于五', '无字'),
    ('推不倒', '缺一门'),
    ('三色三同顺', '喜相逢'),
    ('妙手回春', '自摸'),
    ('杠上开花', '自摸'),
    ('抢杠和', '和绝张'),
    ('全求人', '单钓'),
    ('不求人', '自摸'),
    ('平和', '无字')
]

async def handler(session: str, group_id: int, sender_id: int, message):
    if message[1] == "国标番种":
        await send_group_message(session, group_id, text_message("\n".join([f"{i}番：{' '.join(dic[i])}" for i in dic])))
        return
    
    unrecog = []
    autoignore = []
    message = message[1].split()
    
    for i in against:
        if i[0] in message and i[1] in message:
            message = [k for k in message if k != i[1]]
            autoignore.append(i[1])
    
    cnt = 0
    for i in message:
        for k in dic:
            if i in dic[k]:
                cnt += k
                break
        else:
            unrecog.append(i)
    if cnt != 0:
        if unrecog != []:
            await send_group_message(session, group_id, text_message(f'未识别：{unrecog}'))
        if autoignore != []:
            await send_group_message(session, group_id, text_message(f'自动去除：{autoignore}'))

        if cnt >= 8:
            await send_group_message(session, group_id, text_message(f'{cnt}番，点和({cnt + 8}, 8)，自摸{cnt + 8}all.'))
        else:
            await send_group_message(session, group_id, text_message(f'{cnt}番，诈胡-10all.'))

chinese_mahjong = Plugin('chinese_mahjong')
chinese_mahjong.register_callback('group.@fumoP', handler)