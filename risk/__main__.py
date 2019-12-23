'''
The main is parsing the cmdlines and calling respective modules.
'''

import os
import argparse
import datetime
import logging
import json

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

    @property
    def paths(self):
        return self._paths

CONSTANTS = Constants()

#-----------------------------------------------------------------------------#
# cmdline-parsing

def parse_cmdline():
    '''
    Parse cmdline-args and print help-msg if specified.
    '''

    #-------------------------------------------------------------------------#
    # define args and parse them

    description  = 'This little repo serves as handy tool to get information '
    description += 'in boardgames through calculation or simulation.'
    parser = argparse.ArgumentParser(description=description)

    # max-fight-rounds
    help_msg  = 'Defines the number of dice that should be thrown for the '
    help_msg += 'simulation.'
    parser.add_argument('-n', '--max-fight-rounds',
        metavar=('INT'),
        dest='max_fight_rounds',
        action='store',
        type=int,
        default=10_000,
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

    # export results, even if file exists
    help_msg  = 'Same as \'--export-results\' but forced '
    help_msg += '(removing existing file).'
    parser.add_argument('-of', '--export-results-forced',
        dest='is_exporting_results_forced',
        action='store_true',
        required=False,
        help=help_msg
    )

    # export results
    help_msg  = 'If set, the simulation-results will be exported to the '
    help_msg += 'specified path.'
    parser.add_argument('-o', '--export-results',
        dest='is_exporting_results',
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
    # finalize and return
    params = {'sim': {}}

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

    # max-fight-rounds
    params['sim']['max-fight-rounds'] = args.max_fight_rounds
    # seed
    if args.seed is not None:
        params['sim']['seed'] = args.seed
    else:
        # milliseconds since epoch
        epoch = datetime.datetime(1970, 1, 1)
        now = datetime.datetime.now()
        params['sim']['seed'] = int((now - epoch).total_seconds())
    # export results
    params['is_exporting_results'] = args.is_exporting_results
    params['is_exporting_results_forced'] = args.is_exporting_results_forced

    return params

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    # init logging
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    # extract params
    params = parse_cmdline()

    # check export-path before running simulation
    # (and wasting time if out-file exists)
    if not params['is_exporting_results_forced']:
        if params['is_exporting_results']:
            if os.path.exists(CONSTANTS.paths.risk_output):
                err_msg  = f'Output-file {CONSTANTS.paths.risk_output} does '
                err_msg += 'already exist.'
                logger.error(err_msg)
                exit(1)
            else:
                params['is_exporting_results_forced'] = True

    #-------------------------------------------------------------------------#
    # simulate

    sim = risk.Simulation(
        seed=params['sim']['seed'],
        max_fight_rounds=params['sim']['max-fight-rounds']
    )
    result = sim.monte_carlo()
    result['params'] = params['sim']

    # export results to a json-file
    if params['is_exporting_results_forced']:
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
