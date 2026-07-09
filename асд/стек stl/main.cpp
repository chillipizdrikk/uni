#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <stack>
#include <iostream>

using namespace std;


TEST_CASE("Test 1 (Stack STL)") {
    stack<int> st;
    REQUIRE(st.empty() == true);
    st.push(1);
    REQUIRE(st.top() == 1);
    REQUIRE(st.empty() == false);
    st.pop();
    REQUIRE(st.empty() == true);
}

TEST_CASE("Test 2 (Stack STL)") {
    stack<int> st;
    REQUIRE(st.empty() == true);
    st.push(5);
    REQUIRE(st.empty() == false);
    REQUIRE(st.top() == 5);
    st.push(10);
    REQUIRE(st.top() == 10);
    st.pop();
    REQUIRE(st.top() == 5);
    REQUIRE(st.empty() == false);
    st.pop();
    REQUIRE(st.empty() == true);
}

TEST_CASE("Test 3 (Stack STL)") {
    stack<int> st;
    const int n = 100;
    for (int i = 0; i < n; i++) {
        st.push(i);
        REQUIRE(st.top() == i);
    }
    for (int i = n - 1; i >= 0; i--) {
        REQUIRE(st.top() == i);
        st.pop();
    }
}