/*
 * Generated boilerplate — do not edit.
 *
 * Hardware backend: I2C transfer and library initialization.
 */

#include "__DRIVER_SLUG__.h"

#include <string.h>

#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	const struct device *dev = ctx;
	const struct __DRIVER_SLUG___config *config = dev->config;

	if (read) {
		return i2c_write_read_dt(&config->i2c, &reg, 1, buf, len);
	}

	uint8_t tx[1 + 32];

	if (len > sizeof(tx) - 1) {
		return -EINVAL;
	}

	tx[0] = reg;
	memcpy(&tx[1], buf, len);

	return i2c_write_dt(&config->i2c, tx, len + 1);
}

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	struct __DRIVER_SLUG___data *data = dev->data;
	const struct __DRIVER_SLUG___config *config = dev->config;

	if (!i2c_is_ready_dt(&config->i2c)) {
		return -ENODEV;
	}

	return __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
}
