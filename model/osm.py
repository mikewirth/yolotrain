import json

with open('osm_trackdata.json') as f:
    coordinates = json.load(f)

with open('track site data.json') as f:
    signals = json.load(f)


from math import radians, degrees, sin, cos, asin, acos, sqrt
def great_circle(lat1, lon1, lat2, lon2):
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  return 6371 * (
    acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
  )

def generate_length(track_coordinates):
  track_coordinates = list(reversed(coordinates))

  track_coordinates[0].append(0)

  for idx, elem in enumerate(track_coordinates):
    if idx == 0:
      continue

    last_point = track_coordinates[idx-1]
    length = great_circle(last_point[1], last_point[0], elem[1], elem[0])

    elem.append(last_point[2]+length)

  return track_coordinates

def length_from_point(lat, lon, track):
  shortest_distance = 999999999
  closest_elem = None

  for elem in track:

    distance = sqrt(pow((elem[1]-lat), 2)+pow((elem[0]-lon), 2))
    """
    print("Distnace")
    print(distance)
    print(shortest_distance)
    print(elem)
    print(lon)
    print(lat)
    """

    if distance < shortest_distance:
      shortest_distance = distance
      closest_elem = elem

  return closest_elem

label_map = {
  'balise' : 'balise',
  'main signal' : 'main_signal',
  'distant signal' : 'distant_signal',
}

def length_to_signal(length, signals, object_label, max_radius = 0.2):
  shortest_distance = 999999999
  closest_elem = None

  for elem in signals:
    if elem['type'] not in label_map or label_map[elem['type']] != object_label:
      # reject wrong type
      continue
    signal_distance = float(elem["relativ position"][0:-3])

    distance = abs(length-signal_distance)



    if distance < shortest_distance:
      shortest_distance = distance
      closest_elem = elem

  if shortest_distance > max_radius:
    print("** match error {} greater than tolerance {} **".format(shortest_distance, max_radius))

  closest_elem['match distance'] = shortest_distance

  return closest_elem

import image
from exif import Image
def giveXY(path):
  with open(path, 'rb') as image_file:
       my_image = Image(image_file)
  N1 = my_image.gps_latitude
  N1 = N1[0] + N1[1]/60 + N1[2]/3600
  E1 = my_image.gps_longitude
  E1 = E1[0] + E1[1]/60 + E1[2]/3600
  Loc = (N1, E1)

  return Loc

# Bootstrap: Calculate distance of OSM track points to Landquart station (first point in the list)
lengths = generate_length(coordinates)
#print(lengths)

#length = length_from_point(46.96788830666366, 9.55436143999666, lengths)

length = length_from_point(46.97181447388889, 9.555658623333334, lengths)

"""
print()
print(length)

print()
print(length_to_signal(length[2], signals))
"""

matches = []

def get_signal_from_jpg(filename, object_label):
  loc = giveXY(filename)

  length = length_from_point(loc[0], loc[1], lengths)
  print (length)
  record = length_to_signal(length[2], signals, object_label)
  record['filename'] = filename
  record['gps'] = loc
  matches.append(record)
  return record
