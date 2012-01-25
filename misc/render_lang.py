vehicle_list = container.vehicle_storage.objectValues(['File'])

return context.render_lang_pt(
  vehicle_list=vehicle_list,
)
