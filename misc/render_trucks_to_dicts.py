vehicle_list = container.vehicle_storage.objectValues(['File'])

vehicles_dict = {}

for i in vehicle_list:
  this_veh_props = {}
  for j in i.propertyIds():
    if i.getPropertyType(j) == 'date':
      this_veh_props[j] = i.getProperty(j).year() # this is a hack, the intro_date property should be changed to an int type
    else:      
      this_veh_props[j] = i.getProperty(j)
  del this_veh_props['content_type'] #zope adds this property to file objects automatically but we don't need it here
  this_veh_props['trailer_capacities'] = [int(capacity) for capacity in this_veh_props['trailer_capacities']] #capacities need covnerted to int - lines field stores them as strings
  vehicles_dict[i.id()] = this_veh_props
    
print "vehicles_dict = " + str(vehicles_dict)
return printed
