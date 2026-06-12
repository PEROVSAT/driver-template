# driver-template

Template repository for PerovSat Zephyr out-of-tree drivers. Clone this repo to create a new hardware or mock driver with boilerplate already in place.

## Quick start

```bash
git clone git@github.com:PEROVSAT/driver-template.git my-new-driver
cd my-new-driver
python3 setup.py
```

`setup.py` will ask for:

| Prompt | Example | Notes |
|--------|---------|-------|
| mode | `hardware` or `mock` | Which variant to generate |
| logical device name | `IMU` | Used in Kconfig symbols and `dbuild/device_map.yml` |
| vendor | `invensense` | Devicetree compatible prefix (not `zephyr`) |
| driver slug | `mpu6050` | Lowercase identifier used in filenames and C symbols |
| subsystem | `sensor` | Zephyr driver subdirectory (default: `sensor`) |
| module name | `mpu6050-driver` | West project name (auto-suggested) |

Non-interactive example:

```bash
python3 setup.py --mode mock --device IMU --vendor invensense --driver mpu6050
```

By default, `setup.py` removes the template history and runs `git init` for a clean repository. Pass `--no-fresh-git` to keep the clone's git history.

After setup, `template/` and `setup.py` are deleted. Commit the rendered scaffold and wire it into `perovsat-app` (see the generated `README.md` checklist).

## What gets generated

Each bootstrapped repo is a Zephyr out-of-tree module with:

- `zephyr/module.yml` — west module declaration
- Top-level `Kconfig` and `CMakeLists.txt`
- Driver source under `drivers/<subsystem>/<driver>/`
- Devicetree binding under `dts/bindings/<subsystem>/`
- `DT_DRV_COMPAT`, `DEVICE_DT_INST_DEFINE`, and `DT_INST_FOREACH_STATUS_OKAY`
- Inline `TODO` comments marking where device-specific logic goes

### Hardware variant

- I2C bus scaffold (swap bus/header as needed)
- `struct <driver>_config` and `struct <driver>_data` in the header
- `init()` stub and per-instance device registration
- Kconfig symbol: `CONFIG_PEROVSAT_<DEVICE>`

### Mock variant

- `struct <driver>_mock_data` in the header
- `init()` stub and per-instance device registration
- Minimal binding (`include: base.yaml`)
- Kconfig symbol: `CONFIG_PEROVSAT_<DEVICE>_MOCK`

## Token reference

`setup.py` substitutes these placeholders in paths and file contents:

| Token | Example (hardware) |
|-------|-------------------|
| `__MODULE_NAME__` | `mpu6050-driver` |
| `__DEVICE__` | `IMU` |
| `__VENDOR__` | `invensense` |
| `__DRIVER_SLUG__` | `mpu6050` |
| `__COMPAT__` | `invensense,mpu6050` |
| `__DT_COMPAT__` | `invensense_mpu6050` |
| `__KCONFIG_SYM__` | `PEROVSAT_IMU` |

Mock mode appends `-mock` to the compatible string and `_MOCK` to the Kconfig symbol.

## Not included yet

- Emulator API scaffold
- Twister unit tests

These will be added in a future revision of the template.

## Typical workflow

1. Clone `driver-template` twice — once for the public mock repo, once for the hardware repo (if NDA/private).
2. Run `setup.py` in each with the appropriate `--mode`.
3. Fill in the `TODO` items in the generated driver.
4. Add the new west projects and dbuild snippets in `perovsat-app`.
5. Build with `west dbuild -b <board>`.
