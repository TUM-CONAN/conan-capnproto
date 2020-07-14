from conans import CMake, ConanFile, tools
import os


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

    _src_folder = "capnproto-c++-%s" % version

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

        cmake.configure(source_folder=self._src_folder)
        return cmake

    def build(self):
        cmake = self._cmake_configure()

        if self.settings.os == "Linux":
            tools.replace_in_file(os.path.join(self._src_folder, "cmake", "CapnProtoMacros.cmake"),
                'COMMAND "${CAPNP_EXECUTABLE}"',
                'COMMAND ${CMAKE_COMMAND} -E env "LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/lib:$ENV{LD_LIBRARY_PATH}" ${CAPNP_EXECUTABLE}'
                )
       
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.lib = tools.collect_libs(self)