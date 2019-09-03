from django.views.generic import View
from django.shortcuts import render

from .models import Rank


class RankView(View):
    def get(self, request):
        category = request.GET.get('category', 'speed')
        rank = request.GET.get('rank')
        game_name = request.GET.get('game_name')
        player = request.GET.get('player')
        hits = request.GET.get('hit')
        ranks = Rank.objects.filter(category__icontains=category)
        if rank:
            ranks = ranks.order_by('rank')
        elif game_name:
            ranks = ranks.order_by('game_name')
        elif player:
            ranks = ranks.order_by('player')
        elif hits:
            ranks = ranks.order_by('hits')
        context = {
            'ranks': ranks,
            'category': category,
            'rank': rank,
            'game_name': game_name,
            'player': player,
            'hits': hits,
        }
        return render(request, 'index.html', context=context)


class BossView(View):
    def get(self, request):
        ranks = Rank.objects.filter(rank=1).order_by('game_name', 'category')
        context = {
            'ranks': ranks
        }
        return render(request, 'boss.html', context=context)
