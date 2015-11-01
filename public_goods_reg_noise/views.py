# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Contribute(Page):
    form_model = models.Player
    form_fields = ['contribution']

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_records()

class Punishment(Page):
    form_model = models.Player
    form_fields = ['punishment_p1', 'punishment_p2', 'punishment_p3']

    
class ResultsWaitPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
   pass



page_sequence = [
    Contribute,
    ResultsWaitPage,
    Punishment,
    ResultsWaitPage2,
    Results
]
