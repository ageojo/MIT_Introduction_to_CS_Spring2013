# Problem Set 1C
# Name: Amy C. Geojo


price = float(raw_input("Enter the price of your dream car: "))
interest = float(raw_input("Enter the annual interest rate as a decimal: "))

              
def calculate_yearly_total(monthly, interest):
    total = 0
    for i in range(12):
        total = total + total*interest/12 + monthly
    return(total)

low = 0
high = price

monthly = (low + high)/2.0
total = calculate_yearly_total(monthly, interest)

while abs(total - price) > 0.01:
    if total < price:
        low = monthly
    else:
        high = monthly
    monthly = (low + high)/2.0
    total = calculate_yearly_total(monthly, interest)

monthly = round(monthly, 2)
total = round(total, 2)
    
print "Minimum monthly investment to buy car in 1 year: " + "$" + str(monthly)
print "Account balance: " + "$" + str(total)
