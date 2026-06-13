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

By default, `setup.py` removes the template history, runs `git init`, applies code style checks, and creates an initial commit titled `Template Clone`. Pass `--no-fresh-git` to keep the clone's git history and skip the initial commit.

After setup, `template/` and `setup.py` are deleted. Wire the new driver into `perovsat-app` (see the generated `README.md` checklist).

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

### Testing scaffold

Each bootstrapped repo includes Twister tests under `tests/`:

- **Unit** (`tests/unit`) — runs on `native_sim`; commented example for internal helpers
- **Integration** (`tests/integration`) — runs on `qemu_cortex_m3`
- **SITL** (`tests/sitl`, hardware only) — build-only harness with SITL emulator backend

Hardware drivers also include `__DRIVER_SLUG___emul.c` with a Kconfig choice between integration and SITL emulator backends.

## Token reference

`setup.py` substitutes these placeholders in paths and file contents:

| Token | Example (hardware) | Example (mock) |
|-------|-------------------|----------------|
| `__MODULE_NAME__` | `mpu6050-driver` | `mpu6050-mock-driver` |
| `__DEVICE__` | `IMU` | `IMU` |
| `__VENDOR__` | `invensense` | `invensense` |
| `__DRIVER_SLUG__` | `mpu6050` | `mpu6050` |
| `__DRIVER_BASE__` | `mpu6050` | `mpu6050_mock` |
| `__COMPAT__` | `invensense,mpu6050` | `invensense,mpu6050-mock` |
| `__DT_COMPAT__` | `invensense_mpu6050` | `invensense_mpu6050_mock` |
| `__KCONFIG_SYM__` | `PEROVSAT_IMU` | `PEROVSAT_IMU_MOCK` |

Mock mode appends `-mock` to the compatible string and `_MOCK` to the Kconfig symbol. `__DRIVER_BASE__` is the driver directory and C symbol prefix (`mpu6050` vs `mpu6050_mock`).

## Typical workflow

1. Clone `driver-template` twice — once for the public mock repo, once for the hardware repo (if NDA/private).
2. Run `setup.py` in each with the appropriate `--mode`.
3. Fill in the `TODO` items in the generated driver.
4. Add the new west projects and dbuild snippets in `perovsat-app`.
5. Build with `west dbuild -b <board>`.
