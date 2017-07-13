project( Mechanicca )

cmake_minimum_required(VERSION 3.5)

# Configure project information
set( APPLICATION_NAME ${PROJECT_NAME} )
set( APPLICATION_VERSION 0.1 )
set( APPLICATION_AUTHOR "Martin Kopecky <martin.monster696@gmail.com>" )

if( NOT CMAKE_BUILD_TYPE )
  set( CMAKE_BUILD_TYPE Debug CACHE STRING
       "Choose the type of build, options are: None Debug Release"
       FORCE )
endif()

message( STATUS "Building in [${CMAKE_BUILD_TYPE}] mode." )

# Turn on automatic Qt MOC and UIC invocation
set( CMAKE_AUTOMOC ON )
set( CMAKE_AUTOUIC ON )

# -- Compiler configuration ------------------------------
if( CMAKE_COMPILER_IS_GNUCXX )
	if( CMAKE_CXX_COMPILER_VERSION VERSION_LESS 5.0) 
		message( FATAL_ERROR "${PROJECT_NAME} requires C++14.  G++ must be 5.0 or later, the used version is ${CMAKE_CXX_COMPILER_VERSION}" )
	else()
	 	# C++14 Support
		message( STATUS "Using C++14" ) 
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14" )

		# CXX Flags
		set( CMAKE_CXX_FLAGS "-Wall -Wno-deprecated -Wno-write-strings ${CMAKE_CXX_FLAGS}" )
		
		# Setup shared libraries linker flags
		set( CMAKE_SHARED_LINKER_FLAGS "-Wl,--no-undefined" )
	
		# check platform (32bit / 64bit) 
		if( CMAKE_SIZEOF_VOID_P EQUAL 8 ) 
			message( STATUS "Checking platform: 64-bit" ) 
			set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m64" ) 
		else() 
			message( STATUS "Checking platform: 32-bit") 
		endif() 
	endif()
else()
	message( FATAL_ERROR "Unsupported compiler detected." )
endif( CMAKE_COMPILER_IS_GNUCXX )

# Include Shared library symbol export definition header generator
include( GenerateExportHeader )

# -- Global include directories --------------------------
# Include build directory where generated files are located
set( CMAKE_INCLUDE_CURRENT_DIR ON )

# -- Target directories
# Set where the binaries are built
# Source: http://stackoverflow.com/a/6595001 
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/Bin" )

set( ${APPLICATION_NAME}_ComponentPlugins_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/ComponentPlugins)
set( ${APPLICATION_NAME}_Common_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Common)

# Define DesignRules database
set( DESIGN_RULES_DATABASE_FILE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/DesignRules.db )

# Core
add_subdirectory( Core )