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

# Set CMake modules location
set( CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/Scripts/CMake/Modules" )
set( COMPONENT_GENERATORS_DIR ${CMAKE_SOURCE_DIR}/Scripts/Generators ) 

# -- Target directories
# Set where the binaries are built
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/Bin" )

# Unify the way the directories are named and referenced
set( APPLICATION_COMPONENT_PLUGINS_DIR ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/ComponentPlugins)
set( APPLICATION_COMMON_DIR ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Common)

# Define DesignRules database
set( APPLICATION_DESIGN_RULES_DATABASE_FILE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/DesignRules.db )

# -- SQLite ----------------------------------------------
find_package( SQLite3 )

# -- Boost library ---------------------------------------
# NOTE: Package Boost::units cannot be detected
find_package( Boost 1.33.0 REQUIRED COMPONENTS filesystem system )

if( Boost_FOUND )
	include_directories( SYSTEM ${Boost_INCLUDE_DIRS} )
	link_directories( ${Boost_LIBRARY_DIRS} )	
endif()

# -- OpenCascade -----------------------------------------
# TODO: Try to remove unnecessary libraries if there are any
find_package( OpenCascade REQUIRED COMPONENTS TKernel TKMath TKBool TKBO TKPrim TKTopAlgo TKV3d TKService TKBin TKBRep TKFillet TKOffset TKOpenGl TKGeomBase TKGeomAlgo TKG3d )
if( OpenCascade_FOUND )
	include_directories( SYSTEM ${OpenCascade_INCLUDE_DIR} )
	link_directories( ${OpenCascade_LIBRARY_DIR} )
endif( OpenCascade_FOUND )

# -- Qt5 -------------------------------------------------
# Qt5Widgets finds its own dependencies (Qt5::QtGui and Qt5::QtCore).
find_package(Qt5Widgets)

find_package(Qt5OpenGL)

if( Qt5Core_FOUND )
	# Qt5 version information
	message( STATUS "Found Qt5 version: ${Qt5Core_VERSION_STRING}" )
endif()

set( Qt5_LIBRARIES Qt5::Widgets Qt5::OpenGL )

# -- Ogre ------------------------------------------------
# - Try to find OGRE
# If you have multiple versions of Ogre installed, use the CMake or
# the environment variable OGRE_HOME to point to the path where the
# desired Ogre version can be found.
# By default this script will look for a dynamic Ogre build. If you
# need to link against static Ogre libraries, set the CMake variable
# OGRE_STATIC to TRUE.
#
# Once done, this will define
#
#  OGRE_FOUND - system has OGRE
#  OGRE_INCLUDE_DIRS - the OGRE include directories 
#  OGRE_LIBRARIES - link these to use the OGRE core
#  OGRE_BINARY_REL - location of the main Ogre binary (win32 non-static only, release)
#  OGRE_BINARY_DBG - location of the main Ogre binaries (win32 non-static only, debug)
#
# Additionally this script searches for the following optional
# parts of the Ogre package:
#  Plugin_CgProgramManager, Plugin_ParticleFX, 
#  RenderSystem_GL, RenderSystem_GL3Plus,
#  RenderSystem_GLES, RenderSystem_GLES2,
#  RenderSystem_Direct3D9, RenderSystem_Direct3D11
#  Paging, Terrain, Volume, Overlay
#
# For each of these components, the following variables are defined:
#
#  OGRE_${COMPONENT}_FOUND - ${COMPONENT} is available
#  OGRE_${COMPONENT}_INCLUDE_DIRS - additional include directories for ${COMPONENT}
#  OGRE_${COMPONENT}_LIBRARIES - link these to use ${COMPONENT} 
#  OGRE_${COMPONENT}_BINARY_REL - location of the component binary (win32 non-static only, release)
#  OGRE_${COMPONENT}_BINARY_DBG - location of the component binary (win32 non-static only, debug)
#
# Finally, the following variables are defined:
#
#  OGRE_PLUGIN_DIR_REL - The directory where the release versions of
#       the OGRE plugins are located
#  OGRE_PLUGIN_DIR_DBG - The directory where the debug versions of
#       the OGRE plugins are located
#  OGRE_MEDIA_DIR - The directory where the OGRE sample media is
#       located, if available

if( EXISTS "/usr/local/lib/OGRE/cmake" ) 
    set( CMAKE_MODULE_PATH "/usr/local/lib/OGRE/cmake/;${CMAKE_MODULE_PATH}" )
elseif( EXISTS "/usr/lib/OGRE/cmake" ) 
    set( CMAKE_MODULE_PATH "/usr/lib/OGRE/cmake/;${CMAKE_MODULE_PATH}" )
elseif( EXISTS "/usr/share/OGRE/cmake/modules" ) 
    set( CMAKE_MODULE_PATH "/usr/share/OGRE/cmake/modules/;${CMAKE_MODULE_PATH}" )
else()
    message( FATAL_ERROR "Ogre installation not found." )
endif()

find_package(OGRE REQUIRED )

# Core
add_subdirectory( Core/Source )

# Mechanicca application
add_subdirectory( Application/Source )

# Component plugins
add_subdirectory( Components/Drivetrain/Source )