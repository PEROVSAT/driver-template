#include "__DRIVER_SLUG___lib.h"

#include <errno.h>

/* TODO: Define register addresses and protocol constants. */
#define __DRIVER_UPPER___REG_SAMPLE 0x00

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

	/* TODO: Probe device and apply initial configuration. */

	return 0;
}

int __DRIVER_SLUG___lib_read_sample(struct __DRIVER_SLUG___lib *lib,
				    struct __DRIVER_SLUG___sample *sample)
{
	uint8_t raw[4];
	int ret;

	if (lib == NULL || sample == NULL) {
		return -EINVAL;
	}

	ret = __DRIVER_SLUG___lib_transfer(lib, __DRIVER_UPPER___REG_SAMPLE, raw, sizeof(raw), true);
	if (ret < 0) {
		return ret;
	}

	/* TODO: Decode raw bytes into a sample according to the device protocol. */
	sample->value = (int32_t)((raw[0] << 24) | (raw[1] << 16) | (raw[2] << 8) | raw[3]);

	return 0;
}
