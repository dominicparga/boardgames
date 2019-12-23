import unittest
import logging

import risk

#-----------------------------------------------------------------------------#
# testing

class Risk(unittest.TestCase):

    def test_fight(self):
        # set general simulation-params and init sim
        params = {
            'max-fight-rounds': 1,
            'seed': 1577104599
        }
        sim = risk.Simulation(
            seed=params['seed'],
            max_fight_rounds=params['max-fight-rounds']
        )

        # dice_att, dice_def, expected_result
        expected = [
            ([2], [5], {'defended': 1, 'draw': 0, 'defeated': 0}),
            ([2], [5, 3], {'defended': 1, 'draw': 0, 'defeated': 0}),
            ([2, 5], [3], {'defended': 0, 'draw': 0, 'defeated': 1}),
            ([2, 5], [3, 3], {'defended': 0, 'draw': 1, 'defeated': 0}),
            ([2, 5, 3], [3], {'defended': 0, 'draw': 0, 'defeated': 1}),
            ([2, 5, 3], [3, 4], {'defended': 0, 'draw': 1, 'defeated': 0})
        ]

        # at least 3*2 cases should be tested
        self.assertTrue(len(expected) >= sim.dice_per_att * sim.dice_per_def)

        # simulate fights and check results
        for dice_att, dice_def, expected_result in expected:
            # sum of expected should be max-fight-rounds
            self.assertEqual(
                sim.max_fight_rounds,
                sum(expected_result.values())
            )

            result = sim.fight(
                attackers=dice_att.copy(),
                defenders=dice_def.copy()
            )
            self.assertDictEqual(
                expected_result, result,
                msg=f'attackers={dice_att} and defenders={dice_def}'
            )

if __name__ == '__main__':
    # init logging
    logging.basicConfig(level=logging.WARNING)
    # run tests
    unittest.main(verbosity=2)
