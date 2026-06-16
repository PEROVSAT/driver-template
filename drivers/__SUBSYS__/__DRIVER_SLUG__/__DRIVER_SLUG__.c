#define DT_DRV_COMPAT __DT_COMPAT__

#include "__DRIVER_SLUG__.h"

#include <zephyr/device.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(__DRIVER_SLUG__, CONFIG_LOG_DEFAULT_LEVEL);

#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
extern int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read);
#endif

/* TODO: Replace with your public driver API and register it in DEVICE_DT_INST_DEFINE. */
static int __DRIVER_SLUG___read_sample(const struct device *dev, struct __DRIVER_SLUG___sample *sample)
{
#if defined(CONFIG___KCONFIG_SYM___BACKEND_PUBLIC_MOCK)
	ARG_UNUSED(dev);

	sample->value = 42;
	return 0;
#else
	struct __DRIVER_SLUG___data *data = dev->data;

	return __DRIVER_SLUG___lib_read_sample(&data->lib, sample);
#endif
}

static int __DRIVER_SLUG___init(const struct device *dev)
{
#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
	struct __DRIVER_SLUG___data *data = dev->data;
	int ret;

#if defined(CONFIG___KCONFIG_SYM___BACKEND_HARDWARE)
	const struct __DRIVER_SLUG___config *config = dev->config;

	if (!i2c_is_ready_dt(&config->i2c)) {
		return -ENODEV;
	}
#endif

	ret = __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
	if (ret < 0) {
		return ret;
	}
#else
	ARG_UNUSED(dev);
#endif

	return 0;
}

#define __DRIVER_UPPER___INIT(inst)                                                                \
	static struct __DRIVER_SLUG___data __DRIVER_SLUG___data_##inst;                            \
	static const struct __DRIVER_SLUG___config __DRIVER_SLUG___config_##inst = {               \
		.i2c = I2C_DT_SPEC_INST_GET(inst), /* TODO: .prop = DT_INST_PROP(inst, prop), */   \
	};                                                                                         \
	DEVICE_DT_INST_DEFINE(                                                                     \
		inst,                           /* Device instance number */                       \
		__DRIVER_SLUG___init,           /* initialization function */                      \
		NULL,                           /* Power management system. Null if unused */      \
		&__DRIVER_SLUG___data_##inst,   /* Initialized data struct above */                \
		&__DRIVER_SLUG___config_##inst, /* Initialized config struct above*/               \
		POST_KERNEL, /* When in the boot process to init. Must be after bus */             \
		CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, /* Priority within stage above */             \
		NULL                                 /* TODO: The defined API */                   \
	);

DT_INST_FOREACH_STATUS_OKAY(__DRIVER_UPPER___INIT)
