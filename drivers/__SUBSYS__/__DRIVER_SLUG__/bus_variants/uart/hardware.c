/*
 * Generated boilerplate — do not edit.
 *
 * Hardware backend: UART transfer and library initialization.
 *
 * FILL IN: implement device-specific UART framing (register address + payload).
 */

#include "__DRIVER_SLUG__.h"

#include <errno.h>

#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	const struct device *dev = ctx;
	const struct __DRIVER_SLUG___config *config = dev->config;

	ARG_UNUSED(reg);
	ARG_UNUSED(buf);
	ARG_UNUSED(len);
	ARG_UNUSED(read);

	if (!device_is_ready(config->bus)) {
		return -ENODEV;
	}

	return -ENOTSUP;
}

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	struct __DRIVER_SLUG___data *data = dev->data;
	const struct __DRIVER_SLUG___config *config = dev->config;

	if (!device_is_ready(config->bus)) {
		return -ENODEV;
	}

	return __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
}
