# Provides: SndFile::SndFile

if(APPLE)
    list(APPEND CMAKE_PREFIX_PATH
            /opt/homebrew        # Apple Silicon default
            /usr/local           # Intel default
    )
endif()

find_path(SNDFILE_INCLUDE_DIR sndfile.h
        HINTS ${CMAKE_PREFIX_PATH}/include)

find_library(SNDFILE_LIBRARY NAMES sndfile
        HINTS ${CMAKE_PREFIX_PATH}/lib)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(SndFile
        REQUIRED_VARS SNDFILE_INCLUDE_DIR SNDFILE_LIBRARY)

if(SndFile_FOUND)
    add_library(SndFile::SndFile UNKNOWN IMPORTED)
    set_target_properties(SndFile::SndFile PROPERTIES
            IMPORTED_LOCATION "${SNDFILE_LIBRARY}"
            INTERFACE_INCLUDE_DIRECTORIES "${SNDFILE_INCLUDE_DIR}"
    )
endif()
