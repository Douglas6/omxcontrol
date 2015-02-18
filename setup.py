import distutils.core

distutils.core.setup(
    name = "omxcontrol",
    version = "0.0.1",
    packages = ["."],
    requires = ["dbus"]
)
