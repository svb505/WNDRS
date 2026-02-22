import os

folder = "my_os_production/sys/syst_comp"

paths = []
for name in os.listdir(folder):
      full = os.path.join(folder, name)
      if os.path.isfile(full):
            if name not in ["plc_sys.cfg","plc_clk.cfg","gamebar_settings/gamebar_theme.cfg",
                            "volume.cfg","size.cfg","icons.cfg","gamebar_settings/gamebar_shw_inf.cfg",
                            "lang.cfg","gamebar_settings/gamebar_p.cfg","format_clk.cfg","region.cfg",
                            "auto_upd.cfg","antvrs_state.cfg"]:
                paths.append(f'{name}')
for x in paths:
    print(x)