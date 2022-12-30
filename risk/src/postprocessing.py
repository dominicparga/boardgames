'''
todo
'''

import argparse
import json
import os

import postprocessing

#-----------------------------------------------------------------------------#
# constants

class Constants():
    class __Paths():
        def __init__(self):
            self._root = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
            self._build = os.path.join(self._root, '..', 'build')
            self._risk_output = os.path.join(self._build, 'risk.json')

        @property
        def root(self):
            return self._root

        @property
        def build(self):
            return self._build

        @property
        def risk_output(self):
            return self._risk_output

    def __init__(self):
        self._paths = Constants.__Paths()

    @property
    def paths(self):
        return self._paths

CONSTANTS = Constants()

#-----------------------------------------------------------------------------#
# config

class Config():
    def __init__(self):
        self._input_path = None

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, new_path):
        self._input_path = new_path

#-----------------------------------------------------------------------------#
# risk

def postprocess_risk(result):
    cfg = result['config']
    data = result['data']

    n = cfg['max-fight-rounds']

    #-------------------------------------------------------------------------#
    # chance to win/draw/lose

    # print README-result in markdown-syntax

    print('| winner (%) |   defenders   |    both     |   attackers   |')
    print('|:----------:|--------------:|------------:|--------------:|')

    for key_att, dict_def in data.items():
        # get number of attackers
        # since key_att looks like 'att=1'
        a = key_att[-1]
        for key_def, counts in dict_def.items():
            counts = counts.copy()
            # get number of defenders
            # since key_def looks like 'def=1'
            d = key_def[-1]
            # calculate percentages from counts
            # and prepare print and find winner
            for key, value in counts.items():
                counts[key] = f'{(value / n * 100):2.0f}'
            # add prefixes for winner
            winner_decorator = lambda v: f'(*) {v}'
            loser_decorator  = lambda v: f'    {v}'
            for i, key in enumerate(sorted(counts.keys(), key=counts.get)):
                # sorted returns in ascending order
                # if i is last element -> winner
                if i is len(counts.keys())-1:
                    counts[key] = f'{winner_decorator(counts[key])}'
                else:
                    counts[key] = f'{loser_decorator(counts[key])}'
            # actually print table-row
            defended = counts['defended']
            draw = counts['draw']
            defeated = counts['defeated']
            print(f'|  `{a}>` `({d}` |     {defended}    |    {draw}   |     {defeated}    |')

    #-------------------------------------------------------------------------#
    # chance to lose at least one unit

    print()

    # print README-result in markdown-syntax
    print('| losing >= 1 unit (%) |   defenders   |   attackers   |')
    print('|:--------------------:|--------------:|--------------:|')

    for key_att, dict_def in data.items():
        # get number of attackers
        # since key_att looks like 'att=1'
        a = key_att[-1]
        for key_def, counts in dict_def.items():
            counts = counts.copy()
            # get number of defenders
            # since key_def looks like 'def=1'
            d = key_def[-1]
            # sum up opposite counts to get chance of losing >= 1 unit
            sorted_keys = sorted(counts.keys(), key=counts.get)
            counts_lut = counts.copy()
            for i, k_i in enumerate(sorted_keys):
                loss_chance = 0
                # actually sum up opposite counts
                for j, k_j in enumerate(sorted_keys):
                    if i != j:
                        loss_chance += counts_lut[k_j]
                counts[k_i] = loss_chance
            # calculate percentages from counts
            # and prepare print and find winner
            for key, value in counts.items():
                counts[key] = f'{(value / n * 100):2.0f}'
            # actually print table-row
            defended = counts['defended']
            defeated = counts['defeated']
            print(f'|      `{a}>` `({d}`       |       {defended}      |       {defeated}      |')

#-----------------------------------------------------------------------------#
# cmdline-parsing

def parse_cmdline():
    '''
    Parse cmdline-args and print help-msg if specified.
    '''

    #-------------------------------------------------------------------------#
    # define args and parse them

    description  = 'This tool takes simulation-results and processes it, '
    description += 'e.g. for visualization.'
    parser = argparse.ArgumentParser(description=description)

    # input-path
    help_msg = 'Defines the input-path of the simulation-file.'
    parser.add_argument('-i', '--input',
        metavar=('PATH'),
        dest='input_path',
        action='store',
        type=str,
        required=True,
        help=help_msg
    )

    args = parser.parse_args()

    #-------------------------------------------------------------------------#
    # finalize and return

    cfg = Config()

    cfg.input_path = args.input_path

    return cfg

#-----------------------------------------------------------------------------#
# main

if __name__ == '__main__':
    # extract params
    cfg = parse_cmdline()

    if not os.path.exists(cfg.input_path):
        print(f'ERROR: File of input-path {cfg.input_path} does not exist.')
        exit(1)

    result = None
    with open(cfg.input_path) as json_file:
        result = json.load(json_file)

    boardgame = result['boardgame']
    if boardgame == 'Risk':
        postprocess_risk(result)
    else:
        print(f'Unsupported boardgame {boardgame}')
