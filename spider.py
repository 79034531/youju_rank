import time
import threading
import requests
import pymysql
from lxml import etree


class Spider(object):
    """
    用来爬取游聚游戏平台的排行榜
    """
    domain = 'http://ranking.gotvg.com'  # 游聚游戏平台排行榜地址
    # 一共有3个分类，分别是速通、贪分、挑战
    game_list_url = 'http://ranking.gotvg.com/Index/game/game/{}/category/{}/tag/0/mode/0/role/0.html'
    speed = 'speed'  # 速通分类
    score = 'score'  # 贪分分类
    challenge = 'challenge'  # 挑战分类

    def get_speed_rank(self, start_page=1, end_page=1000, category='speed'):
        """
        默认爬取前1000个游戏的内容。分类默认是速通（因为这个类型的投稿人数最多）
        :param start_page: 开始的页码
        :param end_page: 结束的页码
        :param category: 游戏的分类
        :return: None
        """
        connection = pymysql.connect(
            host='127.0.0.1', user='root', passwd='root', db='youju_rank', port=3306, charset='utf8')  # 连接数据库
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)  # 创建数据库游标
        # 爬取前1000页的内容，需要对range的第二个参数的值 + 1
        for i in range(start_page, end_page + 1):
            response = requests.get(self.game_list_url.format(i, category), timeout=(3, 7))  # 访问页面，增加超时判定
            text = response.text  # 保存响应的文本
            html = etree.HTML(text)  # 将文本转换为HTML的对象
            game_name = html.xpath(".//div[@id='game-info']/h2[@class='name']/text()")  # 游戏标题
            # 有的游戏可能被下架了，这里需要判断一下，可以根据标题来判断，也可以根据Not Found来判断。我这里使用的标题
            if game_name and game_name[0] != '找不到游戏了:(':
                video_list = html.xpath(".//div[@id='video-list']/a")  # 获取到所有的排行
                for video in video_list:
                    video_url = video.xpath("./@href")  # 排行榜录像url。这里这个值是唯一值
                    video_url = self.domain + video_url[0] if video_url else ''  # 使用三目运算，防止取0操作的时候报错
                    rank = video.xpath(".//tr[3]//span/text()")  # 名次
                    rank = rank[0] if rank else ''
                    player = video.xpath(".//div[@class='p1']/a/text()")  # 玩家
                    player = player[0] if player else ''
                    timestamp = video.xpath(".//span[@class='score']/text()")  # 时长
                    timestamp = timestamp[0] if timestamp else ''
                    video_date = video.xpath(".//tr[4]/td[@class='center white'][2]/a/text()")  # 日期
                    video_date = video_date[0] if video_date else ''
                    platform = video.xpath(".//tr[4]/td[@class='center white'][1]/a/text()")  # 平台
                    platform = platform[0] if platform else ''
                    hits = video.xpath(".//div[@class='video-hits']/text()")  # 热度
                    hits = hits[0] if hits else ''
                    cursor.execute("SELECT * FROM rank WHERE video_url = %s", (video_url,))  # 查询链接是否存在
                    result = cursor.fetchone()  # 用来测试是否有这个数据
                    # 没有就添加
                    if not result:
                        cursor.execute(
                            "INSERT INTO rank (game_id, game_name, category, video_url, rank, player, `timestamp`, video_date, platform, hits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                            (i, game_name, category, video_url, rank, player, timestamp, video_date, platform, hits)
                        )  # 映射插入语句
                        connection.commit()  # 提交数据
                        print(f'游戏：{platform}{game_name[0]}-{category}添加成功，玩家：{player}，游戏时长：{timestamp}，地址：{video_url}')
                    # 有的话，更新。因为点击数会增加
                    else:
                        cursor.execute(
                            "UPDATE rank SET game_id = %s, game_name = %s, category = %s, rank = %s, player = %s, `timestamp` = %s, video_date = %s, platform = %s, hits = %s WHERE video_url = %s",
                            (i, game_name, category, rank, player, timestamp, video_date, platform, hits, video_url)
                        )  # 映射更新语句
                        connection.commit()  # 提交数据
                        print(f'游戏：{platform}{game_name[0]}-{category}更新成功，玩家：{player}，游戏时长：{timestamp}，地址：{video_url}')
            print(f'{category}正在查询id为{i}的游戏……')
            time.sleep(0.3)  # 防止网站压力过大，睡眠0.3秒


def speed_spider():
    """
    用来爬取速通分类的数据
    :return: None
    """
    spider = Spider()
    spider.get_speed_rank(category=spider.speed)


def score_spider():
    """
    用来爬取贪分分类的数据
    :return: None
    """
    spider = Spider()
    spider.get_speed_rank(category=spider.score)


def challenge_spider():
    """
    用来爬取挑战分类的数据
    :return: None
    """
    spider = Spider()
    spider.get_speed_rank(category=spider.challenge)


def run():
    """
    用来开启多线程
    :return: None
    """
    threading.Thread(target=speed_spider).start()
    threading.Thread(target=score_spider).start()
    threading.Thread(target=challenge_spider).start()


if __name__ == '__main__':
    run()  # 运行
