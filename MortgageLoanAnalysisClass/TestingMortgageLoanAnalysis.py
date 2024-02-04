'''
#Testing on the dateutils.

#importing methods from the datetime module as base
import datetime
print(datetime.date.today()) # Format is in yyyy-mm-dd

from datetime import datetime
print(datetime.now().time()) #Format is in hh:mm:ss

#comparison of date and time
# Look more into the datetime module


#The dateutil modules works with the datetime object

#from dateutil.relativedelta import
#from dateutil.easter import
#from dateutil.parser import
#from dateutil.rrule import



# Datetime and relativedelta
#NOW=datetime.now()
#print("The datetime right now: " + NOW)
'''

import datetime as dt
from dateutils import month_start, relativedelta
import matplotlib.pyplot as plt
import numpy_financial as npf
import pandas as pd


class Loan:

    def __init__(self, rate, term, loan_amount, start=dt.date.today().isoformat()):
        self.rate = rate / 1200
        self.periods = term * 12
        self.loan_amount = loan_amount
        self.start = month_start(dt.date.fromisoformat(start)) + dt.timedelta(31)
        self.pmt = npf.pmt(self.rate, self.periods, -self.loan_amount)
        self.pmt_str = f"${self.pmt:,.2f}"
        self.table = self.loan_table()

    def loan_table(self):  # make a few rays and convert into data panda frame
        periods = [self.start + relativedelta(months=x) for x in
                   range(self.periods)]  # enumerate start date to end date
        interest = [npf.ipmt(self.rate, month, self.periods, -self.loan_amount)
                    for month in range(1, self.periods + 1)]
        principal = [npf.ppmt(self.rate, month, self.periods, -self.loan_amount)
                     for month in range(1, self.periods + 1)]
        table = pd.DataFrame({'Payment': self.pmt,
                              'Interest': interest,
                              'Principal': principal, }, index=pd.to_datetime(periods))
        table['Balance'] = self.loan_amount - table['Principal'].cumsum()
        return table.round(2)

    def plot_balances(self):
        amort = self.table
        plt.plot(amort.Balance, label="Balance")
        plt.plot(amort.Interest.cumsum(), label="Interest")
        plt.grid(axis="y", alpha=.5)
        plt.legend(loc=8)
        plt.show()


loan = (Loan(5.875, 30, 36000))
print(loan.table)

loan.plot_balances()
