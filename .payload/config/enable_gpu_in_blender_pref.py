import enum
import bpy

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-15s %(levelname)8s : %(message)s'
)

log = logging.getLogger("enable_gpu_in_blender_pref")


class DeviceType(enum.StrEnum):
    CUDA = "CUDA"
    OPTIX = "OPTIX"


# Todo
class Backend(enum.StrEnum):
    OPENCL = "OPENCL"
    VULKAN = "VULKAN"


# References:
# - [](https://blender.stackexchange.com/a/256665/152092)

def enable_gpus(device_type, use_cpus=False):

    log.warning(f"Trying to enable GPUs in Blender Preferences: {device_type}")
    log.warning(f"Trying to enable CPU in Blender Preferences: {use_cpus}")

    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cycles_preferences.refresh_devices()
    devices = cycles_preferences.devices

    if not devices:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []

    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)

        log.warning(f"{device.name} [{list(devices).index(device)}] enabled: {device.use}")

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    log.info(f"Activated GPUs: {activated_gpus}")

    return activated_gpus


enable_gpus(
    device_type=DeviceType.OPTIX,
    use_cpus=True,
)
