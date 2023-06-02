import csv
import random
from datetime import datetime, timedelta
from pytz import timezone

#   //-- 2023 to 2025 market holidays --//
#   //-- https://www.nyse.com/markets/hours-calendars --//
tradingHolidays = [
    "2023-01-02",
    "2023-01-16",
    "2023-02-20",
    "2023-04-07",
    "2023-05-29",
    "2023-06-19",
    "2023-07-04",
    "2023-09-04",
    "2023-11-23",
    "2023-12-25",
    "2024-01-01",
    "2024-01-15",
    "2024-02-19",
    "2024-03-29",
    "2024-05-27",
    "2024-06-19",
    "2024-07-04",
    "2024-09-02",
    "2024-11-28",
    "2024-12-25",
    "2025-01-01",
    "2025-01-20",
    "2025-02-17",
    "2025-04-18",
    "2025-05-26",
    "2025-06-19",
    "2025-07-04",
    "2025-09-01",
    "2025-11-27",
    "2025-12-25",
]

tradingHolidaysDates = [
    datetime.strptime(date_str, '%Y-%m-%d') for date_str in tradingHolidays
]


def get_previous_weekdays(num_days):
    current_time = datetime.now()
    weekdays = []
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("16:00", "%H:%M").time()

    while len(weekdays) < num_days:
        current_time -= timedelta(days=1)
        if current_time.weekday() < 5:  # Monday to Friday (0 to 4)
            exec_date = current_time.date()
            # Check if the exec_time falls on a trading holiday
            if exec_date in tradingHolidaysDates:
                continue  # if the date falls within a holiday then it skips the append

            exec_time = datetime.combine(exec_date, start_time)
            # exec_time = exec_time + timedelta(minutes = random.randint(0, 420))

            # Check if the exec_time falls within the desired trading hours
            exec_time = timezone('US/Eastern').localize(exec_time)
            if exec_time.time() >= start_time and exec_time.time() <= end_time:
                weekdays.append(exec_time)

    return weekdays


def generate_dummy_data(num_rows):
    headers = ['Exec Time', 'Spread', 'Side', 'Qty', 'Pos Effect',
               'Symbol', 'Exp', 'Strike', 'Type', 'Price', 'Net Price', 'Order Type']
    data = []

    # Set some stuff up for exec_time to be within trading hours, based on 9-4 ET
    previous_weekdays = get_previous_weekdays(5)
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("16:00", "%H:%M").time()

    for _ in range(num_rows):
        # Enhanced exec_time data
        exec_date = random.choice(previous_weekdays).date()
        # Make the exec time a random time between 9a and 4p (7hr = 420 min)
        exec_time = datetime.combine(
            exec_date, start_time) + timedelta(minutes=random.randint(0, 420))
        # Format exec time
        exec_time = timezone(
            'US/Eastern').localize(exec_time).strftime('%m/%d/%y %H:%M:%S')

        spread = 'STOCK'
        a = random.randint(-1000, -100)
        b = random.randint(-99, -10)
        c = random.randint(-9, 10)
        d = random.randint(11, 100)
        e = random.randint(101, 1000)
        qty = random.choices([a, b, c, d, e], weights=[1, 5, 40, 5, 1])[0]

        # Side formula
        if qty < 0:
            side = 'SELL'
        else:
            side = 'BUY'

        # Determine likelihood of pos_effect based on status of side
        if side == 'BUY':
            # 80% to 20% are the weights from the example brokerage schema
            pos_effect = random.choices(
                ['TO OPEN', 'TO CLOSE'], weights=[8, 2])[0]
        else:
            # 92% to 8% are the weights from the example brokerage schema
            pos_effect = random.choices(
                ['TO OPEN', 'TO CLOSE'], weights=[8, 92])[0]

        symbol = random.choice(
            ['SPY', 'SOUN', 'DD', 'TSLA', 'CMMB', 'AUPH', 'SLB', 'ATNF'])
        exp = ''
        strike = ''
        if symbol == 'SPY':
            type_ = 'ETF'
        else:
            type_ = 'STOCK'

        # Make price more probable to be a lower number
        p1 = round(random.uniform(1.0, 10.0), 4)
        p2 = round(random.uniform(11.0, 100.0), 4)
        p3 = round(random.uniform(101.0, 400.0), 4)
        # randomly picked weights, but want it to seem more realistic
        price = round(random.choices([p1, p2, p3], weights=[15, 4, 1])[0], 4)

        # this is the ratio in the example data :)
        net_price = price * 0.999999882686286

        # Make order_type realistically weighted based on pos_effect
        if pos_effect == 'TO OPEN':
            # based on actual % mix from example data
            order_type = random.choices(
                ['LMT', 'MKT', 'STP'], weights=[5, 95, 0])
        else:
            # based on actual % mix from example data
            order_type = random.choices(
                ['LMT', 'MKT', 'STP'], weights=[2, 82, 16])

        row = [exec_time, spread, side, qty, pos_effect, symbol,
               exp, strike, type_, price, net_price, order_type]
        data.append(row)

    return headers, data


def write_to_csv(filename, headers, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Account Trade History'] + [''] * (len(headers) - 1))
        writer.writerow([''] + headers)
        writer.writerows([[''] + row for row in data])


# Generate 100 rows of dummy data and write to a CSV file
headers, data = generate_dummy_data(100)
write_to_csv('dummydata044.csv', headers, data)

# Original formulas, before modifying to make more believable
# exec_time = get_previous_weekday(datetime.now()).strftime('%m/%d/%y %H:%M:%S')
# side = random.choice(['BUY', 'SELL']) # Roughly a 50/50 split based on example data
# qty = random.randint(-10, 10)
# pos_effect = random.choice(['TO OPEN', 'TO CLOSE'])
# order_type = random.choice(['LMT', 'MKT', 'STP']) <-- original formula
