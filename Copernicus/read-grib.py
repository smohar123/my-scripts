import pygrib

# Open the GRIB file
grbs = pygrib.open('/Users/smohar/Downloads/85d7c46ed216515a5d1af742c475917b.grib')

# Display the first message (data entry)
grb = grbs.message(1)
print(grb)

# You can extract specific data, such as temperature values
data = grb.values
print(data)
