#!/usr/bin/env python

# -*-coding:utf-8 -*-

import unittest
import pandas as pd
from cuffnote.mortgages import Mortgage, ExtraMonthlyPrincipal, AnnualLumpPayment


class TestAnnualLumpPayment(unittest.TestCase):
    
    def setUp(self):
        # base mortgage
        self.purhase_price = 200000
        self.down_payment_percent = 0.2
        self.down_payment = self.purhase_price * self.down_payment_percent
        self.loan_amount = self.purhase_price - self.down_payment
        self.interest_rate = 0.03375
        self.start_date = '2021-1-1'
        self.years = 30
        self.num_yearly_pmts = 12
        # instantiate base mortgage
        self.loan = Mortgage(
            self.purhase_price,
            self.down_payment_percent,
            self.interest_rate,
            self.start_date,
            self.years,
            num_yearly_payments=self.num_yearly_pmts
        )
        # extra principal attributes
        self.xtra_principal = 500
        # instantiate mortgage with extra principal
        self.loan_xtra_prncpl = ExtraMonthlyPrincipal(
            self.loan,
            self.xtra_principal
        )
        # annual lump payment
        self.annual_payment = 10000
        self.annual_payment_month = 12
        # instantiate base mortgage w/ annual lump payment
        self.base_alp = AnnualLumpPayment(
            self.loan,
            self.annual_payment,
            self.annual_payment_month
        )
        # instantiate mortgage w/ extra mo. pmts + annual lump
        self.loan_xmp_alp = AnnualLumpPayment(
            self.loan_xtra_prncpl,
            self.annual_payment,
            self.annual_payment_month
        )
        
    def test_00_init_from_base_mortgage(self):
        self.assertEqual(
            0.0,
            self.base_alp.get_extra_principal()
        )
        
    def test_01_init_from_extramonthlyprincipal(self):
        self.assertEqual(
            self.xtra_principal,
            self.loan_xmp_alp.get_extra_principal()
        )
        
    def test_02_get_annual_payment(self):
        self.assertEqual(
            self.annual_payment,
            self.loan_xmp_alp.get_annual_payment()
        )
        
    def test_03_set_annual_payment(self):
        self.loan_xmp_alp.set_annual_payment(12000)
        self.assertEqual(
            12000,
            self.loan_xmp_alp.get_annual_payment()
        )
        
    def test_04_get_annual_payment_month(self):
        self.assertEqual(
            self.annual_payment_month,
            self.loan_xmp_alp.get_annual_payment_month()
        )
        
    def test_05_set_annual_payment_month(self):
        self.loan_xmp_alp.set_annual_payment_month(5)
        self.assertEqual(
            5,
            self.loan_xmp_alp.get_annual_payment_month()
        )
        
    def test_06_get_amortization_table(self):
        self.assertIsInstance(
            self.loan_xmp_alp.get_amortization_table(),
            pd.DataFrame
        )
        

if __name__ == '__main__':
    unittest.main()