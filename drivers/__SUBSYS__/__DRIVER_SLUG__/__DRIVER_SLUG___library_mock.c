#include "__DRIVER_SLUG__.h"

#include <string.h>

/*
 * Library mock backend: serve static register data without a real bus.
 *
 * The register map is populated with canned values for integration tests.
 */

#define __DRIVER_UPPER___REGISTER_MAP_SIZE 256

static uint8_t register_map[__DRIVER_UPPER___REGISTER_MAP_SIZE];

static void __DRIVER_SLUG___library_mock_init_once(void)
{
	static bool initialized;

	if (initialized) {
		return;
	}

	memset(register_map, 0, sizeof(register_map));

	/* TODO: Seed register_map with device-specific defaults. */
	register_map[0x00] = 0x00;
	register_map[0x01] = 0x00;
	register_map[0x02] = 0x00;
	register_map[0x03] = 0x2A;

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
