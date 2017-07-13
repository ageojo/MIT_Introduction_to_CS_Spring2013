# Problem Set 1B
# Name: Amy C. Geojo
# Collaborators: Natalia Reim, Alexandre Sahyoun


###########################################################
#version 1 with defined function to calculate yearly total
price = float(raw_input("Enter the price of your dream car: "))
interest = float(raw_input("Enter the annual interest rate as a decimal: "))


# body of f(x) from ps1a
# f(x) computes total investment after 1 year, given fixed monthly investment & interest             
def calculate_yearly_total(monthly, interest):
    total = 0
    for i in range(12):
        total = total + total*interest/12 + monthly
    return(total)


monthly_investment=0.0
total=0

while total < price:

    monthly_investment += 10
    
    # calculate 12 month total here using function calculate_yearly_total
    total=round(calculate_yearly_total(monthly_investment,interest), 2)

print "Minimum monthly investment to buy car in 1 year: " + "$" + str(monthly_investment)
print "Account balance: " + "$" + str(total)

###########################################################
# version 2 with body of function directly in while loop (all but incremented value--the monthly_investment)
price = float(raw_input("Enter the price of your dream car: "))
interest = float(raw_input("Enter the annual interest rate as a decimal: "))

              
monthly_investment=0.0
total=0

while total < price:
    monthly_investment += 10
    
    # calculate 12 month total here
    total=0
    for i in range(12):
        total = total + total*interest/12 + monthly_investment

total = round(total, 2)
print "Minimum monthly investment to buy car in 1 year: " + "$" + str(monthly_investment)
print "Account balance: " + "$" + str(total)
