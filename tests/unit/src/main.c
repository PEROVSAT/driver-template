/*
 * Unit tests for the portable __DRIVER_SLUG__ device library.
 *
 * These tests exercise protocol logic with a fake transfer function and do not
 * require the Zephyr driver or a real bus.
 */

#include <errno.h>
#include <string.h>

#include <zephyr/ztest.h>

#include "__DRIVER_SLUG___lib.h"

static uint8_t fake_register_map[256];

static int fake_transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	ARG_UNUSED(ctx);

	if (reg + len > sizeof(fake_register_map)) {
		return -EINVAL;
	}

	if (read) {
		memcpy(buf, &fake_register_map[reg], len);
	} else {
		memcpy(&fake_register_map[reg], buf, len);
	}

	return 0;
}

ZTEST(__DRIVER_SLUG___unit, test_boot)
{
	zassert_true(true);
}

/*
 * FILL IN: unit tests for lib/__DRIVER_SLUG__/__DRIVER_SLUG___lib.c, e.g.:
 *
 * ZTEST(__DRIVER_SLUG___unit, test_lib_read_reg)
 * {
 *     struct __DRIVER_SLUG___lib lib;
 *     uint8_t val;
 *     int ret;
 *
 *     memset(fake_register_map, 0, sizeof(fake_register_map));
 *     fake_register_map[0x75] = 0x68;
 *
 *     ret = __DRIVER_SLUG___lib_init(&lib, fake_transfer, NULL);
 *     zassert_ok(ret);
 *
 *     ret = __DRIVER_SLUG___lib_read_reg(&lib, 0x75, &val);
 *     zassert_ok(ret);
 *     zassert_equal(val, 0x68);
 * }
 */

ZTEST_SUITE(__DRIVER_SLUG___unit, NULL, NULL, NULL, NULL, NULL);
