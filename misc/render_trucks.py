vehicle_list = container.vehicle_storage.objectValues(['File'])

vehicle_calculated_props = {}

for i in vehicle_list:
  this_veh = vehicle_calculated_props[i.id()] = {}
  this_veh['total_capacity'] = i.truck_capacity
  this_veh['trailer_vehicle_ids'] = {}
  for j in range(1,i.truck_num_trailers+1):
    this_veh['trailer_vehicle_ids']["THIS_TRAILER_" + str(j) + "_ID"] = i.id() + "_trailer_" + str(j)
  this_veh['trailer_capacities'] = {}    
  for j, x in enumerate(i.trailer_capacities):
    this_veh['total_capacity'] = this_veh['total_capacity']+int(x)    
    this_veh['trailer_capacities']["THIS_TRAILER_" + str(j+1) + "_CAPACITY"] = int(x)
    
    
#return str(vehicle_calculated_props)

return context.render_trucks_pt(
  vehicle_list=vehicle_list,
  vehicle_calculated_props=vehicle_calculated_props,
)
