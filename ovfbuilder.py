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
ap.add_argument("--disk", required=True, help="Path to streamOptimized VMDK")
ap.add_argument("--template", required=True, help="Path to ovf_template.xml")
ap.add_argument("--out", required=True, help="Output .ova path")
args = ap.parse_args()

vmdk = args.disk
populated_size = os.path.getsize(vmdk)
virtual_size   = qemu_virtual_size_bytes(vmdk)

# Derive VM name from VMDK filename
vm_name = os.path.splitext(os.path.basename(vmdk))[0]
vmdk_filename = f"{vm_name}.vmdk"

with open(args.template, "r", encoding="utf-8") as f:
    ovf_txt = Template(f.read()).substitute(
        vm_name=vm_name,
        virtual_size=virtual_size,
        populated_size=populated_size,
    )

ovf = f"{vm_name}.ovf"
mf  = f"{vm_name}.mf"

with open(ovf, "w", encoding="utf-8") as f:
    f.write(ovf_txt)

with open(mf, "w", encoding="utf-8") as f:
    f.write(f"SHA1({ovf})= {sha1(ovf)}\n")
    f.write(f"SHA1({vmdk_filename})= {sha1(vmdk)}\n")

with tarfile.open(args.out, "w", format=tarfile.USTAR_FORMAT) as tar:
    tar.add(ovf, arcname=os.path.basename(ovf))
    tar.add(mf,  arcname=os.path.basename(mf))
    tar.add(vmdk, arcname=vmdk_filename)

print(f"OVA written: {args.out}")
