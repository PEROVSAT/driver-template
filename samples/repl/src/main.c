#include <zephyr/device.h>
#include <zephyr/shell/shell.h>

#include <__DRIVER_SLUG__.h>

static __DRIVER_SLUG___t *sh_dev(const struct shell *sh)
{
	const struct device *zdev = DEVICE_DT_GET(DT_ALIAS(__DRIVER_SLUG__));

	if (!device_is_ready(zdev)) {
		shell_error(sh, "device not ready");
		return NULL;
	}

	return __DRIVER_SLUG___from_dev(zdev);
}

static int cmd_status(const struct shell *sh, size_t argc, char **argv)
{
	__DRIVER_SLUG___t *dev = sh_dev(sh);

	ARG_UNUSED(argc);
	ARG_UNUSED(argv);

	if (dev == NULL) {
		return -ENODEV;
	}

	/* FILL IN: call other public APIs via this same from_dev handle. */
	shell_print(sh, "ready");
	return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(__DRIVER_SLUG___cmds,
			       SHELL_CMD(status, NULL, "Check the driver is ready", cmd_status),
			       SHELL_SUBCMD_SET_END);

SHELL_CMD_REGISTER(__DRIVER_SLUG__, &__DRIVER_SLUG___cmds, "__DRIVER_UPPER__ driver", NULL);

int main(void)
{
	return 0;
}
