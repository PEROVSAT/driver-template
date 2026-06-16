#ifndef __DRIVER_UPPER___H_
#define __DRIVER_UPPER___H_

#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>

/* TODO: Swap i2c.h for the correct bus header (SPI, UART, etc.). */

#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
#include "__DRIVER_SLUG___lib.h"
#endif

/** Read-only configuration, populated from devicetree. */
struct __DRIVER_SLUG___config {
	struct i2c_dt_spec i2c;
	/* TODO: Add fields mirroring your devicetree binding properties. */
};

/** Mutable runtime state. */
struct __DRIVER_SLUG___data {
#if defined(CONFIG___KCONFIG_SYM___USES_LIB)
	struct __DRIVER_SLUG___lib lib;
#endif
	/* TODO: Cached samples and driver state. */
};

// TODO: Expose any internal private functions you make, so they can be accessed for unit testing

#endif /* __DRIVER_UPPER___H_ */
