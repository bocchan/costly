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
    name_in_url = 'public_goods_nopunishment_noise'
    players_per_group = 3
    num_rounds = 30

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
        	p.payoff = Constants.endowment - p.contribution + self.individual_share
        	x = random.random()
        	if x < 0.1:
        		p.record = 0
        	if x >= 0.1:
        		p.record = p.contribution
            

class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    contribution = models.CurrencyField(choices=[0,Constants.endowment],widget=widgets.RadioSelect())
    record = models.CurrencyField()
    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()

