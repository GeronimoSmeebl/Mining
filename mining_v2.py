#
# Things that change based on Player preference:
#
Manual_Tool = None          #   <-- Manually selected mining tool                                #
using_garg = False          #   <-- True if Player wants to use gargish pickaxe                  #
Manual_Bag = 0x40601987     #   <-- Storage bag serial                                           #
Rail_Name = ""              #   <-- Name of rail                                                 #
                            #       Note that rail must be in Data/Rails/ folder                 #
Using_Rail = False
Currently_Mining = False
#

# Credit to Credzba, Fate's Whim, and Mourn
# I used a lot of the code from their scripts
# http://razorenhanced.net/dokuwiki/doku.php?id=toolscripts
# http://razorenhanced.net/dokuwiki/doku.php?id=resourcegatheringscripts

#
import common

import clr, time, thread, sys, System

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Data')
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

from System.Threading import ThreadStart, Thread
from System.Collections.Generic import List
from System import Byte, Int32, Environment
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, BorderStyle, Label, FlatStyle, DataGridView,
 DataGridViewAutoSizeColumnsMode, DataGridViewSelectionMode, DataGridViewEditMode, RadioButton, GroupBox,
 TextBox, CheckBox, ProgressBar)
from System.ComponentModel import BackgroundWorker

#

#
shovelID = 0x0F39
pickaxeID = 0x0E86
waitForTarget = 5000
waitAfterMining = 2500
waitAfterPickAxe = 4000
pickaxe_spots = List[int] (( 0x136D, 0x1367, 0x136A)) 
CaveTiles = [ 0x0016, 0x0017, 0x0018, 0x0019, 0x245, 0x246, 0x247, 0x248, 0x249, 0x22b, 0x22c, 0x22d, 0x22e, 0x22f ]
SoilTiles = [ 0x0073, 0x0074, 0x0075, 0x0076,  0x0077, 0x0078 ]
Hues = List[int] (( 0 ))
#

#
def check_weight(bag):
    if Player.Weight > (Player.MaxWeight*.9) or Player.Weight > 520:
        store_ore(bag)
#

#
railCoords = None
Journal.Clear()
def gotoLocation(x1, y1):
    global Currently_Mining
    
    Coords = PathFinding.Route()
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 10
    if (not PathFinding.Go(Coords)) or not Currently_Mining:
        sys.exit()
    Misc.Pause(600)
#

#
MotionMap = {
                        "North": (0, -1), 
                        "Right": (+1, -1),
                        "East": (+1, 0),
                        "Down": (+1, +1),
                        "South": (0, +1),
                        "Left": (-1, +1),
                        "West": (-1, 0),
                        "Up": (-1, -1),
                        "North": (0, -1), 
                        "Right": (+1, -1),
                        "East": (+1, 0),
                        "Down": (+1, +1),
                        "South": (0, +1),
                        "Left": (-1, +1),
                        "West": (-1, 0),
                        "Up": (-1, -1),
                        }  
#

#
def getVeins():
    findVeins = Items.Filter()
    findVeins.Enabled = True
    findVeins.OnGround = 1
    findVeins.Movable = False
    findVeins.RangeMin = -1
    findVeins.RangeMax = 2
    findVeins.Graphics = pickaxe_spots
    findVeins.Hues = List[int]((  ))
    findVeins.CheckIgnoreObject = True
    listVeins = Items.ApplyFilter(findVeins)
    return listVeins
#

#
def mine_spot(tool, bag):
    global Currently_Mining

    x_delta, y_delta = MotionMap[Player.Direction]
    x = Player.Position.X + x_delta
    y = Player.Position.Y + y_delta
    xStart = Player.Position.X
    yStart = Player.Position.Y
    land_id = Statics.GetLandID(x, y, Player.Map)
    
    Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
    if not Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
        
        Player.Walk('West')
        Misc.Pause(400)
        x_delta, y_delta = MotionMap[Player.Direction]
        x = Player.Position.X + x_delta
        y = Player.Position.Y + y_delta
        xStart = Player.Position.X
        yStart = Player.Position.Y
        land_id = Statics.GetLandID(x, y, Player.Map)
        Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
        if not Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
            
            Player.Walk('North')
            Misc.Pause(400)
            x_delta, y_delta = MotionMap[Player.Direction]
            x = Player.Position.X + x_delta
            y = Player.Position.Y + y_delta
            xStart = Player.Position.X
            yStart = Player.Position.Y
            land_id = Statics.GetLandID(x, y, Player.Map)
            Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
            
    if Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
        Journal.Clear()
        while True:
            if not Currently_Mining:
                sys.exit()
            if Player.Position.X != xStart:
                return
            if Player.Position.Y != yStart:
                return    
            if Journal.Search('no metal'):
                Player.HeadMessage(5, "NONE")
                break
            if Journal.Search('no sand'):
                Player.HeadMessage(5, "DONE")                
                break
            if Journal.Search('Target cannot be seen'):
                break
            if Journal.Search('You can\'t mine there'):
                break
            tileinfo = Statics.GetStaticsLandInfo(x, y, Player.Map)
              
            if not Items.FindBySerial(tool):
                tool = get_tool()
            Items.UseItem(tool)
            Target.WaitForTarget(waitForTarget,False)                    
            tiles = Statics.GetStaticsTileInfo(x, y, Player.Map)

            if tileinfo.StaticID in CaveTiles and len(tiles) > 0:
                Target.TargetExecute(x, y, tiles[0].StaticZ, tiles[0].StaticID)
            else:
                Target.TargetExecuteRelative(Player.Serial, 1)
            Misc.Pause(waitAfterMining)
            on_me_filter = Mobiles.Filter()
            on_me_filter.Enabled = True
            on_me_filter.RangeMin = -1
            on_me_filter.RangeMax = 2
            on_me_filter.Bodies = List[int] ( [ 0x006F ] )
            on_me_filter.Notorieties = List[Byte](bytes([3,4,5,6]))
            up_close_enemies = Mobiles.ApplyFilter(on_me_filter)
            if len(up_close_enemies) > 0:
                Player.HeadMessage(2, "STOPPING FOR AGRO")
                sys.quit()
            if Player.WarMode == True:
                sys.quit()    
            if Target.HasTarget(): 
                Target.Cancel()                    
            check_weight(bag)    
    listVeins = getVeins()
    if listVeins != None and len(listVeins) > 0:
        for vein in listVeins:
            if not Currently_Mining:
                sys.exit()
            while Items.FindBySerial(vein.Serial):
            
                if not Items.FindBySerial(tool):
                    tool = get_tool()
                Items.UseItem(tool)
                
                Target.WaitForTarget(waitForTarget,False)
                Target.TargetExecute(vein)
                Misc.Pause(waitAfterMining)
                check_weight(bag)
            if Target.HasTarget(): 
                Target.Cancel()
#

quit_flag = False

#
# Makes tool(s) in case Player runs out
def make_tool():
    global quit_flag

    if Items.BackpackCount( common.tinker_kitsID, 0 ) < 2:
        if quit_flag:
            Player.HeadMessage(10, "Unable to make tool(s)")
            sys.exit()
        else:
            common.MakeTinkerKits()
            quit_flag = true
            make_tool()
        #
    else:
        common.MakeShovel()
        quit_flag = False
#

#
# Returns Serial of tool for mining
# Only gives gargish pickaxe if using_garg is true; otherwise gives pickaxe or shovel
def get_tool():
    if Manual_Tool != None:
        return Manual_Tool

    tool_list = common.findRecursive(Player.Backpack.Serial, [pickaxeID, shovelID], False)

    for item in tool_list:
        if item.ItemID == pickaxeID and ("garg" in item.Name.lower()) == using_garg:
            return item.Serial
        elif not using_garg and item.ItemID == shovelID:
            return item.Serial
    
    if using_garg:
        Player.HeadMessage(10, "No gargish pickaxes in backpack.")
        sys.exit()
    
    Player.HeadMessage(13, "No tool found. Trying to make shovel.")
    make_tool()
    return get_tool()
#

#
def get_storage():
    if Manual_Bag != None and Items.FindBySerial(Manual_Bag):
        return Manual_Bag
    else:
        sys.exit()
#

#
# Stores resources in keys if possible
# Stores remaining ore in ore storage bag (if present)
def store_ore(bag):
    ore_id = 0x19B9
    # TODO: key storage
    
    # Storage bag
    if bag != None:
        for item in Player.Backpack.Contains:
            if item.ItemID == ore_id:
                Items.Move(item, bag, item.Amount)
#

#
def start_mining_work():
    global Using_Rail
    global Rail_Name
    global Currently_Mining

    #
    tool = get_tool()
    storage_bag = get_storage()
    #
    
    if not storage_bag:
        Player.HeadMessage(11, "No storage found.")
        sys.exit()

    #
    if not Using_Rail:
        Misc.SendMessage("Stationary Mining.")
        mine_spot(tool, storage_bag)
        store_ore(storage_bag)
        Player.HeadMessage(11, "Done with stationary mining.")
        sys.exit()
    #
    
    #
    try:
        rail_file_name = "Data/Rails/" + Rail_Name + ".txt"
        rail_file = open(rail_file_name, "r")
        rail_data_json = rail_file.read()
        rail_locations = JavaScriptSerializer().Deserialize(rail_data_json, list)
        rail_file.close()
        end = not rail_locations
        #
        # Repeats visiting and mining at all rail stops
        while True:
            if end:
                sys.exit()
            #
            
            # Traverse to all rail stops and mines
            for location in rail_locations:
                #
                if not Currently_Mining:
                    sys.exit()
                #
                
                # Go to next stop
                gotoLocation(location[0], location[1])
                Misc.Pause(500)
                check_weight(storage_bag)
                mine_spot(tool, storage_bag)
                store_ore(storage_bag)
    #
    except Exception as e:
        Player.HeadMessage(11, "Unable to traverse rail.")
    #
#

#

class mining_util(Form):

    def __init__(self):
        self.start_color = Color.FromArgb(10,225,10)
        self.stop_color = Color.FromArgb(225,10,10)
        
        self.mining_worker = BackgroundWorker()
        self.mining_worker.DoWork += lambda _, __: self._start_mining_work()
        self.mining_worker.RunWorkerCompleted += lambda _, __: self.notify_completion()
        self.mining_worker.WorkerSupportsCancellation = True
    
        self.Text = "Mining Utility"
        self.Width = 250
        self.Height = 225
        self.TopMost = True
       
        self.button = Button()
        self.button.Text = 'Choose Tool Manually'
        self.button.Width = 100
        self.button.Height = 40
        self.button.Location = Point(10, 10)
        self.button.Click += lambda _, __: self.select_manual_tool()
        
        self.button1 = Button()
        self.button1.Text = 'Clear Manual Tool'
        self.button1.Width = 100
        self.button1.Height = 40
        self.button1.Location = Point(125, 10)
        self.button1.Click += lambda _, __: self.clear_manual_tool()

        self.button2 = Button()
        self.button2.Text = 'Toggle Using Gargish Pickaxe'
        self.button2.Width = 100
        self.button2.Height = 40
        self.button2.Location = Point(125, 50)
        self.button2.Click += lambda _, __: self.toggle_gargish()
        
        self.button3 = Button()
        self.button3.Text = 'Set Ore Bag'
        self.button3.Width = 100
        self.button3.Height = 40
        self.button3.Location = Point(10, 50)
        self.button3.Click += lambda _, __: self.set_storage_bag()
        
        self.button4 = Button()
        self.button4.Text = 'Toggle Rail Mining'
        self.button4.Width = 100
        self.button4.Height = 40
        self.button4.Location = Point(10, 90)
        self.button4.Click += lambda _, __: self.toggle_rail()
        
        self.button5 = Button()
        self.button5.Text = 'START'
        self.button5.Width = 75
        self.button5.Height = 30
        self.button5.Location = Point(135, 135)
        self.button5.BackColor = self.start_color
        self.button5.Click += lambda _, __: self.toggle_mine()
        
        self.textbox = TextBox()
        if Misc.ReadSharedValue("railname"):
            self.textbox.Text = Misc.ReadSharedValue("railname")
        else:
            self.textbox.Text = "Rail_Name"
        self.textbox.Location = Point(10, 140)
        self.textbox.BackColor = Color.FromArgb(180,180,180)
        self.textbox.Width = 115
        
        self.Controls.Add(self.button)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.button2)
        self.Controls.Add(self.button3)
        self.Controls.Add(self.button4)
        self.Controls.Add(self.button5)
        self.Controls.Add(self.textbox)
        
    def select_manual_tool(self,):
        global Manual_Tool
        
        selected = Target.PromptTarget("Select Pickaxe.")
        if Items.FindBySerial(selected).ItemID in [shovelID, pickaxeID]:
            Manual_Tool = selected
        else:
            Misc.SendMessage("Not a valid tool.")
        
    def clear_manual_tool(self):
        global Manual_Tool
    
        Manual_Tool = None
    
    def toggle_gargish(self):
        global using_garg
    
        using_garg = not using_garg
        if using_garg:
            Misc.SendMessage("Gargish pickaxe enabled.")
        else:
            Misc.SendMessage("Gargish pickaxe disabled.")
    
    def set_storage_bag(self):
        global Manual_Bag
    
        selected = Target.PromptTarget("Select storage bag.")
        if Items.FindBySerial(selected).IsContainer:
            Manual_Bag = selected
        else:
            Misc.SendMessage("Not a valid container.")
    
    def toggle_rail(self):
        global Using_Rail
    
        if Using_Rail:
            Using_Rail = False
            Misc.SendMessage("Rail Mining Disabled.")
        else:
            Using_Rail = True
            Misc.SendMessage("Rail Mining Enabled.")
    
    def toggle_mine(self):
        global Currently_Mining
    
        if Currently_Mining:
            self.toggle_mine_off()
        else:
            self.toggle_mine_on()
    
    def notify_completion(self):
        self.toggle_mine_off()
        Misc.SendMessage("Finished with mining work.")
        Player.HeadMessage(12, "Finished with mining work.")
        
    def _start_mining_work(self):
        Misc.SendMessage("Starting mining work.")
        start_mining_work()
    
    def toggle_mine_on(self):
        global Currently_Mining
        global Rail_Name
    
        Currently_Mining = True
        Rail_Name = self.textbox.Text
            
        if not self.mining_worker.IsBusy:
            self.mining_worker.RunWorkerAsync()
            
            self.button5.BackColor = self.stop_color
            self.button5.Text = "STOP"
    
    def toggle_mine_off(self):
        global Currently_Mining
    
        Currently_Mining = False
            
        Misc.Pause(500)
            
        self.button5.BackColor = self.start_color
        self.button5.Text = "START"

#

form = mining_util()
Application.Run(form)