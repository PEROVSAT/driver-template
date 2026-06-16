/*
 * Implement your device here — lib-backed API operations.
 *
 * Each static function delegates to the portable library in lib/__DRIVER_SLUG__/.
 * Register implementations in __DRIVER_SLUG___api below.
 */

#include "__DRIVER_SLUG__.h"

/* FILL IN: static functions that call into lib/__DRIVER_SLUG__/__DRIVER_SLUG___lib.c
 *
 * static int read_reg(const struct device *dev, uint8_t reg, uint8_t *val)
 * {
 *     struct __DRIVER_SLUG___data *data = dev->data;
 *
 *     return __DRIVER_SLUG___lib_read_reg(&data->lib, reg, val);
 * }
 */

const struct __DRIVER_SLUG___driver_api __DRIVER_SLUG___api = {
	/* FILL IN: .read_reg = read_reg, */
};
