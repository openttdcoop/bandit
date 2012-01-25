vehicle_list = container.vehicle_storage.objectValues(['File'])

vehicle_calculated_props = {}

for i in vehicle_list:
  this_veh = vehicle_calculated_props[i.id()] = {}
  this_veh['total_capacity'] = i.truck_capacity
  this_veh['trailer_vehicle_ids'] = {}
  this_veh['trailer_vehicle_numeric_ids'] = {}
  for j in range(1,i.truck_num_trailers+1):
    this_veh['trailer_vehicle_ids']["THIS_TRAILER_" + str(j) + "_ID"] = i.id() + "_trailer_" + str(j)
    this_veh['trailer_vehicle_numeric_ids']["THIS_TRAILER_" + str(j) + "_NUMERIC_ID"] = i.numeric_ID + j
  this_veh['trailer_capacities'] = {}
  this_veh['adjusted_truck_capacity'] = 0    
  for j, x in enumerate(i.trailer_capacities):
    #capacity first trailer split with truck according to decimal ratio
    if j == 0 and i.truck_type == "GLOBAL_TRUCK_TYPE_FIFTH_WHEEL":
      trailer_capacity = int(float(x) * (1 - i.fifth_wheel_truck_capacity_fraction))
      this_veh['adjusted_truck_capacity'] = int(float(x) * (i.fifth_wheel_truck_capacity_fraction))
    else:
      trailer_capacity = int(x)
    this_veh['total_capacity'] = this_veh['total_capacity']+int(x)    
    this_veh['trailer_capacities']["THIS_TRAILER_" + str(j+1) + "_CAPACITY"] = trailer_capacity
    
    
#return str(vehicle_calculated_props)

return context.render_trucks_pt(
  vehicle_list=vehicle_list,
  vehicle_calculated_props=vehicle_calculated_props,
)
