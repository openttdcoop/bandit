vehicle_list = context.vehicle_storage.objectValues(['File'])
vehicle_list = list(vehicle_list) # make it a list because what a b-tree folder returns here isn't strictly a list 
vehicle_list.sort(key=lambda vehicle: id)

numeric_ids = []
duplicate_numeric_ids = {}

for i in vehicle_list:
  if i.numeric_ID in numeric_ids:
    duplicate_numeric_ids[i.numeric_ID] = []
  else:
    numeric_ids.append(i.numeric_ID)
  print '------'

for i in vehicle_list:
  if i.numeric_ID in duplicate_numeric_ids:
    duplicate_numeric_ids[i.numeric_ID].append(i.id())

return context.list_all_trucks_pt(
  data = printed,
  all_vehicles = vehicle_list,
  duplicate_numeric_ids = duplicate_numeric_ids,
)
