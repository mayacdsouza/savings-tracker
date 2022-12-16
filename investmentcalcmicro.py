######## MICROSERVICE #########
import time as timer

while True:
    with open('invest.txt') as f:
        first_line = f.readline().strip()
    if first_line != 'run':
        continue
    timer.sleep(1)
    f = open('invest.txt', 'r')
    first_line = f.readline()
    sav_input_data = f.readline()
    inv_input_data = f.readline()
    f.close()
    normalize_sav = sav_input_data[1:-2]
    savings_data = normalize_sav.split(',')
    normalize_inv = inv_input_data[1:-1]
    invest_data = normalize_inv.split(',')
    data = [savings_data, invest_data]

    f = open('invest.txt', 'w')
    for i in range(len(data)):
        if len(data[i]) == 4:
            accountBalance, monthlyAmount, rateOfReturn, time = int(data[i][0]), int(data[i][1]), int(data[i][2]), int(data[i][3])
            result = accountBalance + (monthlyAmount * (((1 + ((rateOfReturn / 100) / 12)) ** (12 * time)) - 1) / ((rateOfReturn / 100) / 12))

            # f.write(str("${:,.2f}".format(result)) + "\n")
            f.write(str(result) + "\n")
    f.close