/*
 * Implement your device here — public-mock API operations.
 *
 * Return hardcoded values for CI and repos without NDA library access.
 * Register implementations in __DRIVER_SLUG___api below.
 */

#include "__DRIVER_SLUG__.h"

/* FILL IN: static functions returning hardcoded values
 *
 * static int read_reg(const struct device *dev, uint8_t reg, uint8_t *val)
 * {
 *     ARG_UNUSED(dev);
 *     ARG_UNUSED(reg);
 *     *val = 0x00;
 *     return 0;
 * }
 */

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	ARG_UNUSED(dev);

	return 0;
}

const struct __DRIVER_SLUG___driver_api __DRIVER_SLUG___api = {
	/* FILL IN: .read_reg = read_reg, */
};
