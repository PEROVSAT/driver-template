/*
 * Generated boilerplate — do not edit.
 *
 * Hardware backend: SPI transfer and library initialization.
 */

#include "__DRIVER_SLUG__.h"

#include <errno.h>
#include <string.h>

#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>

int __DRIVER_SLUG___transfer(void *ctx, uint8_t reg, uint8_t *buf, size_t len, bool read)
{
	const struct device *dev = ctx;
	const struct __DRIVER_SLUG___config *config = dev->config;
	uint8_t tx_buf[1 + 32];
	uint8_t rx_buf[1 + 32];
	struct spi_buf tx_spi_buf = { .buf = tx_buf, .len = 1 + len };
	struct spi_buf rx_spi_buf = { .buf = rx_buf, .len = 1 + len };
	struct spi_buf_set tx = { .buffers = &tx_spi_buf, .count = 1 };
	struct spi_buf_set rx = { .buffers = &rx_spi_buf, .count = 1 };
	int ret;

	if (len > sizeof(tx_buf) - 1) {
		return -EINVAL;
	}

	tx_buf[0] = reg;

	if (read) {
		memset(&tx_buf[1], 0, len);
	} else {
		memcpy(&tx_buf[1], buf, len);
	}

	ret = spi_transceive_dt(&config->bus, &tx, &rx);
	if (ret < 0) {
		return ret;
	}

	if (read) {
		memcpy(buf, &rx_buf[1], len);
	}

	return 0;
}

int __DRIVER_SLUG___backend_init(const struct device *dev)
{
	struct __DRIVER_SLUG___data *data = dev->data;
	const struct __DRIVER_SLUG___config *config = dev->config;

	if (!spi_is_ready_dt(&config->bus)) {
		return -ENODEV;
	}

	return __DRIVER_SLUG___lib_init(&data->lib, __DRIVER_SLUG___transfer, (void *)dev);
}
