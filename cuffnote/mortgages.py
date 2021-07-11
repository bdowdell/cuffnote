import numpy as np
import numpy_financial as npf
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class Mortgage:
    """
    A class to represent a mortgage loan for purchasing a house. This is a base class that builds an amortization table for an n-year fixed interest rate loan. 
    The base class does not include extra principal payments.
    
    Attributes
    -----------
    purchase_price (int): The full purchase price amount. Example: 200000 for a $200,000 purchase price.
    down_payment_percent (float): Percent of purchase price paid as down payment. Example: 0.2 for a 20% down payment.
    interest_rate (float): The loan interest rate. Example: 0.04125 for a 4.125% rate.
    start_year (int): The year the mortgage starts
    start_month (int): The month the mortgage starts
    start_day (int): The day the mortgage starts
    start_date (tuple): The starting date the loan begins, represented as (YYYY, M, D). Example: (2000, 5, 1) for a May 1, 2000 start date.
    years (int): The length of the mortgage loan in years. Example: 30 for a 30 year loan.
    num_yearly_payments (int, optional): The number of installment payments in a year. Typically, mortgages are paid monthly. Defaults to 12.
    down_payment (int): The down payment paid at the start of the loan
    loan_amount (int): The financed portion of the mortgage. Equals purchase_price - down_payment.
    payment (float): The monthly principal + interest payment
    payment_range (DatetimeIndex): Datetime index of payment periods from loan start date to loan payoff date.
    atable (Pandas.DataFrame): Pandas DataFrame containing the amortization table
    """
    
    def __init__(self, purchase_price, down_payment_percent, interest_rate, start_date, years, num_yearly_payments=12):
        """Initializes base mortgage class instance using input arguments

        Args:
            purchase_price (int): The full purchase price amount. Example: 200000 for a $200,000 purchase price.
            down_payment_percent (float): Percent of purchase price paid as down payment. Example: 0.2 for a 20% down payment.
            interest_rate (float): The loan interest rate. Example: 0.04125 for a 4.125% rate.
            start_date (tuple): The starting date the loan begins, represented as (YYYY, M, D). Example: (2000, 5, 1) for a May 1, 2000 start date.
            years (int): The length of the mortgage loan in years. Example: 30 for a 30 year loan.
            num_yearly_payments (int, optional): The number of installment payments in a year. Typically, mortgages are paid monthly. Defaults to 12.
        """
        # initialize instance variables
        self.purchase_price = purchase_price
        self.down_payment_percent = down_payment_percent
        self.interest_rate = interest_rate
        self.start_year, self.start_month, self.start_day = start_date
        self.start_date = (date(self.start_year, self.start_month, self.start_day))
        self.years = years
        self.num_yearly_pmts = num_yearly_payments
        # calculate down payment and starting loan amount
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        # determine monthly payment
        self.payment = self.get_payment()
        self.payment_range = self.get_payment_range()
        
    def get_payment(self):
        """getter method for monthly principal + interest payment

        Returns:
            float: monthly payment
        """
        return round(-1 * npf.pmt(self.interest_rate/self.num_yearly_pmts, self.years*self.num_yearly_pmts, self.loan_amount), 2)
    
    def get_purchase_price(self):
        """getter method for purchase price (loan amount + down payment)

        Returns:
            int: the purchase price
        """
        return self.purchase_price
    
    def set_purchase_price(self, purchase_price):
        """setter method to change purchase price
        
        Changing the purchase price will recalculate the down payment, loan amount, and monthly payment attributes.
        
        Confirms change with a print statement returning the new attribute values.

        Args:
            purchase_price (int): purchase price
        """
        self.purchase_price = purchase_price
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        self.payment = self.get_payment()
        print(f"Purchase price updated to: ${self.purchase_price:,.2f}\n\
        New monthly payment is: ${self.payment:,.2f}")
        
    def get_down_payment_percent(self):
        """getter method for down payment percent

        Returns:
            float: down payment percent
        """
        return self.down_payment_percent
    
    def set_down_payment_percent(self, down_payment_percent):
        """Setter method to change the down payment percent
        
        Changing the down payment percent will recalculate the down payment, the loan amount, and the monthly payment attributes.
        
        Confirms change with a print statement returning the new attribute values.

        Args:
            down_payment_percent (float): the down payment percent, as a float. Example: 0.0475 for a 4.75% rate.
        """
        self.down_payment_percent = down_payment_percent
        self.down_payment = self.purchase_price * self.down_payment_percent
        self.loan_amount = self.purchase_price - self.down_payment
        self.payment = self.get_payment()
        print(f'Down payment percentage updated to {self.down_payment_percent:.2%} which is ${self.down_payment:3,.2f}\n\
        The new monthly payment is ${self.payment:3,.2f}')
        
    def get_down_payment(self):
        """Getter method for down payment (purchase price * down payment percent)

        Returns:
            int: The down payment
        """
        return self.down_payment
    
    def set_down_payment(self, down_payment):
        """Setter method to change the down payment
        
        Changing the down payment will recalculate the loan amount, the down payment percent, and the monthly payment attributes.
        
        Confirms the changes with a print statement returning the new attribute values.

        Args:
            down_payment (int): down payment
        """
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
