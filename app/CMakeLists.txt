set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

add_executable(noise_gate_app app.cpp)
target_include_directories(noise_gate_app PRIVATE ${CMAKE_SOURCE_DIR})

find_package(SndFile REQUIRED)
target_link_libraries(noise_gate_app
        PRIVATE
        noise_gate
        SndFile::SndFile
)

install(TARGETS noise_gate_app RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
