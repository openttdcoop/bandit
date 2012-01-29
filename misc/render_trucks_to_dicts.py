vehicle_list = container.vehicle_storage.objectValues(['File'])

vehicles_dict = {}

for i in vehicle_list:
  this_veh_props = {}
  for j in i.propertyIds():
    if i.getPropertyType(j) == 'date':
      this_veh_props[j] = str(i.getProperty(j))
    else:      
      this_veh_props[j] = i.getProperty(j)
  del this_veh_props['content_type'] #zope adds this property to file objects automatically but we don't need it here
  this_veh_props['trailers_properties'] = {}
  this_veh_props['trailer_capacities'] = [int(capacity) for capacity in this_veh_props['trailer_capacities']] #capacities need covnerted to int - lines field stores them as strings
  for j in range(0,i.truck_num_trailers):
    trailer_props = this_veh_props['trailers_properties'][i.id() + "_trailer_" + str(j+1)] = {}
    trailer_props['numeric_id'] = i.numeric_ID + j + 1
    trailer_capacity = int(i.trailer_capacities[j])
    #capacity first trailer of fifth wheel truck split with truck according to decimal ratio
    if j == 0 and i.truck_type == "GLOBAL_TRUCK_TYPE_FIFTH_WHEEL":
      this_veh_props['truck_capacity'] = truck_capacity = int(float(trailer_capacity) * (i.fifth_wheel_truck_capacity_fraction))
      trailer_capacity = trailer_capacity - truck_capacity
    trailer_props['trailer_capacity'] = trailer_capacity
    
    # add graphics file, lengths etc here later
  vehicles_dict[i.id()] = this_veh_props
    
print "vehicles_dict = " + str(vehicles_dict)
return printed
