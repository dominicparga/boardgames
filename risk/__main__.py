'''
The main is parsing the cmdlines and calling respective modules.
'''

import os
import argparse
import datetime
import logging

import risk

#-----------------------------------------------------------------------------#
# constants

ROOT = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
RESOURCES = os.path.join(ROOT, 'resources')
CONSTANTS = {
    'paths': {
        'root': ROOT,
        'res': RESOURCES
    }
}

def parse_cmdline():
    '''
    Parse cmdline-args and print help-msg if specified.
    '''

    #-------------------------------------------------------------------------#
    # define args and parse them

    description = 'This little repo serves as handy tool to get information in '
    description += 'boardgames through calculation or simulation.'
    parser = argparse.ArgumentParser(description=description)

    # max-fight-rounds
    help_msg = 'Defines the number of dice that should be thrown for the '
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
    # help_msg = 'If set, the simulation calculates an approximation via '
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
    params = {}

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
    params['max-fight-rounds'] = args.max_fight_rounds
    # seed
    if args.seed is not None:
        params['seed'] = args.seed
    else:
        # milliseconds since epoch
        epoch = datetime.datetime(1970, 1, 1)
        now = datetime.datetime.now()
        params['seed'] = int((now - epoch).total_seconds())

    return params

if __name__ == '__main__':
    # init logging
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    params = parse_cmdline()
    ad_counts = risk.run_sim(params)

    # calculate percentages and prepare output
    logger.info(ad_counts)
