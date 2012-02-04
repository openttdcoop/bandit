vehicle_list = container.vehicle_storage.objectValues(['File'])

vehicles = {}

for i in vehicle_list:
  this_veh_props = {}
  for j in i.propertyIds():
    if i.getPropertyType(j) == 'date':
      this_veh_props[j] = i.getProperty(j).year()
    elif i.getPropertyType(j) == 'lines':
      this_veh_props[j] = '|'.join(i.getProperty(j))
    else:      
      this_veh_props[j] = i.getProperty(j)
  del this_veh_props['content_type'] #zope adds this property to file objects automatically but we don't need it here
  vehicles[i.id()] = this_veh_props

return context.render_trucks_to_config_file_pt(
  vehicles=vehicles,
)
