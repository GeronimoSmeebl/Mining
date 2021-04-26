# Modified version of Credzba's common.py found at http://razorenhanced.net/dokuwiki/doku.php?id=toolscripts
# Made for use in Eventine

# All I changed were:
# - a few GUMP SendAction calls that would craft a different item than intended when I tried to use the original
# - corrected some of the Misc SendMessage text

import time
import sys
import math
#
import Mobiles
import Items
import Player
import Gumps
import Target
import Misc
#
import re 
#
from System.Collections.Generic import List
from System import Byte, Int32
#
def FindPets():
    pets = []
    pet_filter = Mobiles.Filter()
    pet_filter.Enabled = True
    pet_filter.RangeMin = -1
    pet_filter.RangeMax = 10
    pet_filter.Notorieties = List[Byte](bytes([1, 2]))
    potentialPets = Mobiles.ApplyFilter(pet_filter)
    for potentialPet in potentialPets:    
        #
        props = Mobiles.GetPropStringList(potentialPet)
        for p in props:
            prop = str(p)
            #Misc.SendMessage(prop)
            ownerMatch = re.search("Owner: ({}).*".format(Player.Name), prop)
            if ownerMatch:                
                pets.append(potentialPet)
            #bonded = re.search("bonded", prop)
            #if bonded:                
                #pets.append(potentialPet)
                
    return pets 
#
def DoForEachItemIn(bag, fn):
    ret_list = []
    if isinstance(bag, int):    
        container = Items.FindBySerial(bag)
    else:
        container = bag
    # if not found
    if container == None:
        return ret_list
    # if the itemId is in array (container or not) return it and don't look further    
    if fn(container):
        ret_list.append(container)
    # if not container return empty list
    if not container.IsContainer:    
        return ret_list
    #  These things appear as containers but are not    
    if container.ItemID == 0x1EA7 and container.Hue == 0x0032:
        # gem of nautical exploration is a container !?!
        return ret_list
    if "sending" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    if "spellbook" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    Items.UseItem(container)
    Items.WaitForContents(container, 2000)
    for item in container.Contains:
        for tmp in DoForEachItemIn(item.Serial, fn):
            ret_list.append(tmp)
    return ret_list
#            
PropValue1 = [
              "regen stamina",
              ]
PropValue2 = [
              "spell damage",
              "regen hits",
              ]
PropValue3 = [
              "defense chance increase",
              "hit chance increase", 
              #"damage increase",
              #"swing speed increase",
              "reflect physical damage",
              "bonus hits",              
              "bonus stamina",
              "bonus mana",
              #"hit life leech",
              #"hit stamina leech",
              #"hit mana leech",
              "hit lower attack"
              "hit lower defense"
              # These are 4 points but not worth 4 to me
              "hit cold area",
              "hit fire area",
              "hit poison area",
              "hit energy area",
              "hit physical area",                                         
              ]
PropValue4 = [
              "bonus strength",
              "bonus dex",
              "bonus int",
              "hit fireball",
              "hit lightning",
              "hit curse",
              "hit fatigue",
              "hit mana drain",
              ]
              
PropValue5 = [
              "faster cast recovery",
              "lower mana cost", 
              "lower reagent cost",
              "physical resist",
              "fire resist",
              "cold resist",
              "poison resist",
              "energy resist",
              "fire eater",
              "cold eater",
              "poison eater",
              "energy eater",
              "kinetic eater",
              "casting focus",
              ] 
PropValue6 = [
              "regen mana",
              ] 

PropValue25 = [
              "damage eater",
              ]               
              
PropValue50 = [
              "faster casting",
              ]               

def ComputeLevelValue(item):
    if item.IsContainer:
        return False
    levelValue = 0
    props = [x.lower() for x in Items.GetPropStringList(item)]    
    for prop in props:
        value = 0
        #
        for check in PropValue1:
            if check in prop:
                value = float(Items.GetPropValue(item, prop))
        #
        for check in PropValue2:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 2
        #
        for check in PropValue3:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 3
        #
        for check in PropValue4:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 4
        #
        for check in PropValue5:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 5
        #
        for check in PropValue6:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 6                                                                
        #
        for check in PropValue25:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 25
        #        
        for check in PropValue50:
            if check in prop:
                value = float(Items.GetPropValue(item, prop)) * 50
        levelValue += value                                         
    #             
    return levelValue
            
#    
def findRecursive(containerSerial, typeArray, openContainers=False):
    ret_list = []    
    container = Items.FindBySerial(containerSerial)
    # if not found
    if container == None:
        return ret_list
    # if the itemId is in array (container or not) return it and don't look further    
    if container.ItemID in typeArray:
        ret_list.append(container)
        return ret_list
    # if not container return empty list
    if not container.IsContainer:    
        return ret_list
    #  These things appear as containers but are not    
    if container.ItemID == 0x1EA7 and container.Hue == 0x0032:
        # gem of nautical exploration is a container !?!
        return ret_list
    if "sending" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    if "spellbook" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    # If a container has not been openned it will appear empty, but opening them all makes the UI ugly   
    if openContainers:        
        Items.UseItem(container)
        Items.WaitForContents(container, 2000)
    for item in container.Contains:
        for tmp in findRecursive(item.Serial, typeArray, openContainers):
            ret_list.append(tmp)
    return ret_list
    
#    
def findRecursiveWithColor(containerSerial, typeArray,  openContainers=False):
    ret_list = []
    types = []
    typeColor = []
    for id in typeArray:
        types.append(id[0])
        typeColor.append(id[1])
    #    
    container = Items.FindBySerial(containerSerial)
    # if not found
    if container == None:
        return ret_list
    # if the itemId is in array (container or not) return it and don't look further 
    try:
        index = types.index(container.ItemID)
        #Misc.SendMessage("2 container: {:x} id: {:x} color: {:x}".format(container.Serial, container.ItemID, container.Hue))
        #Misc.SendMessage("Index: {}".format(index))
        if container.Hue == typeColor[index] or typeColor[index] == -1:
            ret_list.append(container)
    except ValueError:
        pass     
    # if not container return empty list
    if not container.IsContainer:    
        return ret_list
    #  These things appear as containers but are not    
    if container.ItemID == 0x1EA7 and container.Hue == 0x0032:
        # gem of nautical exploration is a container !?!
        return ret_list
    if "sending" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    if "spellbook" in Items.GetPropStringByIndex(container, 0).lower():
        return ret_list
    # If a container has not been openned it will appear empty, but opening them all makes the UI ugly   
    if openContainers:        
        Items.UseItem(container)
        Items.WaitForContents(container, 2000)
    for item in container.Contains:
        #Misc.SendMessage("1 container: {:x} id: {:x} color: {:x}".format(container.Serial, item.ItemID, item.Hue))
        for tmp in findRecursiveWithColor(item.Serial, typeArray, openContainers):
            ret_list.append(tmp)
    return ret_list
#    
def find(containerSerial, typeArray):
    ret_list = []
    container = Items.FindBySerial(containerSerial)
    if container != None:
        for item in container.Contains:
            if item.ItemID in typeArray:
                ret_list.append(item)
    return ret_list  
#
def DexHealingFormula():
    if Player.Dex > 80:
        healTime = 8 - ((Player.Dex - 80) / 20)
        if healTime < 0.5:
            return 0.5
        else:
            return healTime
    else:
        return 8   
#  
NextHealTime = time.time()
def HealMe(wait=True):
    global NextHealTime
    if True == BandageHeal.Status():            
        return        
    healDelay = NextHealTime - time.time()    
    if healDelay > 0:
        if wait:
            Misc.Pause(healDelay*1000)
        else:
            return
    if Misc.CheckSharedValue("BandSelf"):
        Player.ChatSay(0, Misc.ReadSharedValue("BandSelf"))   
    else:    
        Items.UseItemByID(0x0E21, 0x0480)
        Target.WaitForTarget(200, False)
        Target.Self() 
    delay = DexHealingFormula()
    NextHealTime = time.time() + delay 
    #Misc.SendMessage("Next heal time {} now {}".format(NextHealTime, time.time()))
#
tinker_kitsID = 0x1EB8
fletching_kitsID =  0x1022  
woodID = 0x1BD7
woodStorage = 0x44046D13
shaftID = 0x1BD4
metalID = 0x1BF2
hatchetID = 0x0F43
#
def MakeTinkerKits():
    kit = Items.FindByID(tinker_kitsID, 0, Player.Backpack.Serial)
    if kit == None:
        Misc.SendMessage("CANNOT MAKE TINKER KITS WITHOUT AT LEAST 1 IN PACK")
        sys.exit(0)
    #
    if Items.BackpackCount(metalID, 0) < 2:
        Misc.SendMessage("Need iron ingots in your pack to make tinker kit")
        sys.exit(0)
    #
    Items.UseItem(kit)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 23)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 0)
    Gumps.WaitForGump(949095101, 2000) 
    Target.Cancel()
#
def MakeFletchingKits():
    kit = Items.FindByID(tinker_kitsID, 0, Player.Backpack.Serial)
    if kit == None:
        MakeTinkerKits()
        kit = Items.FindByID(tinker_kitsID, 0, Player.Backpack.Serial)
        if kit == None:
            Misc.SendMessage("Insufficient TINKER KITS TO MAKE FLETCHING KIT")
            sys.exit(0)
    #      
    if Items.BackpackCount(metalID, 0) < 3:
        Misc.SendMessage("Need iron ingots in your pack to make fletching kit")
        sys.exit(0)
    #
    Items.UseItem(kit)
    Gumps.WaitForGump(949095101, 5000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 5000)
    Gumps.SendAction(949095101, 142)
    Gumps.WaitForGump(949095101, 5000)
    Gumps.SendAction(949095101, 0)
#    
def MakeHatchet():    
    kit = Items.FindByID(tinker_kitsID, 0, Player.Backpack.Serial)
    if kit == None:
        Misc.SendMessage("Insufficient TINKER KITS TO MAKE HATCHET")
        sys.exit(0)
    #      
    if Items.BackpackCount(metalID, 0) < 4:
        Misc.SendMessage("Need iron ingots in your pack to make hatchet")
        sys.exit(0)
    #
    Items.UseItem(kit)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 30)
    Gumps.WaitForGump(949095101, 10000)
    Gumps.SendAction(949095101, 0)    
#
def MakeShovel():    
    kit = Items.FindByID(tinker_kitsID, 0, Player.Backpack.Serial)
    if kit == None:
        Misc.SendMessage("Insufficient TINKER KITS TO MAKE SHOVEL")
        sys.exit(0)
    #      
    if Items.BackpackCount(metalID, 0) < 4:
        Misc.SendMessage("Need iron ingots in your pack to make shovel")
        sys.exit(0)
    #
    Items.UseItem(kit)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 15)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 72)
    Gumps.WaitForGump(949095101, 2000)
    Gumps.SendAction(949095101, 0)    
#
def convertFromEUO(strID):
    #test = "YPO_BNF_CPH_INF_FSF_OSF_ASF_HNF_FMH_CNF_LSF_NSF_ISF_SMH_RMH_CSF_ZRF_MPH_LPH_MSF_BSF_KPO_GUO_KTF_JTF_BPH_EPH_ZSF_ATF_JPH_SOH_POH_NMH_OMH_LPO_ZTO_XTH_YTH_HSF_KSF_NPO_XPO_FUO_JPO_QPF_NPF_KPH_FYG_RHM_SFR"
    test = strID.upper()
    test_array = test.split('_')
    result = ""
    for item in test_array:
        i = 1
        decid = 0        
        for c in item:
            decid = decid + ( ord(c) - ord('A')) * i
            i = i * 26
        decid = (decid - 7) ^ 69
        result = result + "0x{:x}, ".format(decid)
    return result       

ArmorIgnore = "Armor Ignore"
ArmorPierce = "Armor Pierce"
Bladeweave = "Bladeweave"
BleedAttack = "Bleed Attack"
Block = "Block"
ConcussionBlow = "Concussion Blow"
CrushingBlow = "Crushing Blow"
DefenseMastery = "Defense Mastery"
Disarm = "Disarm"
Dismount = "Dismount"
DoubleShot = "Double Shot"
DoubleStrike = "Double Strike"
DualWield = "Dual Wield"
FrenziedWhirlwind = "Frenzied Whirlwind"
Feint = "Feint"
ForceArrow = "Force Arrow"
InfectiousStrike = "Infectious Strike"
InfusedThrow = "Infused Throw"
LightningArrow = "Lightning Arrow"
MortalStrike = "Mortal Strike"
MovingShot = "Moving Shot"
MysticArc = "Mystic Arc"
NerveStrike = "Nerve Strike"
ParalyzingBlow = "Paralyzing Blow"
PsychicAttack = "Psychic Attack"
RidingSwipe = "Riding Swipe"
SerpentArrow = "Serpent Arrow"
ShadowStrike = "Shadow Strike"
TalonStrike = "Talon Strike"
WhirlwindAttack = "Whirlwind Attack"

weapon_ability_priority = {"Double Strike" : 1,
                           "Double Shot" : 2,
                           "Armor Pierce" : 3,
                           ArmorIgnore : 3,
                           "Crushing Blow" : 4,
                           "Concussion Blow" : 5,
                           "Infectious Strike" : 6,
                           "Mortal Strike" : 7,
                           "Bleed Attack" : 8,
                           "Bladeweave" : 9,
                           "Paralyzing Blow" : 10,
                           "Lightning Arrow" : 11,
                           "Whirlwind Attack" : 999
                           }
                           
requires_mount = {"Double Shot" : True }

weapon_special = {}
weapon_special[0xA289] = [ConcussionBlow, WhirlwindAttack]
weapon_special[0xA28A] = [ArmorPierce, WhirlwindAttack]
weapon_special[0xA28B] = [BleedAttack, WhirlwindAttack]

weapon_special[0x26CE] = [WhirlwindAttack, Disarm ]
weapon_special[0x27AE] =[ Block, None ] 
weapon_special[0x27F9] = [ Block, None ] 
weapon_special[0x422a] = [ None, None ]
weapon_special[0x1b03] = [ None, None ]
weapon_special[0x1b03] = [ None, None ]

weapon_special[0x2D22] = [Feint, ArmorIgnore]
weapon_special[0x2D2E] = [Feint, ArmorIgnore]
weapon_special[0x48BA] = [DoubleStrike, ArmorIgnore]
weapon_special[0x48BB] = [DoubleStrike, ArmorIgnore]

weapon_special[0x13FE] = [DoubleStrike, ArmorIgnore]
weapon_special[0x13FF] = [DoubleStrike, ArmorIgnore]

weapon_special[0xF5E] = [CrushingBlow, ArmorIgnore]
weapon_special[0xF5F] = [CrushingBlow, ArmorIgnore]

weapon_special[0x13FA] = [WhirlwindAttack, ArmorIgnore ]
weapon_special[0x13FB] = [WhirlwindAttack, ArmorIgnore ]

weapon_special[0x2D23] = [Disarm, Bladeweave]
weapon_special[0x2D2F] = [Disarm, Bladeweave]

weapon_special[0x2D26] = [Disarm, Bladeweave]
weapon_special[0x2D32] = [Disarm, Bladeweave]

weapon_special[0x2D27] = [WhirlwindAttack, Bladeweave]
weapon_special[0x2D33] = [WhirlwindAttack, Bladeweave]
0x2D33

weapon_special[0x2D29] = [DefenseMastery, Bladeweave]
weapon_special[0x2D35] = [DefenseMastery, Bladeweave]

weapon_special[0x4067] = [MysticArc, BleedAttack]
weapon_special[0x08FF] = [MysticArc, BleedAttack]

weapon_special[0x2D20] = [PsychicAttack, BleedAttack]
weapon_special[0x2D2C] = [PsychicAttack, BleedAttack]

weapon_special[0x13AF] = [ArmorIgnore, BleedAttack]
weapon_special[0x13B0] = [ArmorIgnore, BleedAttack]

weapon_special[0x1406] = [ConcussionBlow, BleedAttack]
weapon_special[0x1407] = [ConcussionBlow, BleedAttack]

weapon_special[0x48CA] = [Disarm, ConcussionBlow]
weapon_special[0x48CB] = [Disarm, ConcussionBlow]

weapon_special[0x48C2] = [DoubleStrike, ConcussionBlow]
weapon_special[0x48C3] = [DoubleStrike, ConcussionBlow]

weapon_special[0x090B] = [CrushingBlow, ConcussionBlow]
weapon_special[0x4074] = [CrushingBlow, ConcussionBlow]

weapon_special[0x48B0] = [BleedAttack, ConcussionBlow]
weapon_special[0x48B1] = [BleedAttack, ConcussionBlow]

weapon_special[0x26C0] = [Dismount, ConcussionBlow]
weapon_special[0x26CA] = [Dismount, ConcussionBlow]

weapon_special[0xE89] = [DoubleStrike, ConcussionBlow]
weapon_special[0xE8A] = [DoubleStrike, ConcussionBlow]

weapon_special[0x143A] = [CrushingBlow, ConcussionBlow]
weapon_special[0x143B] = [CrushingBlow, ConcussionBlow]

weapon_special[0x143E] = [WhirlwindAttack, ConcussionBlow]
weapon_special[0x143F] = [WhirlwindAttack, ConcussionBlow]

weapon_special[0xF60] = [ArmorIgnore, ConcussionBlow]
weapon_special[0xF61] = [ArmorIgnore, ConcussionBlow]

weapon_special[0x48C0] = [WhirlwindAttack, CrushingBlow]
weapon_special[0x48C1] = [WhirlwindAttack, CrushingBlow]

weapon_special[0x2D24] = [ConcussionBlow, CrushingBlow]
weapon_special[0x2D30] = [ConcussionBlow, CrushingBlow]

weapon_special[0x2D28] = [Disarm, CrushingBlow]
weapon_special[0x2D34] = [Disarm, CrushingBlow]

weapon_special[0x1438] = [WhirlwindAttack, CrushingBlow]
weapon_special[0x1439] = [WhirlwindAttack, CrushingBlow]

weapon_special[0x27AD] = [WhirlwindAttack, DefenseMastery]
weapon_special[0x27F8] = [WhirlwindAttack, DefenseMastery]

weapon_special[0x48BE] = [BleedAttack, Disarm]
weapon_special[0x48BF] = [BleedAttack, Disarm]

weapon_special[0x0904] = [DoubleStrike, Disarm]
weapon_special[0x406D] = [DoubleStrike, Disarm]

weapon_special[0x0903] = [ArmorIgnore, Disarm]
weapon_special[0x406E] = [ArmorIgnore, Disarm]

weapon_special[0x48B6] = [InfectiousStrike, Disarm]
weapon_special[0x48B7] = [InfectiousStrike, Disarm]

weapon_special[0x1404] = [BleedAttack, Disarm]
weapon_special[0x1405] = [BleedAttack, Disarm]

weapon_special[0xE81] = [CrushingBlow, Disarm]
weapon_special[0xE82] = [CrushingBlow, Disarm]

weapon_special[0xDF2] = [Dismount, Disarm]
weapon_special[0xDF3] = [Dismount, Disarm]

weapon_special[0xDF4] = [Dismount, Disarm]
weapon_special[0xDF5] = [Dismount, Disarm]

weapon_special[0xF43] = [ArmorIgnore, Disarm]
weapon_special[0xF44] = [ArmorIgnore, Disarm]

weapon_special[0xEC4] = [ShadowStrike, Disarm]
weapon_special[0xEC5] = [ShadowStrike, Disarm]

weapon_special[0xE85] = [DoubleStrike, Disarm]
weapon_special[0xE86] = [DoubleStrike, Disarm]

weapon_special[0x13F6] = [InfectiousStrike, Disarm]
weapon_special[0x13F7] = [InfectiousStrike, Disarm]

weapon_special[0x0906] = [CrushingBlow, Dismount]
weapon_special[0x406F] = [CrushingBlow, Dismount]

weapon_special[0x0908] = [WhirlwindAttack, Dismount]
weapon_special[0x4075] = [WhirlwindAttack, Dismount]

weapon_special[0x48B4] = [ParalyzingBlow, Dismount]
weapon_special[0x48B5] = [ParalyzingBlow, Dismount]

weapon_special[0x48B2] = [CrushingBlow, Dismount]
weapon_special[0x48B3] = [CrushingBlow, Dismount]

weapon_special[0x13FC] = [MovingShot, Dismount]
weapon_special[0x13FD] = [MovingShot, Dismount]

weapon_special[0xE87] = [BleedAttack, Dismount]
weapon_special[0xE88] = [BleedAttack, Dismount]

weapon_special[0x13B3] = [ShadowStrike, Dismount]
weapon_special[0x13B4] = [ShadowStrike, Dismount]

weapon_special[0x26BD] = [ArmorIgnore, Dismount]
weapon_special[0x26C7] = [ArmorIgnore, Dismount]

weapon_special[0xF4D] = [ParalyzingBlow, Dismount]
weapon_special[0xF4E] = [ParalyzingBlow, Dismount]

weapon_special[0x48CC] = [Feint]
weapon_special[0x48CD] = [Feint]

weapon_special[0x27A4] = [FrenziedWhirlwind, DoubleStrike]
weapon_special[0x27EF] = [FrenziedWhirlwind, DoubleStrike]

weapon_special[0x48D0] = [Feint, DoubleStrike]
weapon_special[0x48D1] = [Feint, DoubleStrike]

weapon_special[0x27A9] = [Feint, DoubleStrike]
weapon_special[0x27F4] = [Feint, DoubleStrike]

weapon_special[0x27A5] = [ ArmorPierce, DoubleShot]
weapon_special[0x27F0] = [ ArmorPierce, DoubleShot]

weapon_special[0x27A7] = [DefenseMastery, FrenziedWhirlwind]
weapon_special[0x27F2] = [DefenseMastery, FrenziedWhirlwind]

weapon_special[0x48C8] = [ParalyzingBlow, InfectiousStrike]
weapon_special[0x48C9] = [ParalyzingBlow, InfectiousStrike]

weapon_special[0x48BC] = [ ArmorIgnore, InfectiousStrike]
weapon_special[0x48BD] = [ ArmorIgnore, InfectiousStrike]

weapon_special[0x0902] = [ShadowStrike, InfectiousStrike]
weapon_special[0x406A] = [ShadowStrike, InfectiousStrike]

weapon_special[0x48AE] = [BleedAttack, InfectiousStrike]
weapon_special[0x48AF] = [BleedAttack, InfectiousStrike]

weapon_special[0x08FD] = [DoubleStrike, InfectiousStrike]
weapon_special[0x4068] = [DoubleStrike, InfectiousStrike]

weapon_special[0x26BF] = [DoubleStrike, InfectiousStrike]
weapon_special[0x26C9] = [DoubleStrike, InfectiousStrike]

weapon_special[0x1400] = [ ArmorIgnore, InfectiousStrike]
weapon_special[0x1401] = [ ArmorIgnore, InfectiousStrike]

weapon_special[0x26BE] = [ParalyzingBlow, InfectiousStrike]
weapon_special[0x26C8] = [ParalyzingBlow, InfectiousStrike]

weapon_special[0xEC2] = [BleedAttack, InfectiousStrike]
weapon_special[0xEC3] = [BleedAttack, InfectiousStrike]

weapon_special[0x0907] = [ ArmorIgnore, MortalStrike]
weapon_special[0x4076] = [ ArmorIgnore, MortalStrike]

weapon_special[0x0905] = [DoubleStrike, MortalStrike]
weapon_special[0x4070] = [DoubleStrike, MortalStrike]

weapon_special[0x090C] = [BleedAttack, MortalStrike]
weapon_special[0x4073] = [BleedAttack, MortalStrike]

weapon_special[0x48C6] = [ParalyzingBlow, MortalStrike]
weapon_special[0x48C7] = [ParalyzingBlow, MortalStrike]

weapon_special[0x26C2] = [ArmorIgnore, MovingShot]
weapon_special[0x26CC] = [ArmorIgnore, MovingShot]

weapon_special[0xF4F] = [ConcussionBlow, MortalStrike]
weapon_special[0xF50] = [ConcussionBlow, MortalStrike]

weapon_special[0x1402] = [ShadowStrike, MortalStrike]
weapon_special[0x1403] = [ShadowStrike, MortalStrike]

weapon_special[0x26BC] = [CrushingBlow, MortalStrike]
weapon_special[0x26C6] = [CrushingBlow, MortalStrike]

weapon_special[0x143C] = [ArmorIgnore, MortalStrike]
weapon_special[0x143D] = [ArmorIgnore, MortalStrike]

weapon_special[0x26C1] = [DoubleStrike, MortalStrike]
weapon_special[0x26CB] = [DoubleStrike, MortalStrike]

weapon_special[0x26BB] = [ParalyzingBlow, MortalStrike]
weapon_special[0x26C5] = [ParalyzingBlow, MortalStrike]

weapon_special[0xF45] = [BleedAttack, MortalStrike]
weapon_special[0xF46] = [BleedAttack, MortalStrike]

weapon_special[0x26C3] = [DoubleStrike, MovingShot]
weapon_special[0x26CD] = [DoubleStrike, MovingShot]

weapon_special[0x08FE] = [BleedAttack, ParalyzingBlow]
weapon_special[0x4072] = [BleedAttack, ParalyzingBlow]

weapon_special[0x48B8] = [ConcussionBlow, ParalyzingBlow]
weapon_special[0x48B9] = [ConcussionBlow, ParalyzingBlow]

weapon_special[0x48C4] = [BleedAttack, ParalyzingBlow]
weapon_special[0x48C5] = [BleedAttack, ParalyzingBlow]

weapon_special[0xF62] = [ ArmorIgnore, ParalyzingBlow]
weapon_special[0xF63] = [ ArmorIgnore, ParalyzingBlow]

weapon_special[0xDF0] = [WhirlwindAttack, ParalyzingBlow]
weapon_special[0xDF1] = [WhirlwindAttack, ParalyzingBlow]

weapon_special[0x13F8] = [ConcussionBlow, ParalyzingBlow]
weapon_special[0x13F9] = [ConcussionBlow, ParalyzingBlow]

weapon_special[0x26BA] = [BleedAttack, ParalyzingBlow]
weapon_special[0x26C4] = [BleedAttack, ParalyzingBlow]

weapon_special[0x13B5] = [DoubleStrike, ParalyzingBlow]
weapon_special[0x13B6] = [DoubleStrike, ParalyzingBlow]

weapon_special[0x13B9] = [CrushingBlow, ParalyzingBlow]
weapon_special[0x13BA] = [CrushingBlow, ParalyzingBlow]

weapon_special[0x2D1F] = [LightningArrow, PsychicAttack]
weapon_special[0x2D2B] = [LightningArrow, PsychicAttack]

weapon_special[0x27A2] = [CrushingBlow, RidingSwipe]
weapon_special[0x27ED] = [CrushingBlow, RidingSwipe]

weapon_special[0x2D1E] = [ForceArrow, SerpentArrow]
weapon_special[0x2D2A] = [ForceArrow, SerpentArrow]

weapon_special[0x2D21] = [InfectiousStrike, ShadowStrike]
weapon_special[0x2D2D] = [InfectiousStrike, ShadowStrike]

weapon_special[0xFB4] = [CrushingBlow, ShadowStrike]
weapon_special[0xFB5] = [CrushingBlow, ShadowStrike]

weapon_special[0xF51] = [InfectiousStrike, ShadowStrike]
weapon_special[0xF52] = [InfectiousStrike, ShadowStrike]

weapon_special[0x13EC] = [CrushingBlow, ShadowStrike]
weapon_special[0x13E4] = [CrushingBlow, ShadowStrike]

weapon_special[0x1440] = [BleedAttack, ShadowStrike]
weapon_special[0x1441] = [BleedAttack, ShadowStrike]

weapon_special[0x1442] = [DoubleStrike, ShadowStrike]
weapon_special[0x1443] = [DoubleStrike, ShadowStrike]

weapon_special[0x48CE] = [DualWield, TalonStrike]
weapon_special[0x48CF] = [DualWield, TalonStrike]

weapon_special[0xF4B] = [DoubleStrike, WhirlwindAttack]
weapon_special[0xF4C] = [DoubleStrike, WhirlwindAttack]

weapon_special[0x27A8] = [Feint, NerveStrike]
weapon_special[0x27F3] = [Feint, NerveStrike]

weapon_special[0x406C] = [MovingShot, InfusedThrow]
weapon_special[0x0901] = [MovingShot, InfusedThrow]


# Hard Coded weapon abilities
def default_weapon_abilities(itemID):
    if itemID in weapon_special:
        return weapon_special[itemID]
    else:
        return [None, None]
#
   

def MoveToBOH():
    if Misc.CheckSharedValue("BagOfHolding"):
        bagOfHolding = Misc.ReadSharedValue("BagOfHolding")
        boh_types = [0x0E1F, 0x1bdd, 0x1bfb, 0x19b9, 0x1081, 0x26b4, 0xeed, 0x9f1, 0x318f, 0x3190, 0x3191, 0xf3f,  0xe21]    
        boh_items = []
        for i in findRecursive(Player.Backpack.Serial, boh_types):
            if i.Container != bagOfHolding:                
                   boh_items.append(i)
            #boh_items = [i for i in boh_items if i.ItemID != 0xe24 or i.Hue == 0]
        for item in boh_items:            
            if Items.GetPropStringByIndex(item, 1).lower() != "blessed":
                Items.Move(item.Serial, bagOfHolding, 0)
                Misc.Pause(800)


    