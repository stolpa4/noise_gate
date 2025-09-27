set(noise_gate_tests noise_gate_test)

foreach(test ${noise_gate_tests})

    add_executable(${test} ${test}.cpp ${test}.hpp)
    target_include_directories(${test} PRIVATE ${CMAKE_SOURCE_DIR})
    target_link_libraries(${test} PRIVATE noise_gate)

    install(TARGETS ${test}
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
            ARCHIVE DESTINATION lib
            INCLUDES DESTINATION include
            FILE_SET HEADERS)

endforeach()
