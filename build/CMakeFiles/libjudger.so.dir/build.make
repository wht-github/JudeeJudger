# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.14

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/wang/Workspace/OJ/Judee

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/wang/Workspace/OJ/Judee/build

# Include any dependencies generated for this target.
include CMakeFiles/libjudger.so.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/libjudger.so.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/libjudger.so.dir/flags.make

CMakeFiles/libjudger.so.dir/src/argtable3.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/argtable3.o: ../src/argtable3.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/libjudger.so.dir/src/argtable3.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/argtable3.o   -c /home/wang/Workspace/OJ/Judee/src/argtable3.c

CMakeFiles/libjudger.so.dir/src/argtable3.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/argtable3.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/argtable3.c > CMakeFiles/libjudger.so.dir/src/argtable3.i

CMakeFiles/libjudger.so.dir/src/argtable3.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/argtable3.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/argtable3.c -o CMakeFiles/libjudger.so.dir/src/argtable3.s

CMakeFiles/libjudger.so.dir/src/child.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/child.o: ../src/child.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/libjudger.so.dir/src/child.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/child.o   -c /home/wang/Workspace/OJ/Judee/src/child.c

CMakeFiles/libjudger.so.dir/src/child.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/child.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/child.c > CMakeFiles/libjudger.so.dir/src/child.i

CMakeFiles/libjudger.so.dir/src/child.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/child.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/child.c -o CMakeFiles/libjudger.so.dir/src/child.s

CMakeFiles/libjudger.so.dir/src/killer.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/killer.o: ../src/killer.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/libjudger.so.dir/src/killer.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/killer.o   -c /home/wang/Workspace/OJ/Judee/src/killer.c

CMakeFiles/libjudger.so.dir/src/killer.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/killer.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/killer.c > CMakeFiles/libjudger.so.dir/src/killer.i

CMakeFiles/libjudger.so.dir/src/killer.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/killer.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/killer.c -o CMakeFiles/libjudger.so.dir/src/killer.s

CMakeFiles/libjudger.so.dir/src/logger.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/logger.o: ../src/logger.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/libjudger.so.dir/src/logger.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/logger.o   -c /home/wang/Workspace/OJ/Judee/src/logger.c

CMakeFiles/libjudger.so.dir/src/logger.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/logger.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/logger.c > CMakeFiles/libjudger.so.dir/src/logger.i

CMakeFiles/libjudger.so.dir/src/logger.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/logger.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/logger.c -o CMakeFiles/libjudger.so.dir/src/logger.s

CMakeFiles/libjudger.so.dir/src/main.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/main.o: ../src/main.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/libjudger.so.dir/src/main.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/main.o   -c /home/wang/Workspace/OJ/Judee/src/main.c

CMakeFiles/libjudger.so.dir/src/main.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/main.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/main.c > CMakeFiles/libjudger.so.dir/src/main.i

CMakeFiles/libjudger.so.dir/src/main.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/main.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/main.c -o CMakeFiles/libjudger.so.dir/src/main.s

CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o: ../src/rules/c_cpp.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o   -c /home/wang/Workspace/OJ/Judee/src/rules/c_cpp.c

CMakeFiles/libjudger.so.dir/src/rules/c_cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/rules/c_cpp.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/rules/c_cpp.c > CMakeFiles/libjudger.so.dir/src/rules/c_cpp.i

CMakeFiles/libjudger.so.dir/src/rules/c_cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/rules/c_cpp.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/rules/c_cpp.c -o CMakeFiles/libjudger.so.dir/src/rules/c_cpp.s

CMakeFiles/libjudger.so.dir/src/rules/general.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/rules/general.o: ../src/rules/general.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/libjudger.so.dir/src/rules/general.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/rules/general.o   -c /home/wang/Workspace/OJ/Judee/src/rules/general.c

CMakeFiles/libjudger.so.dir/src/rules/general.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/rules/general.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/rules/general.c > CMakeFiles/libjudger.so.dir/src/rules/general.i

CMakeFiles/libjudger.so.dir/src/rules/general.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/rules/general.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/rules/general.c -o CMakeFiles/libjudger.so.dir/src/rules/general.s

CMakeFiles/libjudger.so.dir/src/runner.o: CMakeFiles/libjudger.so.dir/flags.make
CMakeFiles/libjudger.so.dir/src/runner.o: ../src/runner.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/libjudger.so.dir/src/runner.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libjudger.so.dir/src/runner.o   -c /home/wang/Workspace/OJ/Judee/src/runner.c

CMakeFiles/libjudger.so.dir/src/runner.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libjudger.so.dir/src/runner.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/wang/Workspace/OJ/Judee/src/runner.c > CMakeFiles/libjudger.so.dir/src/runner.i

CMakeFiles/libjudger.so.dir/src/runner.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libjudger.so.dir/src/runner.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/wang/Workspace/OJ/Judee/src/runner.c -o CMakeFiles/libjudger.so.dir/src/runner.s

# Object files for target libjudger.so
libjudger_so_OBJECTS = \
"CMakeFiles/libjudger.so.dir/src/argtable3.o" \
"CMakeFiles/libjudger.so.dir/src/child.o" \
"CMakeFiles/libjudger.so.dir/src/killer.o" \
"CMakeFiles/libjudger.so.dir/src/logger.o" \
"CMakeFiles/libjudger.so.dir/src/main.o" \
"CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o" \
"CMakeFiles/libjudger.so.dir/src/rules/general.o" \
"CMakeFiles/libjudger.so.dir/src/runner.o"

# External object files for target libjudger.so
libjudger_so_EXTERNAL_OBJECTS =

../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/argtable3.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/child.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/killer.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/logger.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/main.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/rules/c_cpp.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/rules/general.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/src/runner.o
../output/libjudger.so: CMakeFiles/libjudger.so.dir/build.make
../output/libjudger.so: CMakeFiles/libjudger.so.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/wang/Workspace/OJ/Judee/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Linking C executable ../output/libjudger.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/libjudger.so.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/libjudger.so.dir/build: ../output/libjudger.so

.PHONY : CMakeFiles/libjudger.so.dir/build

CMakeFiles/libjudger.so.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/libjudger.so.dir/cmake_clean.cmake
.PHONY : CMakeFiles/libjudger.so.dir/clean

CMakeFiles/libjudger.so.dir/depend:
	cd /home/wang/Workspace/OJ/Judee/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/wang/Workspace/OJ/Judee /home/wang/Workspace/OJ/Judee /home/wang/Workspace/OJ/Judee/build /home/wang/Workspace/OJ/Judee/build /home/wang/Workspace/OJ/Judee/build/CMakeFiles/libjudger.so.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/libjudger.so.dir/depend

