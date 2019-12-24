'''
The main is parsing the cmdlines, starting the simulation and exporting
the results, if wished.
'''

import argparse
import json
import logging
import os

import risk

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
        self._boardgame = 'Risk'

    @property
    def paths(self):
        return self._paths

    @property
    def boardgame(self):
        return self._boardgame

CONSTANTS = Constants()

#-----------------------------------------------------------------------------#
# config

class Config():
    def __init__(self):
        self._sim = risk.SimulationConfig()
        self._is_output_enabled = False
        self._is_output_forced = False

    @property
    def sim(self):
        return self._sim

    @property
    def is_output_enabled(self):
        return self._is_output_enabled

    @is_output_enabled.setter
    def is_output_enabled(self, value):
        self._is_output_enabled = value

    @property
    def is_output_forced(self):
        return self._is_output_forced

    @is_output_forced.setter
    def is_output_forced(self, value):
        self._is_output_forced = value

#-----------------------------------------------------------------------------#
# cmdline-parsing

def parse_cmdline():
    '''
    Parse cmdline-args and print help-msg if specified.
    '''

    #-------------------------------------------------------------------------#
    # define args and parse them

    description  = 'Have you ever asked yourself in boardgame \'Risk\', what '
    description += 'the winning-chance of your attackers/defenders is?'
    parser = argparse.ArgumentParser(description=description)

    # max-fight-rounds
    help_msg  = 'Defines the number of dice that should be thrown for the '
    help_msg += 'simulation.'
    parser.add_argument('-n', '--max-fight-rounds',
        metavar=('INT'),
        dest='max_fight_rounds',
        action='store',
        type=int,
        required=False,
        help=help_msg
    )

    # seed
    help_msg = 'Defines the seed for the RNG.'
    parser.add_argument('-s', '--seed',
        metavar=('INT'),
        dest='seed',
        action='store',
        type=int,
        required=False,
        help=help_msg
    )

    # enable output
    help_msg  = 'If set, the simulation-results will be exported to the '
    help_msg += 'specified path.'
    parser.add_argument('-o', '--enable-output',
        dest='is_output_enabled',
        action='store_true',
        required=False,
        help=help_msg
    )

    # force output, even if file exists
    help_msg  = 'Same as \'--enable-output\' but forced '
    help_msg += '(removing existing file).'
    parser.add_argument('-of', '--force-output',
        dest='is_output_forced',
        action='store_true',
        required=False,
        help=help_msg
    )


    # logging-level
    help_msg = 'Sets the logging-level'
    parser.add_argument('-log', '--logging-level',
        metavar=('STRING'),
        dest='logging_level',
        choices=['debug', 'info', 'warning', 'error'],
        required=False,
        help=help_msg
    )
    help_msg = 'Sets the logging-level to \'info\' overwriting other flags.'
    parser.add_argument('-v', '--verbose',
        dest='verbose',
        action='store_true',
        required=False,
        help=help_msg
    )

    # approximation vs analytical solution
    # help_msg  = 'If set, the simulation calculates an approximation via '
    # help_msg += 'monte-carlo instead of the analytical correct solution. '
    # help_msg += 'Default is true since analytical solution is not supported '
    # help_msg += 'yet.'
    # parser.add_argument('-mc', '--monte-carlo',
    #     dest='use_mc',
    #     action='store_true',
    #     required=False,
    #     default=True,
    #     help=help_msg
    # )

    args = parser.parse_args()

    #-------------------------------------------------------------------------#
    # logging-level

    if args.verbose:
        args.logging_level = logging.INFO
    elif args.logging_level is not None:
        if args.logging_level == 'debug':
            args.logging_level = logging.DEBUG
        elif args.logging_level == 'info':
            args.logging_level = logging.INFO
        elif args.logging_level == 'warning':
            args.logging_level = logging.WARNING
        elif args.logging_level == 'error':
            args.logging_level = logging.ERROR
    else:
        args.logging_level = logging.WARNING
    # set logging-levels
    logging.getLogger(__name__).setLevel(args.logging_level)
    logging.getLogger(risk.__name__).setLevel(args.logging_level)

    #-------------------------------------------------------------------------#
    # finalize and return

    cfg = Config()

    cfg.sim.max_fight_rounds = args.max_fight_rounds
    cfg.sim.seed = args.seed
    cfg.is_output_enabled = args.is_output_enabled
    cfg.is_output_forced = args.is_output_forced

    return cfg

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    # init logging
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    # extract params
    cfg = parse_cmdline()

    # check export-path before running simulation
    # (and wasting time if out-file exists)
    if not cfg.is_output_forced:
        if cfg.is_output_enabled:
            if os.path.exists(CONSTANTS.paths.risk_output):
                err_msg  = f'Output-file {CONSTANTS.paths.risk_output} does '
                err_msg += 'already exist.'
                logger.error(err_msg)
                exit(1)
            else:
                cfg.is_output_forced = True

    #-------------------------------------------------------------------------#
    # simulate

    sim = risk.Simulation(cfg.sim)
    result = sim.monte_carlo()

    #-------------------------------------------------------------------------#
    # export results to a json-file

    result = {'data': result}
    result['config'] = cfg.sim.to_dict()
    result['boardgame'] = CONSTANTS.boardgame

    if cfg.is_output_forced:
        with open(CONSTANTS.paths.risk_output, 'w') as json_file:
            json.dump(result, json_file, indent=4)

    # # calculate percentages
    # for dict_def in result.values():
    #     for counts in dict_def.values():
    #         counts['defended'] /= float(sim.max_fight_rounds)
    #         counts['draw'] /= float(sim.max_fight_rounds)
    #         counts['defeated'] /= float(sim.max_fight_rounds)

    # prepare output
    logger.info(result)
