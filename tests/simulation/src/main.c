/*
 * Simulation harness: boots the driver with the simulation backend.
 *
 * TODO: Connect Basilisk here once the socket backend is implemented.
 */

#include <zephyr/kernel.h>

int main(void)
{
	/* connect Basilisk here */

	while (true) {
		k_sleep(K_FOREVER);
	}

	return 0;
}
