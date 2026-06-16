/*
 * Generated boilerplate — do not edit.
 *
 * Simulation backend: socket transfer and library initialization.
 *
 * FILL IN (simulation only): open a socket on init, serialize register read/write
 * requests, and block until Basilisk returns the response.
 */

#include "__DRIVER_SLUG__.h"

#include <errno.h>

#include <zephyr/device.h>

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	ARG_UNUSED(ctx);
	ARG_UNUSED(reg);
	ARG_UNUSED(buf);
	ARG_UNUSED(len);
	ARG_UNUSED(read);

	return -ENOTSUP;
}

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	struct __DRIVER_SLUG___data *data = dev->data;

	return __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
}
