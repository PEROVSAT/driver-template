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

## Emulator (hardware only)

- [ ] Fill in `__DRIVER_SLUG___emul.c` register map and transfer logic
- [ ] Integration backend (`CONFIG___KCONFIG_SYM___EMUL_BACKEND_INTEGRATION`): canned responses for ztest
- [ ] SITL backend (`CONFIG___KCONFIG_SYM___EMUL_BACKEND_SITL`): socket code goes here for Basilisk

**DBuild contract:** In `perovsat-app`, emulation mode uses the hardware driver west project (not mock), sets `CONFIG_EMUL=y`, `CONFIG_I2C_EMUL=y`, `CONFIG___KCONFIG_SYM___EMUL=y`, and `CONFIG___KCONFIG_SYM___EMUL_BACKEND_SITL=y`, with a board overlay wiring `zephyr,i2c-emul-controller`. Driver-repo integration tests set `CONFIG___KCONFIG_SYM___EMUL_BACKEND_INTEGRATION=y` instead.

## Testing

Run from the driver repo root (requires Zephyr workspace with this module):

```bash
# Unit tests (native_sim)
west twister -T tests/unit -p native_sim

# Integration tests (QEMU Cortex-M33)
west twister -T tests/integration -p mps2/an521
```

Hardware drivers also scaffold:

```bash
# SITL image (build-only; Basilisk not available in CI)
west twister -T tests/sitl -p mps2/an521 --build-only
```

| Test | Platform | Modes | Notes |
|------|----------|-------|-------|
| `tests/unit` | `native_sim` | hardware, mock | Commented example for internal helpers |
| `tests/integration` | `mps2/an521` | hardware, mock | Hardware uses emulator overlay |
| `tests/sitl` | `mps2/an521` | hardware only | `build_only: true` in `testcase.yaml` |
