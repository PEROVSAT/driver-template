# __MODULE_NAME__

__DRIVER_UPPER__ driver (PerovSat Zephyr module).

## Driver TODOs

- [ ] Library: implement protocol logic in `lib/__DRIVER_SLUG__/`
- [ ] Binding: declare devicetree properties in `dts/bindings/__SUBSYS__/`
- [ ] Header: fill in config/data structs in `drivers/__SUBSYS__/__DRIVER_SLUG__/`
- [ ] `init()`: device setup and backend-specific initialization
- [ ] Per-instance `_INIT` macro: map binding properties into config struct fields
- [ ] Driver API: register an API struct in `DEVICE_DT_INST_DEFINE` if needed
- [ ] Transfer backends: fill in hardware, simulation, and library-mock transfer functions

## Backends

This driver supports four build-time backends via Kconfig:

| Backend | Kconfig | Library | Use case |
|---------|---------|---------|----------|
| **Hardware** | `CONFIG___KCONFIG_SYM___BACKEND_HARDWARE` | Yes | Real device on the bus |
| **Simulation** | `CONFIG___KCONFIG_SYM___BACKEND_SIMULATION` | Yes | Socket to Basilisk (SITL) |
| **Library mock** | `CONFIG___KCONFIG_SYM___BACKEND_LIBRARY_MOCK` | Yes | Static register data via injected transfer fn |
| **Public mock** | `CONFIG___KCONFIG_SYM___BACKEND_PUBLIC_MOCK` | No | Hardcoded API returns; NDA-safe default |

The default backend is **public mock**, so the repo builds without the device library.

**DBuild contract:** In `perovsat-app`, set the backend via snippet `.conf` (e.g. `CONFIG___KCONFIG_SYM___BACKEND_SIMULATION=y` for SITL). Hardware builds use `CONFIG___KCONFIG_SYM___BACKEND_HARDWARE=y`.

## NDA devices

The template scaffolds the device library in-repo at `lib/__DRIVER_SLUG__/`. For NDA devices:

1. Move `lib/__DRIVER_SLUG__/` into a private west-module repository.
2. Remove the local `lib/` directory from the public driver repo.
3. Build with `CONFIG___KCONFIG_SYM___BACKEND_PUBLIC_MOCK=y` for CI and contributors without library access.
4. Link the private library module only in builds that have access.

The Zephyr wrapper already compiles without the library when public mock is selected.

## App integration (perovsat-app)

- [ ] Add `__MODULE_NAME__` as a west project in `west.yml`
- [ ] Map `__MODULE_NAME__` to the logical device role your application expects (e.g. IMU)
- [ ] Create snippet under `snippets/<snippet-name>/` with `CONFIG___KCONFIG_SYM__=y` and the desired backend in `.conf`
- [ ] Add devicetree overlay with `compatible = "__COMPAT__"`

## Testing

Run from the driver repo root (requires Zephyr workspace with this module):

```bash
# Unit tests (native_sim) — library protocol logic, no Zephyr driver
west twister -T tests/unit -p native_sim

# Public mock (native_sim) — NDA-safe, no library linked
west twister -T tests/public_mock -p native_sim

# Library mock (QEMU Cortex-M3)
west twister -T tests/library_mock -p qemu_cortex_m3

# Simulation image (build-only; Basilisk not available in CI)
west twister -T tests/simulation -p qemu_cortex_m3 --build-only
```

| Test | Platform | Backend | Notes |
|------|----------|---------|-------|
| `tests/unit` | `native_sim` | N/A (library only) | Fake transfer fn in test |
| `tests/public_mock` | `native_sim` | Public mock | Default; no library |
| `tests/library_mock` | `qemu_cortex_m3` | Library mock | Static register map |
| `tests/simulation` | `qemu_cortex_m3` | Simulation | `build_only: true` |

## UART variant

The template defaults to I2C (`include: i2c-device.yaml`). For UART-based NDA devices, update the binding, config struct, and `__DRIVER_SLUG___hardware.c` transfer backend to use the Zephyr UART API instead of I2C.
