#ifndef __DRIVER_UPPER___H_
#define __DRIVER_UPPER___H_

#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>

/* TODO: Swap i2c.h for the correct bus header (SPI, etc.). */

/** Read-only configuration, populated from devicetree. */
struct __DRIVER_SLUG___config {
	struct i2c_dt_spec i2c;
	/* TODO: Add fields mirroring your devicetree binding properties. */
};

/** Mutable runtime state. */
struct __DRIVER_SLUG___data {
	/* TODO: Cached samples and driver state. */
};

#endif /* __DRIVER_UPPER___H_ */
