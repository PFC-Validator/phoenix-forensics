#!/usr/bin/env python3
import unittest
from pipeline_utils import capture_status, display_amount, parse_coins

class AmountTests(unittest.TestCase):
    def test_single_coin(self):
        self.assertEqual(parse_coins('123uluna'), [{'amount': 123, 'denom': 'uluna'}])

    def test_multi_coin_is_not_dropped(self):
        self.assertEqual(parse_coins('123uluna,456ibc/ABC'), [
            {'amount': 123, 'denom': 'uluna'}, {'amount': 456, 'denom': 'ibc/ABC'},
        ])

    def test_invalid_amount_fails_closed(self):
        for value in ['', '1.5uluna', '12', 'uluna', '1uluna,']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_coins(value)

    def test_unknown_denom_is_not_assumed_six_decimals(self):
        result = display_amount(123456789, 'factory/terra1x/token')
        self.assertIsNone(result['display_amount'])
        self.assertEqual(result['base_amount'], '123456789')

class CaptureTests(unittest.TestCase):
    def test_truncation_is_explicit(self):
        row = capture_status('data/phoenix/Rose_treasury_transactions.json')
        self.assertFalse(row['complete'])
        self.assertEqual((row['saved'], row['reported_total'], row['missing']), (100, 171, 71))

    def test_complete_capture(self):
        row = capture_status('data/transfers/rebel_orbital_sender.json')
        self.assertTrue(row['complete'])
        self.assertEqual(row['saved'], 24)

    def test_zero_result_has_counter_queries(self):
        row = capture_status('data/phoenix/MB_prior_treasury_transactions.json')
        self.assertIn('counter-queries', row['classification'])
        self.assertIsNotNone(row['caution'])

if __name__ == '__main__':
    unittest.main()
