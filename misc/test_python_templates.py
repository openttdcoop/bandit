from string import Template

truck_template = open('test_case.tnml').read()

#print truck_template

truck_id = 'mack'
truck_type = 'fifth_wheel_truck'
truck_number_of_trailers = 1

print Template(truck_template).substitute(
  truck_id=truck_id,
  truck_type=truck_type,
  truck_number_of_trailers = truck_number_of_trailers,
  truck_sg = truck_id + '_sg',
  truck_switch_cargo_subtype = truck_id + '_switch_cargo_subtype',
  truck_switch_articulated = truck_id + '_switch_articulated',
)