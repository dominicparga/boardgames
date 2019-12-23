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

    parser = argparse.ArgumentParser(description=
        'This little repo serves as handy tool to get information in boardgames through  '
        'calculation or simulation.'
    )

    help_msg = 'Defines the number of dice that should be thrown.'
    parser.add_argument('-n', '--max-fight-rounds',
        metavar=('MAX_DICE_THROWS'),
        action='store',
        type=int,
        default=100,
        required=False,
        help=help_msg
    )

    help_msg = 'Defines the seed for the RNG.'
    parser.add_argument('-s', '--seed',
        metavar=('SEED'),
        action='store',
        type=int,
        required=False,
        help=help_msg
    )

    help_msg = 'Sets the logging-level'
    parser.add_argument('-log', '--logging-level',
        metavar=('LOGGING_LEVEL'),
        choices=['debug', 'info', 'warning', 'error'],
        required=False,
        help=help_msg
    )

    args = parser.parse_args()

    #-------------------------------------------------------------------------#
    # finalize and return

    params = {}

    # logging-level
    if args.logging_level:
        if args.logging_level == 'debug':
            args.logging_level = logging.DEBUG
        elif args.logging_level == 'info':
            args.logging_level = logging.INFO
        elif args.logging_level == 'warning':
            args.logging_level = logging.WARNING
        elif args.logging_level == 'error':
            args.logging_level = logging.ERROR
        # set logging-levels
        logging.getLogger(__name__).setLevel(args.logging_level)
        logging.getLogger(risk.__name__).setLevel(args.logging_level)

    # max-fight-rounds
    params['max-fight-rounds'] = args.max_fight_rounds
    # seed
    if args.seed:
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

    params = parse_cmdline()
    risk.run_sim(params)
