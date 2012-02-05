# provide mapping of truck_type strings to numbers for use in range checks etc
# constants like this are one case where c pre-processor was a little more elegant than python 
truck_type_nums = {
  'solo_truck'         : 0, 
  'drawbar_truck'      : 1,
  'fifth_wheel_truck'  : 2,
}
# expose these identifiers as a convenience 
solo_truck_type_num        = truck_type_nums['solo_truck']
fifth_wheel_truck_type_num = truck_type_nums['fifth_wheel_truck']
drawbar_truck_type_num     = truck_type_nums['drawbar_truck']

# model lives are pretty standard, the game randomises them anyway so no need to offer much variety
model_lives = {
  'BANDIT_MODEL_LIFE_SHORT'  : 10,
  'BANDIT_MODEL_LIFE_MEDIUM' : 20,
  'BANDIT_MODEL_LIFE_LONG'   : 30,
}

# vehicles lives are pretty standard, not much gained by varying them in detail (although can add more options here if needed)
vehicle_lives = {
  'BANDIT_VEHICLE_LIFE_SHORT'  : 15,
  'BANDIT_VEHICLE_LIFE_MEDIUM' : 25,
  'BANDIT_VEHICLE_LIFE_LONG'   : 35,
}

# trucks refit to quite standard sets of cargos.  The main reason for variation is to provide gameplay difference between truck models
standard_class_refits = {
  'default' : {
        'allow'    : 'CC_MAIL, CC_EXPRESS, CC_ARMOURED, CC_BULK, CC_PIECE_GOODS,CC_LIQUID, CC_REFRIGERATED, CC_COVERED,',
        'disallow' : 'CC_PASSENGERS',
  },
  'express' : {
        'allow'    : 'CC_EXPRESS',
        'disallow' : 'CC_PASSENGERS',
  },
  'heavy_duty' : {
        'allow'    : 'CC_BULK',
        'disallow' : 'CC_PASSENGERS',
  }
}

cargo_body_type_mappings = dict(
  MILK = 'tanker',
  OIL_ = 'tanker',
  RFPR = 'tanker',
  WATR = 'tanker',
  PETR = 'tanker',
  DYES = 'tanker',
  COAL = 'dump',
  IORE = 'dump',
  CLAY = 'dump',
  SAND = 'dump',
  STEL = 'flat',
  VEHI = 'flat',
)
