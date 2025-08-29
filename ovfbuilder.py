#!/usr/bin/env python3
import argparse, json, os, tarfile, hashlib, subprocess
from string import Template

def qemu_virtual_size_bytes(vmdk: str) -> int:
    info = subprocess.check_output(["qemu-img","info","--output=json", vmdk], text=True)
    return int(json.loads(info)["virtual-size"])

def sha1(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

ap = argparse.ArgumentParser()
ap.add_argument("--vm-name", required=True)
ap.add_argument("--cpus", type=int, default=2)
ap.add_argument("--memory-mb", type=int, default=2048)
ap.add_argument("--nic-type", choices=["E1000","VMXNET3"], default="VMXNET3")
ap.add_argument("--network-name", default="VM Network")
ap.add_argument("--disk", required=True, help="Path to streamOptimized VMDK")
ap.add_argument("--template", required=True, help="Path to ovf_template.xml")
ap.add_argument("--out", required=True, help="Output .ova path")
args = ap.parse_args()

vmdk = args.disk
populated_size = os.path.getsize(vmdk)
virtual_size   = qemu_virtual_size_bytes(vmdk)

with open(args.template, "r", encoding="utf-8") as f:
    ovf_txt = Template(f.read()).substitute(
        vm_name=args.vm_name,
        cpus=args.cpus,
        memory_mb=args.memory_mb,
        nic_type=args.nic_type,
        network_name=args.network_name,
        virtual_size=virtual_size,
        populated_size=populated_size,
    )

ovf = f"{args.vm_name}.ovf"
mf  = f"{args.vm_name}.mf"

with open(ovf, "w", encoding="utf-8") as f:
    f.write(ovf_txt)

with open(mf, "w", encoding="utf-8") as f:
    f.write(f"SHA1({ovf})= {sha1(ovf)}\n")
    f.write(f"SHA1({os.path.basename(vmdk)})= {sha1(vmdk)}\n")

with tarfile.open(args.out, "w", format=tarfile.USTAR_FORMAT) as tar:
    tar.add(ovf, arcname=os.path.basename(ovf))
    tar.add(mf,  arcname=os.path.basename(mf))
    tar.add(vmdk, arcname=os.path.basename(vmdk))

print(f"OVA written: {args.out}")
