#!/usr/bin/env python

# -*-coding:utf-8 -*-

import unittest
import numpy_financial as npf
from cuffnote.mortgages import Mortgage

class TestBaseMortgage(unittest.TestCase):
    def setUp(self):
        self.purchase_price = 200000
        self.down_payment_percent = 0.2
        self.interest_rate = 0.03375
        self.start_date = (2021, 1, 1)
        self.years = 30
        self.num_yearly_pmts = 12
        self.loan = Mortgage(
            self.purchase_price,
            self.down_payment_percent,
            self.interest_rate,
            self.start_date,
            self.years,
            num_yearly_payments=self.num_yearly_pmts
        )
        
    def test_00_get_payment(self):
        self.assertAlmostEqual(
            self.loan.get_payment(),
            round(-1 * npf.pmt(self.interest_rate/self.num_yearly_pmts, self.num_yearly_pmts*self.years, self.purchase_price - 0.2*self.purchase_price), 2),
            2
        )


if __name__ == '__main__':
    unittest.main()