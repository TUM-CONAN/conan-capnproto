from conans import CMake, ConanFile, tools


class CapNProtoConan(ConanFile):
    name = "capnproto"
    version = tools.get_env("GIT_TAG", "0.8.0")
    license = "MIT"
    description = "Cap'n Proto serialization/RPC system"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {
        "shared": [True, False],
    }

    default_options = {
        "shared": True,
    }

    def source(self):
        tools.get("https://capnproto.org/capnproto-c++-%s.tar.gz" % self.version)

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure(source_folder="capnproto-c++-%s" % self.version)
        return cmake

    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.lib = tools.collect_libs(self)