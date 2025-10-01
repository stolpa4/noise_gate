set(noise_gate_tests noise_gate_test)

foreach(test IN LISTS noise_gate_tests)
    add_executable(${test} ${test}.cpp ${test}.hpp)
    target_link_libraries(${test} PRIVATE noise_gate)
    add_test(NAME ${test} COMMAND ${test})
endforeach()
