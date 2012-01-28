from string import Template

truck_template = open('test_case.tnml').read()

#print truck_template

truck_type = 'fifth_wheel_truck'
truck_number_of_trailers = 1

trucks = {
  'mack'      :{'trailers' : 1, 'hp': 100},
  'kenworth'  :{'trailers' : 1, 'hp': 200},
  'peterbilt' :{'trailers' : 1, 'hp': 300}
}

for truck_id in trucks:
  truck = trucks[truck_id]
  print Template(truck_template).substitute(
    truck_id=truck_id,
    truck_type=truck_type,
    truck_number_of_trailers = truck['trailers'],
    truck_sg = truck_id + '_sg',
    truck_switch_cargo_subtype = truck_id + '_switch_cargo_subtype',
    truck_switch_articulated = truck_id + '_switch_articulated',
    power = truck['hp'],
    test_include = Template(open('test_case_2.tnml').read()).substitute(stuff = 'foo')
  )