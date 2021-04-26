# Based on parts from Credzba's common.py

#
import Items
import Player
import Gumps
import Target
import Misc
#

#
tinker_kitsID = 0x1EB8
metalID = 0x1BF2
#

# Finds all items matching an ID in item_types
def find_items(item_types, item_serial=Player.Backpack.Serial):
    found_items = []    
    cur_item = Items.FindBySerial(item_serial)
    
    # If the serial does not correspond to an item, no items can be found
    if not cur_item:
        return found_items

    # If I was looking for this item, add this item to the list of found items
    if cur_item.ItemID in item_types:
        found_items.append(cur_item)

    # If the item is not a container, no need to search within item for contained items
    if not cur_item.IsContainer:  
        return found_items

    # Otherwise, search inside of item for contained items
    
    # If current item is an empty container, it does not contain any items
    if len(cur_item.Contains) == 0:
        return found_items
    
    

    # Otherwise, look at all contained items and their potential contents with this same function for the same item types
    for item in cur_item.Contains:
        for contained_in_item in find_items(item_types, item.Serial):
            found_items.append(contained_in_item)
    return found_items
#

# Makes a tinkering kit
def make_tinker():
    kits_in_pack = find_items([tinker_kitsID])
    
    # If no tinker kits found in backpack, exit with message
    if len(kits_in_pack) == 0:
        Misc.SendMessage("Need tinker kit to craft a tinker kit.")
        sys.exit()
    #
    
    # Arbitrarily use the first kit found in pack
    use_kit = kits_in_pack[0]

    # Make sure user has enough metal to craft tinker kit
    if Items.BackpackCount(metalID, 0) < 2:
        Misc.SendMessage("Not enough iron to craft tinker kit.")
        sys.exit()
    #
    
    # Craft tinkering kit via tinkering GUMP
    Items.UseItem(use_kit)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 23)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 0)
    Gumps.WaitForGump(949095101, 2000) 
    Target.Cancel()
#

# Makes a shovel
def make_shovel():    
    kits_in_pack = find_items([tinker_kitsID])
    
    # If no tinker kits found in backpack, exit with message
    if len(kits_in_pack) == 0:
        Misc.SendMessage("Need tinker kit to craft shovel.")
        sys.exit()
    #
    
    # Arbitrarily use the first kit found in pack
    use_kit = kits_in_pack[0]
    
    # Make sure user has enough metal to craft shovel
    if Items.BackpackCount(metalID, 0) < 4:
        Misc.SendMessage("Not enough iron to craft shovel.")
        sys.exit()
    #

    # Craft shovel via tinkering GUMP
    Items.UseItem(use_kit)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 72)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 0)    
    Gumps.WaitForGump(949095101, 2000) 
    Target.Cancel()
#