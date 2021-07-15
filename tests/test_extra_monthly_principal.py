#!/usr/bin/env python

# -*-coding:utf-8 -*-

import unittest
import numpy as np
import numpy_financial as npf
import datetime as date
import pandas as pd
from cuffnote.mortgages import Mortgage, ExtraMonthlyPrincipal


class TestExtraMonthlyPrincipal(unittest.TestCase):
    def setUp(self):
        # base mortgage attributes
        self.purhase_price = 200000
        self.down_payment_percent = 0.2
        self.down_payment = self.purhase_price * self.down_payment_percent
        self.loan_amount = self.purhase_price - self.down_payment
        self.interest_rate = 0.03375
        self.start_date = (2021, 1, 1)
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
        
    def test_00_get_payment_inheritance(self):
        self.assertEqual(
            self.loan.get_payment(),
            self.loan_xtra_prncpl.get_payment()
        )
        
    def test_01_get_extra_principal(self):
        self.assertEqual(
            self.xtra_principal,
            self.loan_xtra_prncpl.get_extra_principal()
        )
        
    def test_02_set_extra_principal(self):
        self.loan_xtra_prncpl.set_extra_principal(400)
        self.assertEqual(
            400,
            self.loan_xtra_prncpl.get_extra_principal()
        )
        
    def test_03a_get_amortization_table_df_instance(self):
        self.assertIsInstance(
            self.loan_xtra_prncpl.get_amortization_table(),
            pd.DataFrame
        )
        
    def test_03b_get_amortization_table_extra_principal_col(self):
        self.assertIn(
            'Extra Principal',
            self.loan_xtra_prncpl.get_amortization_table().columns
        )
        
    def test_03c_get_amortization_table_equal_extra_principal(self):
        self.assertEqual(
            self.loan_xtra_prncpl.get_extra_principal(),
            self.loan_xtra_prncpl.get_amortization_table().loc[1, 'Extra Principal']
        )
        
    def test_03d_get_amortization_table_start_date(self):
        new_extra_start_date = self.loan_xtra_prncpl.get_payment_range()[12].strftime('%Y-%m-%d')
        atable_extra_prncpl_shifted = self.loan_xtra_prncpl.get_amortization_table(new_extra_start_date)
        self.assertEqual(
            0,
            atable_extra_prncpl_shifted.loc[12, 'Extra Principal']
        )
        self.assertEqual(
            self.loan_xtra_prncpl.get_extra_principal(),
            atable_extra_prncpl_shifted.loc[13, 'Extra Principal']
        )
        

if __name__ == '__main__':
    unittest.main()