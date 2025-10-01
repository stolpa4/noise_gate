cmake_minimum_required(VERSION 3.23)

## Common things
################

if (NOT DEFINED CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 20)
endif()

set(CMAKE_CXX_EXTENSIONS OFF)

project(
        noise_gate
        VERSION 1.0.0
        DESCRIPTION "Library for audio noise reduction"
        LANGUAGES CXX C)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/Modules")

## Library and sources
######################

add_library(noise_gate SHARED)

set(noise_gate_source_files noise_gate)
list(TRANSFORM noise_gate_source_files PREPEND "${PROJECT_SOURCE_DIR}/noise_gate/")

set(noise_gate_private_sources ${noise_gate_source_files})
list(TRANSFORM noise_gate_private_sources APPEND ".cpp")

set(noise_gate_public_headers ${noise_gate_source_files})
list(TRANSFORM noise_gate_public_headers APPEND ".hpp")

target_sources(noise_gate
        PRIVATE ${noise_gate_private_sources}
        PUBLIC FILE_SET HEADERS
        BASE_DIRS ${noise_gate_SOURCE_DIR}
        FILES ${noise_gate_public_headers})

## Compiler set up

## Compiler specific things
###########################

include(CheckCXXCompilerFlag)

target_compile_options(noise_gate PRIVATE -Wall -Wextra -Wshadow -Wnon-virtual-dtor -pedantic -Wold-style-cast -Wcast-align -Wunused
        -Woverloaded-virtual -Wpedantic -Wconversion -Wsign-conversion -Wmisleading-indentation
        -Wduplicated-cond -Wduplicated-branches -Wlogical-op -Wnull-dereference -Wuseless-cast
        -Wdouble-promotion -Wformat=2 -Wimplicit-fallthrough -Wuninitialized -Wmaybe-uninitialized
        -Wno-unknown-pragmas -Wno-unknown-warning-option)

## This feature is relatively new for gcc, checking for it separately
check_cxx_compiler_flag("-Wanalyzer-use-of-uninitialized-value" SUPPORTS_WANALYZER_USE_OF_UNINITIALIZED_VALUE)
if(SUPPORTS_WANALYZER_USE_OF_UNINITIALIZED_VALUE)
    message(STATUS "Compiler supports -Wanalyzer-use-of-uninitialized-value")
    target_compile_options(noise_gate PRIVATE -Wanalyzer-use-of-uninitialized-value)
else()
    message(STATUS "Compiler does not support -Wanalyzer-use-of-uninitialized-value")
endif()



option(SANITIZE_ADDRESS "Enable address sanitizer" OFF)
option(SANITIZE_UB "Enable undefined behaviour sanitizer" OFF)
option(SANITIZE_LEAK "Enable memory leak sanitizer" OFF)

if(SANITIZE_ADDRESS)
    message(STATUS "Building with sanitize address")
    target_compile_options(noise_gate PRIVATE -fsanitize=address -fno-omit-frame-pointer)
    target_link_options(noise_gate PRIVATE -fsanitize=address)
endif()

if(SANITIZE_UB)
    message(STATUS "Building with sanitize UB")
    target_compile_options(noise_gate PRIVATE -fsanitize=undefined)
    target_link_options(noise_gate PRIVATE -fsanitize=undefined)
endif()

if(SANITIZE_LEAK)
    # This is not supported for arm darwin
    check_cxx_compiler_flag("-fsanitize=leak" SUPPORTS_SANITIZE_LEAK)
    if(SUPPORTS_SANITIZE_LEAK)
        message(STATUS "Building with sanitize leak")
        target_compile_options(noise_gate PRIVATE -fsanitize=leak)
        target_link_options(noise_gate PRIVATE -fsanitize=leak)
    endif()
endif()


## Linker set up
################

# Find and link some libraries here
#find_library(AVFORMAT_LIBRARY avformat)

#set(noise_gate_common_link_libs ${AVFORMAT_LIBRARY})
#target_link_libraries(noise_gate ${noise_gate_common_link_libs})

# Find the lib include directories
#find_path(AVFORMAT_INCLUDE_DIR libavformat/avformat.h)

#target_include_directories(noise_gate PUBLIC ${AVFORMAT_INCLUDE_DIR})

# Or try an alternative:
#find_package(FFMPEG REQUIRED COMPONENTS avformat)

#target_link_libraries(noise_gate PUBLIC FFMPEG::avformat)

## Tests
########

option(BUILD_TESTS "build the tests" OFF)
if(BUILD_TESTS)
    message(STATUS "Building tests")
    enable_testing()
    add_subdirectory(tests)
endif()


## App
######

option(BUILD_APP "build the app" OFF)
if(BUILD_APP)
    message(STATUS "Building app")
    add_subdirectory(app)
endif()

## Installation
###############

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS noise_gate
        EXPORT noise_gate-targets
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(EXPORT noise_gate-targets
        FILE noise_gate-targets.cmake
        NAMESPACE noise_gate::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/noise_gate
)

configure_package_config_file(
        cmake/noise_gate-config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/noise_gate-config.cmake
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/noise_gate
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/noise_gate-config.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/noise_gate
)
