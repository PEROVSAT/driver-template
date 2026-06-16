#ifndef __DRIVER_UPPER___LIB_H_
#define __DRIVER_UPPER___LIB_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/**
 * Bus-agnostic byte transfer callback.
 *
 * @param ctx  Opaque context (typically the Zephyr device pointer).
 * @param reg  Register address or protocol offset.
 * @param buf  Data buffer.
 * @param len  Length of @p buf.
 * @param read true for read, false for write.
 *
 * @return 0 on success, negative errno on failure.
 */
typedef int (*__DRIVER_SLUG___transfer_fn)(void *ctx, uint8_t reg, uint8_t *buf, size_t len,
					   bool read);

/** Portable device library state (protocol logic, no Zephyr dependency). */
struct __DRIVER_SLUG___lib {
	__DRIVER_SLUG___transfer_fn transfer;
	void *ctx;
	/* FILL IN: protocol/runtime state */
};

/**
 * Initialize the device library with an injected transfer function.
 *
 * @param lib       Library instance to initialize.
 * @param transfer  Bus transfer callback.
 * @param ctx       Opaque context passed to @p transfer.
 *
 * @return 0 on success, negative errno on failure.
 */
int __DRIVER_SLUG___lib_init(struct __DRIVER_SLUG___lib *lib, __DRIVER_SLUG___transfer_fn transfer,
			     void *ctx);

/* FILL IN: declare protocol functions that use lib->transfer(), e.g.:
 *
 * int __DRIVER_SLUG___lib_read_reg(struct __DRIVER_SLUG___lib *lib, uint8_t reg, uint8_t *val);
 */

#endif /* __DRIVER_UPPER___LIB_H_ */
