from django.db import models


class Rank(models.Model):
    CATEGORY = (
        ('speed', '速通'),
        ('score', '贪分'),
        ('challenge', '挑战')
    )

    game_id = models.IntegerField(verbose_name='游戏id')
    game_name = models.CharField(max_length=100, verbose_name='游戏名称')
    category = models.CharField(max_length=20, choices=CATEGORY, default='speed', verbose_name='游戏类型')
    video_url = models.CharField(max_length=254, verbose_name='录像地址')
    rank = models.IntegerField(default=1, verbose_name='排名')
    player = models.CharField(max_length=30, verbose_name='玩家')
    timestamp = models.CharField(max_length=30, blank=True, null=True, verbose_name='时长')
    video_date = models.CharField(max_length=30, blank=True, null=True, verbose_name='日期')
    platform = models.CharField(max_length=30, verbose_name='分类')
    hits = models.IntegerField(default=0, verbose_name='点击量')

    class Meta:
        db_table = 'rank'
        ordering = ['game_name', 'rank']
