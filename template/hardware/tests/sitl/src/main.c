/*
 * SITL harness: boots the hardware driver with the SITL emulator backend.
 *
 * TODO: connect Basilisk here once the socket backend is implemented.
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
