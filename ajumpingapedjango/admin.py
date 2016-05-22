# -*- coding: utf-8 -*-
from django.contrib import admin
from ajumpingapedjango.models import GameBalance

class GameBalanceAdmin(admin.ModelAdmin):
    model = GameBalance
    max_num = 1
    list_display =('playerHorizontalSpeed', 'brainSpawDeltaY', 'bananaSpawDeltaY', 'jumpForce', 'startJumpForce',)
admin.site.register(GameBalance, GameBalanceAdmin)