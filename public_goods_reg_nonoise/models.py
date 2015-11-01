# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
import otree.constants
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_reg_nonoise'
    players_per_group = 3
    num_rounds = 50

    # define more constants here
    endowment = c(20)
    efficiency_factor = 0.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor
        for p in self.get_players():
            p.income = Constants.endowment - p.contribution + self.individual_share
            p.cost = p.punishment_p1 + p.punishment_p2 + p.punishment_p3
            if p.id_in_group == 1:
                p.deduction = sum([q.punishment_p1 for q in p.other_player()])
            if p.id_in_group == 2:
                p.deduction = sum([q.punishment_p2 for q in p.other_player()])
            if p.id_in_group == 3:
                p.deduction = sum([q.punishment_p3 for q in p.other_player()])
            if p.income >= (3 * p.deduction):#ここは解釈が正しいか確信がない
                p.payoff = p.income - p.cost - 3 * p.deduction
            if p.income < (3 * p.deduction):
                p.payoff = 0 - p.cost
class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    contribution = models.CurrencyField(choices=[0,Constants.endowment],widget=widgets.RadioSelect())
    punishment_p1 = models.CurrencyField(min=0, max=50)
    punishment_p2 = models.CurrencyField(min=0, max=50)
    punishment_p3 = models.CurrencyField(min=0, max=50)
    income = models.PositiveIntegerField(min=0, max=90)
    cost  = models.PositiveIntegerField(min=0, max=150)
    deduction = models.PositiveIntegerField(min=0, max=150)
    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()

    def set_payoff(self):
        self.income = Constants.endowment - self.contribution + group.individual_share
        self.cost = self.punishment_for_p1 + self.punishment_for_p2 + self.punishment_for_p3
        self.deduction = sum([q.punishment_p1 for q in self.other_player()])

    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        if self.id_in_group == 2:
            return 'Player 2'
        if self.id_in_group == 3:
            return 'Player 3'