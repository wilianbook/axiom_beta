#!/bin/sh

# echo fclk0 >/sys/devices/axi.0/f8007000.ps7-dev-cfg/fclk_export
# echo fclk1 >/sys/devices/axi.0/f8007000.ps7-dev-cfg/fclk_export
# echo fclk2 >/sys/devices/axi.0/f8007000.ps7-dev-cfg/fclk_export
# echo fclk3 >/sys/devices/axi.0/f8007000.ps7-dev-cfg/fclk_export

echo fclk0 >/sys/devices/soc0/axi\@0/f8007000.ps7-dev-cfg/fclk_export
echo fclk1 >/sys/devices/soc0/axi\@0/f8007000.ps7-dev-cfg/fclk_export
echo fclk2 >/sys/devices/soc0/axi\@0/f8007000.ps7-dev-cfg/fclk_export
echo fclk3 >/sys/devices/soc0/axi\@0/f8007000.ps7-dev-cfg/fclk_export

echo 100000000 >/sys/class/fclk/fclk0/set_rate	# 100MHz
echo  10000000 >/sys/class/fclk/fclk1/set_rate	# 10MHz
echo 100000000 >/sys/class/fclk/fclk2/set_rate	# 100MHz
echo 125000000 >/sys/class/fclk/fclk3/set_rate	# 125MHz

