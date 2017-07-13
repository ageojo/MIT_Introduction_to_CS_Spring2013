# Problem Set 1A
# Name: Amy C. Geojo


interest = float(raw_input('Enter the interest rate as a decimal: '))
monthly_investment = float(raw_input('Enter the fixed monthly investment: '))

balance = 0
count = 0

for i in range(12):
    count = count + 1
    balance = balance + balance*interest/12 + monthly_investment
    print "Balance after month " + str(count) + ":" + " " +"$" + str(round(balance,2))

paid = monthly_investment*12

print "Amount paid:" + " " + "$" + str(round(monthly_investment*12, 2))
print "Amount earned from interest:" + " " + "$" + str(round(balance-paid,2))



