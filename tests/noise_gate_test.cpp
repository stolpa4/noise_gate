#include "noise_gate_test.hpp"


#include <noise_gate/noise_gate.hpp>      // craft_greeting

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h" // TEST_CASE, SUBCASE, CHECK, REQUIRE

TEST_CASE("Greeting is working") {
    SUBCASE("Simple name greeting") {
        CHECK(craft_greeting("John") == "Hello, John!");
        CHECK(craft_greeting("Jane") == "Hello, Jane!");
        REQUIRE(craft_greeting("Robin") == "Hello, Robin!");
    }
}
