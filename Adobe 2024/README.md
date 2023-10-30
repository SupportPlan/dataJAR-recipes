# Import Adobe 2024 Title

## About
These recipes are based on: https://github.com/autopkg/adobe-ccp-recipes

But with the death of Creative Cloud Packager (https://macmule.com/2018/10/15/adobe-creative-cloud-2019-the-death-of-creative-cloud-packager-device-licensing/), have been rejigged to work with locally downloaded pkgs.

***Please Note:*** Imports have now been tested with all titles Adobe have released for 2024

***Please Note:*** Munki support has been added for Adobe's new Intel-only and Apple Silicon-only packages, please see section *[Adobe and Apple Silicon](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/README.md#adobe-and-apple-silicon)* below

## Pre-reqs

1) Build the wanted Adobe 2024 titles from the Adobe Admin Console.

*Please Note:* These should be of the **Managed Package** variety, as a Self Service package does not create the required `_Uninstall.pkg` which is needed by the [Adobe2024Versioner.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Versioner.py) processor. See [this issue](https://github.com/autopkg/dataJAR-recipes/issues/39) for more info.

2) For each Adobe package title, use the naming convention of:

Adobe*AppName*2024

For example:

- AdobeAcrobatDC2024   
- AdobeAfterEffects2024   
- AdobeAnimate2024    
- AdobeAudition2024   
- AdobeBridge2024   
- AdobeCharacterAnimator2024  
- AdobeDimension2024    
- AdobeDreamweaver2024  
- AdobeIllustrator2024    
- AdobeInCopy2024   
- AdobeInDesign2024  
- AdobeLightroom2024  
- AdobeLightroomClassic2024   
- AdobeMediaEncoder2024   
- AdobePhotoshop2024    
- AdobePrelude2024   
- AdobePremierePro2024   
- AdobePremiereRush2024   
- AdobeXD2024

With the latest commit, we can also accept a naming convention that starts with Adobe and has 2024 somewhere in the name. For example:

- AdobeAcrobatDC2024
- AdobeAcrobatDC2024-Intel
- AdobeAcrobatDC2024-ARM

3) Mount the Adobe downloader DMG and run the download application. Once downloaded, unzip the file if your browser does not auto unzip the download. This must be in your `~/Downloads` folder.

*Please Note:* Keep the name of the unzipped directory the same as the the installer/uninstaller package within.

Also, these packages should only contain a maximum of the Creative Cloud Desktop App (CCDA) and only **one** other App (e.g. CCDA and Photoshop). Most of the Adobe-supplied Templates for packages aren't compatible with this.

4) Create the respective munki or jss recipe overrides. The override name **must** be the same as the Adobe 2024 pkg. 

For example:

`AdobeAcrobatDC2024.jss.recipe`
`AdobeAcrobatDC2024.munki.recipe`

*Please Note:* The [Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py) script assumes your autopkg overrides live in `~/Library/AutoPkg/RecipeOverrides`.

5) The `NAME` input variable must also match the Adobe package title. For Munki admins, the "MUNKI_NAME" input can be used to specify a different Munki Name for the import.

## Usage

With the pre-reqs met, you can run the [Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py) script found in this repo.

You will need to pass to [Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py) the recipe type, which would be either jss or munki.

For example:

`/path/to/Adobe2024Importer.py jss` or `/path/to/Adobe2024Importer.py munki`

## Process
[Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py) will:

1. Check the running users ~/Downloads folder for folders matching the pattern: Adobe&ast;2024&ast;, exiting if nothing found.
2. Create an empty recipe list at ~/Downloads/adobe2024_list.txt
3. Check that the Adobe&ast;2024&ast; folder/s contain a sub directory called Build containing a pkg called \*\_Install.pkg, skipping this pkg if not found.
4. If step 3 passes for a pkg, next we look for an override named Adobe&ast;2024&ast;.jss.recipe or Adobe&ast;2024&ast;.munki.recipe in ~/Library/AutoPkg/RecipeOverrides (depending on what option was passed to [Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py), skipping this pkg if not found.
5. If step 4 is successful, the Override added to the ~/Downloads/adobecc2024_list.txt recipe list. Steps 3-5 are repeated for all Adobe&ast;2024&ast; folders found within ~/Downloads.
6. If any items are added to the ~/Downloads/adobe2024_list.txt recipe list, this is then ran with a report written to ~/Downloads/adobe2024_report.plist

## Adobe and Apple Silicon

Adobe have started to release titles that support Apple Silicon devices. In order to facility this, they have the administrator specify the type of *package* that is created from the Admin console. 

**Note:** Although you can specify an Apple Silicon / arm64 package, the content for the majority of Apps are still Intel-only and will require Rosetta 2 to be installed on devices even for this packages to install.

The Munki support is achieved through the use of the built in support for the `supported_architectures` pkginfo key ([More Info](https://github.com/munki/munki/wiki/Supported-Pkginfo-Keys)). In order for this to work correctly on Apple Silicon devices, you must make sure to be running Munki v5.2.1 or newer. You will need to create two packages per Adobe 2024 title, one with the Intel option selected, and one with Apple Silicon/arm64 selected. These both need to be imported into your Munki repo with the same Munki name, and with the appropriate `supported_architectures` value/s set.

In order to support this, we've had to make some changes to the Munki parent recipe, the [Adobe2024Versioner.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Versioner.py) processor and the [Adobe2024Importer.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Importer.py) script. The core changes have been detailed below:

- Package names are now more flexible, and will search for packages starting with "Adobe" and contains "2024". This allows you to create packages with the architecture type at the end.
- As the NAME input is used by versioner to find the packages, this must always match the name of the packages you create
	- To specify a NAME for Munki, add the "MUNKI_NAME" option to the recipe Input, and use this in the pkginfo Input (see committed changes to the parent Munki recipe).  
	- If offering both an Intel and arm64 package for the same install, ensure that the supported_architectures key is set correctly (see below) and use the same MUNKI_NAME for the two recipes.    
- In order to import the "same" App version packages for the Intel and ARM installs, We have needed to add the `force_munkiimport` `true` key to the main Input.
	- This may result in duplicate imports if the admin's download folder is not cleared up after each run, or the name isn't changed away from starting with Adobe (e.g. change from "AdobeMediaEncoder2024-ARM" to "OFF-AdobeMediaEncoder2024-ARM
- [Adobe2024Versioner.py](https://github.com/autopkg/dataJAR-recipes/blob/master/Adobe%202024/Adobe2024Versioner.py) will now look for the "ProcessorArchitecture" key within each Adobe install package. 
	- If this has a value of "x64" it's for Intel Macs. It will set the pkginfo key `supported_architectures` to an array of `x86_64` (e.g. Intel Macs only). It will also rename the install and uninstall disk image to include the word "Intel" 
	- If this has a value of "arm64" it's for Apple Silicon Macs. It will set the pkginfo key `supported_architectures` to an array of `arm64` (e.g. Apple Silicon Macs only). It will also rename the install and uninstall disk image to include the word "ARM"
	- **Note:** Apple Silicon devices must be running Munki v5.2.1 or newer for the architecture type to be detected properly
	- **Note:** Although Adobe supply arm64 installers for for all of their 2024 suite, most of these packages will still deploy an Intel version of the software and so will need Rosetta 2 installed. It seems the installers will also fail without Rosetta 2, even with the "arm64" packages.

If you find any problems, please log an Issue on this repo.
