/*
 * Generated boilerplate — do not edit.
 *
 * Device registration and init wiring. Backend selection is handled by CMake;
 * see __DRIVER_SLUG___device.c / __DRIVER_SLUG___public_mock.c for the API.
 */

#define DT_DRV_COMPAT __DT_COMPAT__

#include "__DRIVER_SLUG__.h"

#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(__DRIVER_SLUG__, CONFIG_LOG_DEFAULT_LEVEL);

extern int __DRIVER_SLUG___backend_init(const struct device *dev);
extern const struct __DRIVER_SLUG___driver_api __DRIVER_SLUG___api;

static int __DRIVER_SLUG___init(const struct device *dev)
{
	return __DRIVER_SLUG___backend_init(dev);
}

#define __DRIVER_UPPER___INIT(inst)                                                                \
	static struct __DRIVER_SLUG___data __DRIVER_SLUG___data_##inst;                            \
	static const struct __DRIVER_SLUG___config __DRIVER_SLUG___config_##inst = {               \
		.bus = SPI_DT_SPEC_INST_GET(inst, 0, 0),                                           \
	};                                                                                         \
	DEVICE_DT_INST_DEFINE(inst, __DRIVER_SLUG___init, NULL, &__DRIVER_SLUG___data_##inst,      \
			      &__DRIVER_SLUG___config_##inst, POST_KERNEL,                           \
			      CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &__DRIVER_SLUG___api);

DT_INST_FOREACH_STATUS_OKAY(__DRIVER_UPPER___INIT)
