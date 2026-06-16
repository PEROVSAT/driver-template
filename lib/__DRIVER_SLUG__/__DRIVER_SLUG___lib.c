#include "__DRIVER_SLUG___lib.h"

#include <errno.h>

/*
 * Data flow:
 *   driver init -> lib_init(lib, transfer_fn, dev)   injects bus I/O
 *   lib fn      -> lib->transfer(ctx, reg, buf, len, read)
 *   backend     -> __DRIVER_SLUG___transfer() in _hardware.c / _simulation.c / _library_mock.c
 *
 * To read a register: lib->transfer(lib->ctx, REG_ADDR, &val, 1, true);
 */

/* FILL IN: register addresses and protocol constants */

static int __DRIVER_SLUG___lib_transfer(struct __DRIVER_SLUG___lib *lib, uint8_t reg,
					uint8_t *buf, size_t len, bool read)
	__attribute__((unused));
static int __DRIVER_SLUG___lib_transfer(struct __DRIVER_SLUG___lib *lib, uint8_t reg,
					uint8_t *buf, size_t len, bool read)
{
	if (lib == NULL || lib->transfer == NULL) {
		return -EINVAL;
	}

	return lib->transfer(lib->ctx, reg, buf, len, read);
}

int __DRIVER_SLUG___lib_init(struct __DRIVER_SLUG___lib *lib, __DRIVER_SLUG___transfer_fn transfer,
			     void *ctx)
{
	if (lib == NULL || transfer == NULL) {
		return -EINVAL;
	}

	lib->transfer = transfer;
	lib->ctx = ctx;

	/* FILL IN: probe device and apply initial configuration */

	return 0;
}

/* FILL IN: protocol functions, e.g.:
 *
 * int __DRIVER_SLUG___lib_read_reg(struct __DRIVER_SLUG___lib *lib, uint8_t reg, uint8_t *val)
 * {
 *     if (lib == NULL || val == NULL) {
 *         return -EINVAL;
 *     }
 *     return __DRIVER_SLUG___lib_transfer(lib, reg, val, 1, true);
 * }
 */
