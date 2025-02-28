# Define the library
add_library(MyLibrary STATIC mylib.cpp)

# Specify include directories for the library
target_include_directories(MyLibrary PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Install the library
install(TARGETS MyLibrary
        DESTINATION lib)

# Install the header file
install(FILES mylib.h
        DESTINATION include)

