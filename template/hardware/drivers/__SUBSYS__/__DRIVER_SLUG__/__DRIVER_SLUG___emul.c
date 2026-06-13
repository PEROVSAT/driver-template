/*
 * Device emulator for integration testing (ztest) and SITL (Basilisk).
 *
 * TODO: Swap i2c_emul.h for the correct bus emulator header (SPI, etc.).
 */

#define DT_DRV_COMPAT __DT_COMPAT__

#include <string.h>

#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/i2c_emul.h>

/** Emulator runtime state (e.g. register file). */
struct __DRIVER_SLUG___emul_data {
	uint8_t register_map[256];
	/* TODO: Add device-specific emulator state. */
};

static int __DRIVER_SLUG___emul_transfer(const struct emul *target, struct i2c_msg *msgs,
					 int num_msgs, int addr)
{
	struct __DRIVER_SLUG___emul_data *data = target->data;

	ARG_UNUSED(addr);

#if defined(CONFIG___KCONFIG_SYM___EMUL_BACKEND_INTEGRATION)
	/* Integration backend: return canned/static data for ztest. */
	for (int i = 0; i < num_msgs; i++) {
		if (msgs[i].flags & I2C_MSG_READ) {
			/* TODO: Fill msgs[i].buf from data->register_map. */
			ARG_UNUSED(data);
		} else {
			/* TODO: Update data->register_map from msgs[i].buf. */
			ARG_UNUSED(data);
		}
	}
	return 0;
#elif defined(CONFIG___KCONFIG_SYM___EMUL_BACKEND_SITL)
	/* socket code goes here: open port, exchange data with Basilisk */
	ARG_UNUSED(data);
	ARG_UNUSED(msgs);
	ARG_UNUSED(num_msgs);
	return 0;
#else
	ARG_UNUSED(data);
	ARG_UNUSED(msgs);
	ARG_UNUSED(num_msgs);
	return -ENOTSUP;
#endif
}

static struct i2c_emul_api __DRIVER_SLUG___emul_bus_api = {
	.transfer = __DRIVER_SLUG___emul_transfer,
};

static int __DRIVER_SLUG___emul_init(const struct emul *target, const struct device *parent)
{
	struct __DRIVER_SLUG___emul_data *data = target->data;

	ARG_UNUSED(parent);

	/* TODO: Initialize emulator state (register defaults, etc.). */
	memset(data->register_map, 0, sizeof(data->register_map));

	return 0;
}

#define __DRIVER_UPPER___EMUL_DEFINE(inst)                                                         \
	static struct __DRIVER_SLUG___emul_data __DRIVER_SLUG___emul_data_##inst;                  \
	EMUL_DT_INST_DEFINE(inst, __DRIVER_SLUG___emul_init, &__DRIVER_SLUG___emul_data_##inst,    \
			    NULL, &__DRIVER_SLUG___emul_bus_api, NULL)

DT_INST_FOREACH_STATUS_OKAY(__DRIVER_UPPER___EMUL_DEFINE)
