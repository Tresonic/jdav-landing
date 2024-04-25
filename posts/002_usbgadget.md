# USB-CDC-Gadget Orange Pi Zero +2 H3
with Armbian bullseye 5.15.93-sunxi

In `/etc/modules` add:
```g_cdc```

To fix MAC addresses add `/etc/modprobe.d/g_cdc.conf` with:

```options g_cdc dev_addr=12:34:56:78:9a:bc host_addr=12:34:56:78:9a:bd```

## Manual IPs
On the gadget:

```nmcli con add type ethernet ifname usb0 con-name usb-con ip4 10.0.0.2/24 gw4 10.0.0.1 ipv4.dns 8.8.8.8```

On the host:

```nmcli con add type ethernet mac 12:34:56:78:9a:bd con-name usb-con ip4 10.0.0.1/24 ipv4.method shared```

Activate connection on both sides:

```nmcli con up usb-con```
