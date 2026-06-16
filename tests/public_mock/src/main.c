/*
 * Integration tests for the __DRIVER_SLUG__ driver with the public-mock backend.
 *
 * This suite builds without the device library and is safe for CI and repos
 * without NDA library access.
 */

#include <zephyr/device.h>
#include <zephyr/ztest.h>

#include "__DRIVER_SLUG__.h"

ZTEST(__DRIVER_SLUG___public_mock, test_boot)
{
	/* Placeholder: remove once real integration tests are added. */
	zassert_true(true);
}

ZTEST_SUITE(__DRIVER_SLUG___public_mock, NULL, NULL, NULL, NULL, NULL);
