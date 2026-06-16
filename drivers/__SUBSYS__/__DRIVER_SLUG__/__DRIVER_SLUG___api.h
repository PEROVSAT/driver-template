#ifndef __DRIVER_UPPER___API_H_
#define __DRIVER_UPPER___API_H_

#include <zephyr/device.h>

/**
 * Public driver API — add one function pointer per operation exposed to the application.
 *
 * Example shape for a single operation:
 *
 *   int (*read_reg)(const struct device *dev, uint8_t reg, uint8_t *val);
 */
struct __DRIVER_SLUG___driver_api {
	/* FILL IN: function pointers for each public operation */
};

#endif /* __DRIVER_UPPER___API_H_ */
