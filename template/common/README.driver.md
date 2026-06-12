# __MODULE_NAME__

__DRIVER_UPPER__ __DEVICE__ driver (PerovSat Zephyr module).

## Driver TODOs

- [ ] Binding: declare devicetree properties in `dts/bindings/__SUBSYS__/`
- [ ] Header: fill in config/data structs (hardware) or mock data struct in the driver `.h`
- [ ] `init()`: device setup and initialization
- [ ] Per-instance `_INIT` macro: map binding properties into config struct fields
- [ ] Driver API: register an API struct in `DEVICE_DT_INST_DEFINE` if needed

## App integration (perovsat-app)

- [ ] Add `__MODULE_NAME__` as a west project in `west.yml`
- [ ] Add `__DEVICE__` entry in `dbuild/device_map.yml` pointing `__MODE__` mode to `__MODULE_NAME__`
- [ ] Create snippet under `snippets/<snippet-name>/` with `CONFIG___KCONFIG_SYM__=y` in `.conf`
- [ ] Add devicetree overlay with `compatible = "__COMPAT__"`

## Deferred (not yet scaffolded)

- [ ] Emulator (Emulator API)
- [ ] Twister unit tests
