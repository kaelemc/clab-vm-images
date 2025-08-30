
# Containerlab VM Images

Prebuilt VM images to get up and running with [containerlab](https://containerlab.dev) as fast as possible.

The images are created using [bootc](https://bootc-dev.github.io/bootc/).

Current formats are:

- OVA 
- VMDK
- QCOW2

## Image info

The images are based on CentOS Stream 9.

Since the images are created with bootc, the distro is immutable.

> [!IMPORTANT]  
> Effectively this means you should use `rpm-ostree` as the package manager, instead of `dnf`

Default credentials are:

|  Username  |  Password  |
|------------|------------|
| `clab`     | `clab`     |

