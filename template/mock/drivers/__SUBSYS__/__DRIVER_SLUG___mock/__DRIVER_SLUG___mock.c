#define DT_DRV_COMPAT __DT_COMPAT__

#include "__DRIVER_SLUG___mock.h"

#include <zephyr/device.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(__DRIVER_SLUG___mock, CONFIG_LOG_DEFAULT_LEVEL);

static int __DRIVER_SLUG___mock_init(const struct device *dev)
{
	ARG_UNUSED(dev);

	/* TODO: Initialize mock runtime state. */

	return 0;
}

#define __DRIVER_UPPER___MOCK_INIT(inst)                                                           \
	static struct __DRIVER_SLUG___mock_data __DRIVER_SLUG___mock_data_##inst;                  \
	DEVICE_DT_INST_DEFINE(                                                                     \
		inst,                              /* Device instance number */                    \
		__DRIVER_SLUG___mock_init,         /* initialization function */                   \
		NULL,                              /* Power management system. Null if unused */   \
		&__DRIVER_SLUG___mock_data_##inst, /* Initialized data struct above */             \
		NULL,        /* Config struct goes here if you're using it */                      \
		POST_KERNEL, /* When in the boot process to init. Must be after bus */             \
		CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, /* Priority within stage above */             \
		NULL                                 /* TODO: The defined API */                   \
	);

DT_INST_FOREACH_STATUS_OKAY(__DRIVER_UPPER___MOCK_INIT)
