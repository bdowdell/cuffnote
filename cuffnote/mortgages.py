import numpy as np
import numpy_financial as npf
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class Mortgage:
    
    def __init__(self, purchase_price, down_payment_percent, interest_rate, years, num_yearly_payments, start_date):
        # initialize instance variables
        self.purchase_price = purchase_price
        self.down_payment_percent = down_payment_percent
        self.interest_rate = interest_rate
        self.years = years
        self.num_yearly_pmts = num_yearly_payments
        self.start_year, self.start_month, self.start_day = start_date
        self.start_date = (date(self.start_year, self.start_month, self.start_day))
        # calculate down payment and starting loan amount
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        # determine monthly payment
        self.payment = self.get_payment()
        self.payment_range = self.get_payment_range()
        
    def get_payment(self):
        return round(-1 * npf.pmt(self.interest_rate/self.num_yearly_pmts, self.years*self.num_yearly_pmts, self.loan_amount), 2)
    
    def get_purchase_price(self):
        return self.purchase_price
    
    def set_purchase_price(self, purchase_price):
        self.purchase_price = purchase_price
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        self.payment = self.get_payment()
        print(f"Purchase price updated to: ${self.purchase_price:,.2f}\n\
        New monthly payment is: ${self.payment:,.2f}")
        
    def get_down_payment_percent(self):
        return self.down_payment_percent
    
    def set_down_payment_percent(self, down_payment_percent):
        self.down_payment_percent = down_payment_percent
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        self.payment = self.get_payment()
        print(f'Down payment percentage updated to {self.down_payment_percent:.2%} which is ${self.down_payment:3,.2f}\n\
        The new monthly payment is ${self.payment:3,.2f}')
        
    def get_down_payment(self):
        return self.down_payment
    
    def set_down_payment(self, down_payment):
        self.down_payment = down_payment
        self.loan_amount = self.purchase_price - self.down_payment
        self.down_payment_percent = round(self.down_payment / self.purchase_price, 3)
        self.payment = self.get_payment()
        print(f'Down payment updated to ${self.down_payment:3,.2f} which represents {self.down_payment_percent:.2%} down.\n\
        The new monthly payment is ${self.payment:3,.2f}')
    
    def get_interest_rate(self):
        return self.interest_rate
    
    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate
        self.payment = self.get_payment()
        print(f'Interest Rate updated to {self.interest_rate:.2%} and the new monthly payment is ${self.payment:3,.2f}')
    
    def get_years(self):
        return self.years
    
    def set_years(self, years):
        self.years = years
        self.payment = self.get_payment()
        print(f'Number of years updated to {self.years} years and the new monthly payment is ${self.payment:3,.2f}')
    
    def get_num_yearly_pmts(self):
        return self.num_yearly_pmts
    
    def set_num_yearly_pmts(self, num_yearly_pmts):
        self.num_yearly_pmts = num_yearly_pmts
        self.payment = self.get_payment()
        print(f'Number of yearly payments updated to {self.num_yearly_pmts} and the per-period payment is ${self.payment:3,.2f}')
    
    def get_start_date(self):
        return self.start_date
    
    def set_start_date(self, start_date):
        self.start_year, self.start_month, self.start_day = start_date
        self.start_date = (date(self.start_year, self.start_month, self.start_day))
        print(f'Start date updated to {self.start_date.strftime("%m-%d-%Y")}')
    
    def get_loan_amount(self):
        return self.loan_amount
              
    def get_payment_range(self):
        self.payment_range = pd.date_range(self.start_date, periods=self.years * self.num_yearly_pmts, freq='MS')
        self.payment_range.name = 'Payment Date'
        return self.payment_range
    
    def get_payoff_date(self):
        return self.payment_range[-1].strftime("%m-%d-%Y")
              
    def get_number_of_payments(self):
        return self.years * self.num_yearly_pmts
              
    def get_amortization_table(self):
        self.payment_range = self.get_payment_range()
        self.atable = pd.DataFrame(
            index=self.payment_range,
            columns=['Payment', 'Principal Paid', 'Interest Paid', 'Beginning Balance', 'Ending Balance'],
            dtype=float
        )
        self.atable.reset_index(inplace=True)
        self.atable.index += 1
        self.atable.index.name = 'Period'
        self.atable['Payment'] = self.get_payment()
        self.atable['Principal Paid'] = -1 * npf.ppmt(self.interest_rate/self.num_yearly_pmts, self.atable.index, self.years*self.num_yearly_pmts, self.loan_amount)
        self.atable['Interest Paid'] = -1 * npf.ipmt(self.interest_rate/self.num_yearly_pmts, self.atable.index, self.years*self.num_yearly_pmts, self.loan_amount)
        self.atable.loc[1, 'Beginning Balance'] = self.loan_amount
        self.atable.loc[1, 'Ending Balance'] = self.atable.loc[1, 'Beginning Balance'] - self.atable.loc[1, 'Principal Paid']
        for i in range(2, self.years*self.num_yearly_pmts + 1):
            self.atable.loc[i, 'Ending Balance'] = self.atable.loc[i - 1, 'Ending Balance'] - self.atable.loc[i, 'Principal Paid']
            self.atable.loc[i, 'Beginning Balance'] = self.atable.loc[i - 1, 'Ending Balance']
        self.atable['Cumulative Principal Paid'] = self.atable['Principal Paid'].cumsum()
        self.atable['Cumulative Interest Paid'] = self.atable['Interest Paid'].cumsum()
        return self.atable.round(2)
    
    def get_total_principal_paid(self):
        return round(self.atable['Cumulative Principal Paid'].iloc[-1], 2)
              
    def get_total_interest_paid(self):
        return round(self.atable['Cumulative Interest Paid'].iloc[-1], 2)
    
    def get_total_cost_of_loan(self):
        return round(self.get_total_principal_paid() + self.get_total_interest_paid(), 2)
