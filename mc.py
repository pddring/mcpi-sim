print "Loading... please wait"

# import minecraft modules
from local.minecraft import *
from local.block import *

# create link to minecraft game or simulator
# change 10.10.95.64 to the ip address of your raspberry pi
mc = Minecraft.create("10.10.95.64")

# post a chat message
mc.postToChat("Hello")

# draw a stone block at (x=0, y=0, z=0)
mc.setBlock(0,0,0, STONE)