library(XML)
library(xml2)
library(rvest)
library(dplyr)

# time = million seconds ~ 12 days
# lat1 = min latitude = -65.9994
# lat2 = max latitude = 64.1747
# latStepSize = lat step size =
# lon1 = min longitude = 1.7945
# lon2 = max longitude = -1.7987
# lonStepSize = longitude step size
# elevation = height = 
# elevationUnits = 'K'
# coordinateSystem = 'D' (GPS) or 'M' (Mean Sea Level)
# magneticComponent = use x, y, z CHECK
#   d = Declination
#   i = Inclination
#   x = North component
#   y = East component
#   z = Vertical intensity
#   h = Horizontal intensity
#   f = Total intensity
# model = WMM or IGRF
# startYear = a value in range:
#   WMM: 2015-2019
#   IGRF: 1590-2014
# startMonth = 1-12
# startDay = 1-31
# USE vector: c(YYYY, M, D)
# end date: c(YYYY, M, D)
# datStepSize = default 1.0 ... in years
# resultFormat = use 'csv'
prefix = 'https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid?'

make_request = function(
  filename,
  lat1, lat2, latStepSize,
  lon1, lon2, lonStepSize,
  elevation, elevationUnits,
  coordinateSystem, magneticComponent,
  model,
  startDate, endDate, dateStepSize,
  resultFormat) {
  prefix = 'https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfgrid?'
  request = paste0(
    prefix,
    'lat1=', lat1, '&lat2=', lat2, '&latStepSize=', latStepSize,
    '&lon1=', lon1, '&lon2=', lon2, '&lonStepSize=', lonStepSize,
    '&elevation=', elevation, '&elevationUnits=', elevationUnits,
    '&coordinateSystem=', coordinateSystem, '&magneticComponent=', magneticComponent,
    '&model=', model,
    '&startYear=', startDate[1], '&startMonth=', startDate[2], '&startDay=', startDate[3],
    '&endYear=', endDate[1], '&endMonth=', endDate[2], '&endDay=', endDate[3],
    '&dateStepSize=', dateStepSize,
    '&resultFormat=', resultFormat
  )
  download.file(url = request, destfile = filename)
}
for (axis in c('x', 'y', 'z')) {
  make_request(
    paste0(axis, '.csv'),
    -10.9, 14.1, 0.1,
    -137.2, -99.9, 0.1,
    25389000, 'M',
    'M', axis,
    'WMM',
    c(2017, 1, 1), c(2017, 1, 2), 1,
    'csv'
  )
}
# 1 = date in decimal yearas
# 2 = latitude (degrees)
# 3 = longitude (degrees)
# 4 = elevation in km mean sea level
# 5 = component of field in decimal nanoTeslas
x = read.csv('x.csv', header = FALSE, stringsAsFactors = FALSE)
y = read.csv('y.csv', header = FALSE, stringsAsFactors = FALSE)
z = read.csv('z.csv', header = FALSE, stringsAsFactors = FALSE)
combined = cbind(
  x[ , c(2, 3, 5)],
  y[ , 5],
  z[ , 5]
)
colnames(combined) = c('lat', 'lon', 'b_x', 'b_y', 'b_z')

write.csv(x = combined, file = 'b_field_data.csv')
