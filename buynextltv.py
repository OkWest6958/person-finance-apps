import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import math



"""# Should I overpay to a lower LTV?"""



with st.expander('How to use this calculator'):
    """This calculator is for determining how valuable it might be to overpay 
    your mortgage such that you can secure a better interest rate at a lower Loan-To-Value ratio (LTV)"""
    """It could also be used by first time buyers to determine how beneficial it might be to save for a bigger deposit"""
    """By entering the value of your house and your current 
    mortgage amount, you will be shown how much more you would need to pay to secure a target LTV"""
    """By entering the interest rate offered at your current LTV, and the interest rate offered at your target LTV, you 
    will be shown how valuable overpaying might be, expressed as both an overall net £ increase and 
    what equivalent annualised rate of return this is for your overpayment investment"""
    """You will need to find what rates are available to you at your current and target LTV. 
    You can find rates by using price comparison tools such 
    as [MoneySuperMarket](https://www.moneysupermarket.com/mortgages/), or by using a mortgage broker 
    (you will need to search for mortgages with various mortgage amounts. You can find LTV ratios below)"""
    """This calculator will display any benefits over the duration of a fixed term mortgage period, rather than over the full mortgage term. 
    This is because there are many options available once a fix has ended (securing a new rate, overpaying a lump sum, etc.), and so it 
    can be misleading and intangible to extrapolate any impacts beyond the fix period"""
    """More information on LTV can be found [here](https://www.moneysupermarket.com/mortgages/loan-to-value-ratio-explained/)"""

st.divider()

"""## Enter your existing mortgage details"""

property_value = st.number_input(
    'How much is your house currently **valued** at (£)?',
    0,
    100000000,
    200000,
    1000,
    help="""Enter what you expect the value of your house to be when 
    you go to secure your mortgage/remortgage. A higher valuation will improve your LTV"""
)

mortgage_amount = st.number_input(
    'What is your current remaining **mortgage balance** (£)?',
    0,
    100000000,
    150000,
    1000,
    help="""Enter what you expect the balance of your to mortgage to be when you remortgage. 
    If you are a first time buyer, enter your current planned deposit"""
)

mortgage_term = st.number_input(
    'What is your existing or desired **mortgage term** (years)?',
    1,
    100,
    30,
    help="""This is required to calculate your monthly repayments. Mortgage terms can generally 
    be changed when remortgaging. A longer term will result in smaller monthly repayments"""
)

current_ltv = mortgage_amount/property_value*100

st.write(
    "### Your current LTV is: :green[{}%]".format(math.ceil(current_ltv))
)

if current_ltv % 1 != 0:
    st.write("(Mortgage providers will round up to this from your actual :green[{:.2f}%] LTV)".format(current_ltv))


ltv_table = pd.DataFrame({'LTV': (np.arange(19) + 1) * 5})

ltv_table['Mortgage amount'] = ltv_table['LTV'] * property_value / 100

with st.expander('Show LTV ratios for given house value'):
    ltv_table.sort_values('LTV', ascending=False, inplace=True)
    ltv_table.set_index('LTV', inplace=True)
    st.write(ltv_table.style.format('£{:,.2f}'))
    st.write("Mortgage providers typically do not give better rates below 60% LTV")

st.divider()



"""# Enter your prospective mortgage details"""

fixed_term_duration = st.number_input(
    'How long do you intend to **fix** your **next mortgage** for (years)?',
    1,
    mortgage_term,
    5,
    help="""Required to display any benefits over the course of a fixed term mortgage"""
)

current_ltv_rate = st.number_input(
    'What is the **interest rate** offered at your **current LTV bracket**? (%)',
    0.00,
    1000.00,
    4.50,
    0.01,
    help="""Used to calculate the current costs of the mortgage"""
)

if current_ltv % 5 == 0:
    proposed_ltv = current_ltv - 5
else:
    proposed_ltv = current_ltv//5*5

next_ltv = st.number_input(
    'What is the **LTV bracket** you are aiming for? (%)',
    0.00,
    current_ltv,
    proposed_ltv,
    5.0,
    help="""What LTV bracket do you want to calculate potential value for. This must be lower than your current LTV bracket"""
)

next_ltv_rate = st.number_input(
    'What **interest rate** is available at the **LTV bracket you are aiming for**? (%)',
    0.00,
    current_ltv_rate,
    current_ltv_rate - 0.05,
    0.01,
    help="""Used to calculate the costs of your prospective mortgage. This must be lower than your current LTV interest rate"""
)

amount_to_next_ltv = (current_ltv - next_ltv) * property_value / 100



st.write(
    '### You would need to spend :green[£{:,.2f}] to reach the LTV bracket you are aiming for'.format(amount_to_next_ltv)
)


st.divider()


"""# Simple results"""


current_ltv_pmt = -npf.pmt(
    current_ltv_rate / 100 / 12,
    mortgage_term * 12,
    mortgage_amount
)

st.write(
    'At the rate offered for your current LTV, you would be paying: :green[£{:,.2f}] a month'.format(current_ltv_pmt)
)

next_ltv_pmt = -npf.pmt(
    next_ltv_rate / 100 / 12,
    mortgage_term * 12,
    mortgage_amount - amount_to_next_ltv
)

st.write(
    'At the rate offered for the LTV you are aiming for, you would be paying: :green[£{:,.2f}] a month'.format(next_ltv_pmt)
)

monthly_savings = current_ltv_pmt-next_ltv_pmt


total_monthly_savings_after_fix_duration = monthly_savings * fixed_term_duration * 12



st.write(
    """This is a difference of :green[£{:,.2f}] per month, which is a total saving 
    of :green[£{:,.2f}] after :green[{}] years""".format(monthly_savings,total_monthly_savings_after_fix_duration,fixed_term_duration)
)


current_ltv_balance_after_fix = -npf.fv(
    current_ltv_rate / 100 / 12,
    fixed_term_duration * 12,
    -current_ltv_pmt,
    mortgage_amount
)

next_ltv_balance_after_fix = -npf.fv(
    next_ltv_rate / 100 / 12,
    fixed_term_duration * 12,
    -next_ltv_pmt,
    mortgage_amount - amount_to_next_ltv
)


st.write(
    """After :green[{}] years, your remaining mortgage balance would be:
    \n* :green[£{:,.2f}] for your current LTV rate
    \n* :green[£{:,.2f}] for the LTV rate you are aiming for""".format(fixed_term_duration, current_ltv_balance_after_fix, next_ltv_balance_after_fix)
)



current_ltv_net_worth = property_value - current_ltv_balance_after_fix
next_ltv_net_worth = property_value - next_ltv_balance_after_fix + (current_ltv_pmt - next_ltv_pmt) * fixed_term_duration * 12



st.write(
    """Therefore, after :green[{}] years your net worth would be:
    \n* :green[£{:,.2f}] at your current LTV rate. (:green[£{:,.2f}] from the value of your house, 
    :green[£{:,.2f}] from monthly mortgage repayment savings, and 
    :red[£{:,.2f}] from your remaining mortgage balance)""".format(fixed_term_duration,
                                                    current_ltv_net_worth,
                                                    property_value,
                                                    0,
                                                    -current_ltv_balance_after_fix)
)

st.write(
    """\n* :green[£{:,.2f}] at your current LTV rate. (:green[£{:,.2f}] from the value of your house, 
    :green[£{:,.2f}] from monthly mortgage repayment savings, and 
    :red[£{:,.2f}] from your remaining mortgage balance)""".format(next_ltv_net_worth,
                                                                   property_value,
                                                                   monthly_savings*12*fixed_term_duration,
                                                                   -next_ltv_balance_after_fix)
)




net_worth_diff =  next_ltv_net_worth - current_ltv_net_worth

equivilant_rate_of_return = ((net_worth_diff / amount_to_next_ltv) ** (1 / fixed_term_duration) - 1) * 100


st.write("""### This means you are :green[£{:,.2f}] better off after :green[{}] years for an initial investment of :green[£{:,.2f}]""".format(net_worth_diff,fixed_term_duration,amount_to_next_ltv))

st.write('### This is the equivalent of a guaranteed :green[{:,.2f}%] annualised rate of return on your initial investment of :green[£{:,.2f}]'.format(equivilant_rate_of_return,amount_to_next_ltv))


st.divider()


"""
# Fairer results
"""

st.write(
    'The above "Simple results" assume you do not utilise your :green[£{:,.2f}] monthly repayments savings'.format(monthly_savings)
)

st.write(
    """On your current LTV, you would be spending :green[£{:,.2f}] per 
    month on your mortgage, so let's spend up to that amount on the new mortgage or savings""".format(current_ltv_pmt)
)

monthly_savings_fv_at_rate = -npf.fv(
    next_ltv_rate/100/12,
    fixed_term_duration*12,
    monthly_savings,
    0
)

st.write(
    """If you use :green[£{:,.2f}] a month to overpay your mortgage (at :green[{:,.2f}%]), 
    or put this money into savings earning :green[{:,.2f}%], you would have :green[£{:,.2f}] (reduced from 
    your mortgage balance or saved in the bank) instead of 
    the original :green[£{:,.2f}] of unutilised monthly repayments savings""".format(monthly_savings,
                                                                        next_ltv_rate,
                                                                        next_ltv_rate,
                                                                        monthly_savings_fv_at_rate,
                                                                        monthly_savings * fixed_term_duration * 12)
)



st.write('''### This is an increase of :green[£{:,.2f}] from the "Simple results"'''.format(monthly_savings_fv_at_rate-monthly_savings*fixed_term_duration*12))

st.write(
    """This means your new net worth after :green[{}] years 
    is :green[£{:,.2f}]""".format(fixed_term_duration,
                                  property_value + monthly_savings_fv_at_rate - next_ltv_balance_after_fix)
)

st.write(
    """This means you are :green[£{:,.2f}] better off after :green[{}] years for 
    an initial investment of :green[£{:,.2f}]""".format(property_value + monthly_savings_fv_at_rate - next_ltv_balance_after_fix - current_ltv_net_worth,
                                        fixed_term_duration,
                                        amount_to_next_ltv)
)


st.divider()


"""
# Optimistic results
"""

st.write(
    """The above "Fairer results" assume you overpay your new mortgage 
    or achieve a savings rate equal to your new mortgage rate (:green[{:,.2f}%])""".format(next_ltv_rate)
)


st.write(
    """As this is your mortgage rate, and generally mortgage overpayments 
    are always available, you will always be able to utilise **at least** this rate (:green[{:,.2f}%])""".format(next_ltv_rate)
)


st.write(
    """If you can earn more than :green[{:,.2f}%] in either savings or investments, you will be even better off""".format(next_ltv_rate)
)



monthly_savings_fv_at_higher_rate = -npf.fv(
    (next_ltv_rate+1)/100/12,
    fixed_term_duration*12,
    monthly_savings,
    0
)


st.write(
    """* Earning :green[{:,.2f}%] on you :green[£{:,.2f}] a month 
    would make your net worth :green[£{:,.2f}]. This is an increase of :green[£{:,.2f}] compared to overpaying""".format(next_ltv_rate + 1,
                  monthly_savings,
                  property_value + monthly_savings_fv_at_higher_rate - next_ltv_balance_after_fix,
                  (property_value + monthly_savings_fv_at_higher_rate - next_ltv_balance_after_fix) - (property_value + monthly_savings_fv_at_rate - next_ltv_balance_after_fix))
)



monthly_savings_fv_at_highest_rate = -npf.fv(
    (next_ltv_rate+3)/100/12,
    fixed_term_duration*12,
    monthly_savings,
    0
)


st.write(
    """* Earning :green[{:,.2f}%] on you :green[£{:,.2f}] a month 
    would make your net worth :green[£{:,.2f}]. This is an increase of :green[£{:,.2f}] compared to overpaying""".format(next_ltv_rate + 3,
                  monthly_savings,
                  property_value + monthly_savings_fv_at_highest_rate - next_ltv_balance_after_fix,
                  (property_value + monthly_savings_fv_at_highest_rate - next_ltv_balance_after_fix) - (property_value + monthly_savings_fv_at_rate - next_ltv_balance_after_fix))
)
