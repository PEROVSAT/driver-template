/*
 * Generated boilerplate — do not edit.
 *
 * Library-mock backend: static register map transfer and library initialization.
 */

#include "__DRIVER_SLUG__.h"

#include <string.h>

#include <zephyr/device.h>

#define __DRIVER_UPPER___REGISTER_MAP_SIZE 256

static uint8_t register_map[__DRIVER_UPPER___REGISTER_MAP_SIZE];

static void __DRIVER_SLUG___library_mock_init_once(void)
{
	static bool initialized;

	if (initialized) {
		return;
	}

	memset(register_map, 0, sizeof(register_map));
	initialized = true;
}

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	ARG_UNUSED(ctx);

	__DRIVER_SLUG___library_mock_init_once();

	if (reg + len > sizeof(register_map)) {
		return -EINVAL;
	}

	if (read) {
		memcpy(buf, &register_map[reg], len);
	} else {
		memcpy(&register_map[reg], buf, len);
	}

	return 0;
}

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	struct __DRIVER_SLUG___data *data = dev->data;

	return __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
}
