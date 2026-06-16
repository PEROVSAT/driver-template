#include "__DRIVER_SLUG__.h"

#include <errno.h>

/*
 * Simulation backend: exchange register traffic with Basilisk over a socket.
 *
 * TODO: Open a socket on init, serialize register read/write requests, and
 *       block until Basilisk returns the response.
 */

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	ARG_UNUSED(ctx);
	ARG_UNUSED(reg);
	ARG_UNUSED(buf);
	ARG_UNUSED(len);
	ARG_UNUSED(read);

	return -ENOTSUP;
}
