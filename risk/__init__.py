'''
todo
'''

import datetime
import logging
import random

#-----------------------------------------------------------------------------#
# logging

logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------------#
# config

class SimulationConfig():
    def __init__(self):
        self._max_fight_rounds = 10_000

        # milliseconds since epoch
        epoch = datetime.datetime(1970, 1, 1)
        now = datetime.datetime.now()
        self._seed = int((now - epoch).total_seconds())

    @property
    def max_fight_rounds(self):
        return self._max_fight_rounds

    @max_fight_rounds.setter
    def max_fight_rounds(self, n):
        if n is not None:
            self._max_fight_rounds = n

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, new_seed):
        if new_seed is not None:
            self._seed = new_seed

    def to_dict(self):
        return {
            'seed': self.seed,
            'max-fight-rounds': self.max_fight_rounds
        }

#-----------------------------------------------------------------------------#

class Die():

    def __init__(self, seed):
        self._seed = seed
        random.seed(seed)

    @property
    def seed(self):
        return self._seed

    def throw(self, k=1):
        if k > 1:
            return [random.randint(1, 6) for _ in range(k)]
        else:
            return random.randint(1, 6)

class Simulation():
    '''
    todo
    '''

    def __init__(self, cfg):
        '''
        Initialize the simulation by setting up the datastructures
        '''

        # set general simulation-parameter
        self._die = Die(cfg.seed)
        self._max_fight_rounds = cfg.max_fight_rounds

        # set specific simulation-parameter
        self._ad_counts = {}
        # 1-3 attackers (att) vs 1-2 defenders (def)
        self._dice_per_att = 3
        self._dice_per_def = 2

        # fill win-counts as empty dict
        for i_att in range(self._dice_per_att):
            dict_att = {}
            for i_def in range(self._dice_per_def):
                # add empty counter-element for a-d-combination
                dict_att[Simulation.__key_def(i_def)] = {
                    'defended': 0,
                    'draw': 0,
                    'defeated': 0
                }
            self._ad_counts[Simulation.__key_att(i_att)] = dict_att

    #-------------------------------------------------------------------------#
    # getter

    @property
    def max_fight_rounds(self):
        return self._max_fight_rounds

    @property
    def dice_per_att(self):
        return self._dice_per_att

    @property
    def dice_per_def(self):
        return self._dice_per_def

    @property
    def dice_per_round(self):
        return self._dice_per_att + self._dice_per_def

    def __ad_counts(self, i_att, i_def):
        return self._ad_counts[self.__key_att(i_att)][self.__key_def(i_def)]

    @staticmethod
    def __key_att(a):
        return f'att={a+1}'

    @staticmethod
    def __key_def(d):
        return f'def={d+1}'

    #-------------------------------------------------------------------------#
    # simulation-pipeline

    def monte_carlo(self):
        logger.info(f'seed={self._die.seed}')

        # throw dice and count wins
        for _ in range(self.max_fight_rounds):
            self.run_one_iteration()

        return self._ad_counts

    def run_one_iteration(self):
        # throw dice and use them for all a-d-combinations
        # -> save random-calls
        # -> better performance
        dice_throws = self._die.throw(k=self.dice_per_round)

        # iterate through 1-3 attackers vs 1-2 defenders and count
        for i_att in range(self.dice_per_att):
            for i_def in range(self.dice_per_def):
                # "throw dice" (or use already thrown dice from above)
                attackers = dice_throws[0:(i_att+1)]
                defenders = dice_throws[(i_att+1):(i_att+i_def+2)]

                result = self.fight(attackers, defenders)
                self.update(i_att, i_def, result)

                logger.debug(f'att={attackers}')
                logger.debug(f'def={defenders}')
                logger.debug(f'result={result}')
                logger.debug('')

    @staticmethod
    def fight(attackers, defenders):
        '''
        Attackers have 1-3 dice-values, defenders 1-2, out of [1, 6].

        attackers: [a0, a1, a2]

        defenders: [d0, d1]
        '''
        attackers = sorted(attackers)
        defenders = sorted(defenders)
        result = {
            'defended': 0,
            'draw': 0,
            'defeated': 0
        }

        # count wins of each team
        defended = 0
        defeated = 0
        for i in range(min(len(attackers), len(defenders))):
            # increase i since running backwards
            # -> -1 is first element
            i += 1
            # if equal, defenders win
            if attackers[-i] > defenders[-i]:
                defeated += 1
            else:
                defended += 1

        # If one team has no wins, it has lost every 1on1-battle.
        if defended == 0:
            result['defeated'] += 1
        elif defeated == 0:
            result['defended'] += 1
        else:
            # If both teams have wins, also both teams have lost one unit.
            # -> no winner because only 2 defender-dice
            result['draw'] += 1

        return result

    def update(self, i_att, i_def, result):
        '''
        result should be a dict of keys { 'defended', 'draw', 'defeated' }
        '''

        ad_counts = self.__ad_counts(i_att, i_def)
        ad_counts['defended'] += result['defended']
        ad_counts['draw'] += result['draw']
        ad_counts['defeated'] += result['defeated']
