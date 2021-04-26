This script is intended for use on UO Eventine.

Not intended to be used for AFK mining: AFK resource collection is NOT ALLOWED on UO Eventine.



The script's interface is somewhat self-explanatory, but this README explains the details.

I bolded the parts I thought most important to explain.

* Summary:
	* Mines ore vein(s) to completion.
	* Add the mining script and tools.py to your Scripts folder in your RE (Razor Enhanced) directory and add the mining script in RE under the scripting section to use.
		
	* __The script is not perfect and has some edge case issues; the stop button can sometimes stop it from working, necessitating restarting the script. See the Known Bugs section for more information.__
	* __I am happy to improve this script to the best of my ability. Please PM me (Geronimo Smeebl) if you have any problems or suggestions.__

* BUTTONS:
	* Choose Tool Manually:
		* This allows the user to mine with a specific tool of their choosing. This feature is disabled by default.
		* Clicking the button and target your preferred pickaxe to use this feature.

		* The default tool mode searches through the player's backpack and selects a tool arbitrarily (excluding gargish pickaxes as explained within its respective button description).
		* The default tool mode will also try to create a shovel if the user does not have any tools in their backpack.

	* Clear Manual Tool:
		* If a user has selected a manual tool, this button clears that selection, so the script will revert to the default tool mode.

	* __Set Ore Bag__:
		* The user must choose a bag for their ore.
		* This button allows the user to choose the bag in which they wish to store their ore.

		* This button must be used every time the script is run with the exception of the BAG ALTERNATIVE described below.

	* Toggle Using Gargish Pickaxe:
		* This allows the user to decide whether or not they want to mine with (a) gargish pickaxe(s). This feature is disabled by default.

		* If this feature is enabled, only gargish pickaxes will be selected to use for mining.

		* If this feature is disabled, gargish pickaxes will not be selected for mining.

		* If a tool is chosen manually, this feature is ignored.

	* __Toggle Rail Mining__:
		* This allows the user to decide whether they want to mine along a rail. This feature is disabled by default.
		* The default mode simply mines to completion any ore veins within range of the player's current location.

		* Rail Mining is described below.


* __RAIL MINING__:
	* A rail is just an ordered set of locations.
	* Rail Mining entails attempting to mine at each of the locations in the rail in order.

	* A rail can be created using Mourn's RailRecorder.py script found [here](http://razorenhanced.net/download/scripts/mourn/RailRecorder.py).

	* __For use in this script, the user must have their rail file in a folder named "Rails" in their Data folder in their Razor Enhanced directory.__
	* __Note that the "Rails" folder does not exist by default, so it must be created manually by the user.__
	* __Alse note that the rail recorder stores the rail file in the user's Documents folder, so the rail file must be moved after creation to be used with this script.__

	* __To mine a specific rail, just make sure the corresponding file is in the Data folder and put the rail's name in the script's textbox where it says Rail_Name.__
	* A rail's name corresponds to the name chosen when creating the rail with Mourn's RailRecorder.

	* __The Pathfinding is not perfect and if the character gets stuck the mining work will stop.__
	* My recommendation is manually moving your character until they are no longer stuck.
	* This should not be a problem since AFK resource gathering is not allowed on Eventine anyway.


* __BAG ALTERNATIVE__:
	* Instead of using the Set Ore Bag button every time the script is run, the user can manually put their bag's Serial in the script's code at the top.

	* Directions:
		1. Select this script in the scripting section in RE and click Edit.

		1. Click the Inspect Entities button at the top of the Enhanced Script Editor.

		1. Select the bag you want to use for mining.

		1. In the Enhanced Item Inspector copy The Serial number of the bag (of the form 0xXXXXXXXX)

		1. Paste that number on line 6 of the script to replace the serial number currently their.

	* This will cause the script to set the ore bag to that selected bag every time it is run.
	* This means you don't need to use the Set Ore Bag button and target that bag every time.
	* Using the set ore bag button will override this manually selected bag.


* Credit:
	* I based this mining script on the following:
		* Credzba's [mining.py](http://razorenhanced.net/download/scripts/credzba/mining.py)
		* Credzba's [common.py](http://razorenhanced.net/download/scripts/credzba/common.py)
		* Fate's Whim's [automine.py](http://razorenhanced.net/download/scripts/fateswhim/automine.py)
		* Mourn's [RailRecorder.py](http://razorenhanced.net/download/scripts/mourn/RailRecorder.py)

		* The links are for the actual scripts. The links to those scripts and others are aggregated on the following pages:
			* http://razorenhanced.net/dokuwiki/doku.php?id=toolscripts
			* http://razorenhanced.net/dokuwiki/doku.php?id=resourcegatheringscripts

* __Known Bugs__
	* Most bugs I've experienced are a result of malfunctions with rail mining.
	* If the STOP button is pressed and there is no message stating "Finished with mining work." then the script may not continue to function as intended which will necessitate stopping the script using the RE stop button or with the close button on the interface, then starting the script again.
	* To my knowledge, if the script is stopped while Pathfinding is ongoing, the Pathfinding will continue past the termination of the script until the Pathfinding destination is reached. I'm not sure I can do anything about this.
	* The bug above means that your computer resources might still be in use for pathfinding after closing the script. I would recommend not pressing start until your character is somewhat near the first location in your rail and having adjacent rail locations somewhat near one another to minimize issues with Pathfinding.
	* __If UO ends up hogging your computer CPU even after closing the script, it is likely due to the Pathfinding bug described above; you may need to restart your UO client. I have only experienced this when trying to Rail Mine on a rail that was on a different Facet than my character when I clicked START.__
	* __Other than Pathfinding as described above, I have not experienced any bugs having effects lasting beyond the termination of the script in which they arose (i.e. to my knowledge, bugs that come up only have an effect while the script is running; they do not have an effect after the script is closed)__.
	* In the case of any bugs or malfunctions, closing the script should stop most problems. In the worst case you may need to restart your UO client.
