from meteocalc import Temp, dew_point

# create input temperature in different units
t = Temp(25, 'c')  # c - celsius, f - fahrenheit, k - kelvin

# calculate Dew Point
dp = dew_point(temperature=t, humidity=70)

print('Dew Point in celsius:', dp.c)
