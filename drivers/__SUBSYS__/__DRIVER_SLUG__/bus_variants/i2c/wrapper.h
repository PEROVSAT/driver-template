#ifndef __DRIVER_UPPER___H_
#define __DRIVER_UPPER___H_

#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>

#include "__DRIVER_SLUG___api.h"

#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
#include "__DRIVER_SLUG___lib.h"
#endif

/** Read-only configuration, populated from devicetree. */
struct __DRIVER_SLUG___config {
	struct i2c_dt_spec bus;
	/* FILL IN: additional fields mirroring your devicetree binding properties */
};

/** Mutable runtime state. */
struct __DRIVER_SLUG___data {
#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
	struct __DRIVER_SLUG___lib lib;
#endif
	/* FILL IN: cached samples and driver state */
};

#endif /* __DRIVER_UPPER___H_ */
