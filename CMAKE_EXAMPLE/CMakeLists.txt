cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)

# Add the subdirectory for the library
add_subdirectory(lib)

# Add the executable target
add_executable(MyExecutable main.cpp)

# Link the library to the executable
target_link_libraries(MyExecutable PRIVATE MyLibrary)

# Install the executable and the library
install(TARGETS MyExecutable
        DESTINATION bin)

install(TARGETS MyLibrary
        DESTINATION lib)

# Install the header file
install(FILES lib/mylib.h
        DESTINATION include)

# Specify installation rules for other files, such as documentation or resources
# Example: install(FILES README.md DESTINATION share/myproject)

# Include CPack for packaging
include(CPack)

