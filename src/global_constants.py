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

#body_types
bt_tanker = namedtuple('colourset')
bt_tipping = nametuple('colourset','height')
# use the dict constructor here, normally I don't, but it makes adding cargos faster (no string quotes needed).
# design note: small variations probably better than large ones, e.g. ['flat_large_crates','flat_small_crates'] rather than ['flat','tanker']
cargo_body_type_mappings = dict(
    MILK = [bt_tanker('silver')],
    OIL_ = [bt_tanker('black')],
    RFPR = [bt_tanker('cc2')],
    WATR = [bt_tanker('cc1')],
    PETR = [bt_tanker('silver')],
    DYES = [bt_tanker('cc2')],
    COAL = ['dump'],
    IORE = ['dump'],
    CLAY = ['dump'],
    SAND = ['dump'],
    STEL = ['grey_metals'],
    VEHI = ['flat'],
    ENSP = ['flat','box'],
    BEER = ['flat', bt_tanker('silver'),'dump','logs','livestock','lowbed'], # these values for testing only
)

body_type_spritesheet_y_offset_mapping = dict (
    box          =  20,
    tanker       =  60,
    flat         = 100,
    dump         = 140,
    logs         = 100, # value for testing only
    grey_metals  = 100, # value for testing only
    livestock    = 100, # value for testing only
    lowbed       = 100, # value for testing only
)

#map truck weight factors to extra_type_info
weight_factors = dict (
    EXPRESS_TRUCK              = 0.8,
    EXPRESS_TRUCK_LONG_HAUL    = 1,
    GENERAL_PURPOSE            = 1,
    GENERAL_PURPOSE_LONG_HAUL  = 1.2,
    HEAVY_DUTY                 = 1.4,
    HEAVY_DUTY_LONG_HAUL       = 1.6,
)

graphics_path = 'src/graphics/' # this is for nml, don't need to use python path module here

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

fifth_wheel_truck_quota = 0.5 # constant representing proportion of capacity etc transferred to fifth wheel trucks from first trailer
