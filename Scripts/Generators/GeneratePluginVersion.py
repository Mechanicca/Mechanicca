#!/usr/bin/python

import sys, getopt, sqlite3

class PluginVersionGenerator:

	# Constructor
	def __init__( self, argv ):
		# Parse input arguments
		self.ParseArguments( argv )		

		self.HeaderFileHeader = \
'''/*
 * <CompName>_Version.h
 *
 *  [GENERATED FILE - Do not edit manually]

 *  Author: Martin Kopecky <martin.monster696@gmail.com>
 */

#ifndef GENERATED_<COMPNAME_UPPERCASE>_VERSION_H_
#define GENERATED_<COMPNAME_UPPERCASE>_VERSION_H_

#define VERSION_MAJOR			<MAJOR_VERSION>
#define VERSION_MINOR			<MINOR_VERSION>
#define VERSION_PATCH			<PATCH_VERSION>

#define VERSION_STRING			"<MAJOR_VERSION>.<MINOR_VERSION>"
#define VERSION_COMPLETE_STRING	"<MAJOR_VERSION>.<MINOR_VERSION>.<PATCH_VERSION>"

#endif
'''
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<CompName>", str( self.Component ) );
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<COMPNAME_UPPERCASE>", str( self.Component.upper() ) );

		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<MAJOR_VERSION>", str( self.Version[0] ) );
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<MINOR_VERSION>", str( self.Version[1] ) );
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<PATCH_VERSION>", str( self.Version[2] ) );

		# Create / open generated header file
		self.GeneratedHeaderFile = open( self.OutputFileName, "w" );

		self.GeneratedHeaderFile.write( self.HeaderFileHeader );

	# Destructor
	def __del__( self ):
		# Close generated file
		self.GeneratedHeaderFile.close()

	# Process all script input parameters
	def ParseArguments( self, argv ):
		# Declare filenames
		self.Version = ''

		try:
			# Parse script input argument
			opts, args = getopt.getopt(argv,"hv:o:c:",["version=", "output=", "component="])
		except getopt.GetoptError:
			# Display help when unsupported argument is set up...
			print '-v <VersionString> -o <OutputHeaderFile> -c <Component>'
			# ...and exit the script
			sys.exit(2)
		# Iterate through the options
		for opt, arg in opts:
			# Help...
			if opt == '-h':
				print '-v <VersionString> -o <OutputHeaderFile> -c <Component>'
				sys.exit()
			# Version settings
			elif opt in ("-v", "--version"):
				self.Version = arg.split( "." );
			# Output file settings
			elif opt in ("-o", "--output"):
				self.OutputFileName = arg
			# Component settings
			elif opt in ("-c", "--component"):
				self.Component = arg

# Script main()
def main( argv ):
	# Instantiate generator
	Generator = PluginVersionGenerator( argv )

# Script entry point	
if __name__ == "__main__":
	main( sys.argv[1:] )
