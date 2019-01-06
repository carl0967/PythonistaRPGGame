from objc_util import *
from random import random
from scene import *
import ui


class Game (Scene):
	cell_sieze = 64
	move_postion = Point(0,0)
	moving = False
		
	def touch_began(self,touch):
		print('touch')
		x, y = touch.location
		self.move_postion = Point(x,y)
		self.moving = True
		#move_action = Action.move_to(x, y, 0.7, TIMING_SINODIAL)
		#self.player.run_action(move_action)
		
	def initializeCharactor(self):
				boy = SpriteNode('plc:Character_Boy', position=(64*2, 64))		
				self.player = boy
				self.add_child(boy)
	
	def initializeItems(self):
		for i in range(5):
			x = self.cell_sieze * i
			y = self.cell_sieze * i
			node = SpriteNode('plc:Chest_Closed',position = (x,y))
			self.add_child(node)
			
	def setup(self):
		self.background_color = '#004f82'
		self.initializeCharactor()
		
		self.initializeItems()
		
		ground = Node(parent=self)
		x = 0
		# Increment x until we've reached the right edge of the screen...
		while x <= self.size.w + 64:
			tile = SpriteNode('plf:Ground_PlanetHalf_mid', position=(x, 0))
			ground.add_child(tile)
			# Each tile is 64 points wide.
			x += 64
				
	def update(self):
		if self.moving:
			x = self.player.position.x
			y = self.player.position.y
			
			diff_x = (self.move_postion.x - x)
			diff_y = (self.move_postion.y - y)
			
			move_x = 0
			move_y = 0
			
			if abs(diff_x) > self.cell_sieze:
				if diff_x > 0:
					move_x = self.cell_sieze
				else:
					move_x = -self.cell_sieze
			if abs(diff_y) > self.cell_sieze:
				if diff_y > 0:
					move_y = self.cell_sieze
				else:
					move_y = -self.cell_sieze
			
			if move_x == 0 and move_y == 0:
				self.moving = False
				return
				
			self.player.position = (x + move_x, y + move_y)

UIKeyCommand = ObjCClass('UIKeyCommand')

modifiers = {(1<<17): 'Shift', (1<<18): 'Ctrl', (1<<19): 'Alt', (1<<20): 'Cmd', (1<<21): 'NumPad'}

def keyCommands(_self, _cmd):
		cmd_key_flag = (1<<20)
		key_d = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('D', 0, 'keyCommandAction:')
		key_a = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('A', 0, 'keyCommandAction:')
		key_w = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('W', 0, 'keyCommandAction:')
		key_s = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('S', 0, 'keyCommandAction:')
		key_command_r = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('R', cmd_key_flag, 'keyCommandAction:')
		key_command_b = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('B', cmd_key_flag, 'keyCommandAction:')
		commands = ns([key_d,key_a,key_w,key_s,key_command_r, key_command_b])
		return commands.ptr

def canBecomeFirstResponder(_self, _cmd):
		return True

def keyCommandAction_(_self, _cmd, _sender):
	self = ObjCInstance(_self)
	key_cmd = ObjCInstance(_sender)
	flags = key_cmd.modifierFlags()
	modifier_str = ' + '.join(modifiers[m] for m in modifiers.keys() if (m & flags))
	key_input = key_cmd.input()
	print 'Input: "%s" Modifiers: %s' % (key_input, modifier_str)
	
	x = game_view.player.position.x
	
	y = game_view.player.position.y
	
	move_size = 64
	if str(key_input) == 'D':
		x = x + move_size
	elif str(key_input) == 'A':
		x = x - move_size
	elif str(key_input) == 'W':
		y = y + move_size
	elif str(key_input) == 'S':
		y = y - move_size
	
	game_view.player.position = (x,y)

KeyCommandsView = create_objc_class('KeyCommandsView', UIView, [keyCommands, canBecomeFirstResponder, keyCommandAction_])

game_view = Game()

@on_main_thread
def main():
		x = 800
		y = 800
		frame = (0,0,x,y)
		main_view = SceneView(frame=frame)
		main_view.name = 'Key Commands Demo'

		v = KeyCommandsView.alloc().initWithFrame_(((0, 0), (0,0)))
		v.setBackgroundColor_(UIColor.lightGrayColor())
		v.becomeFirstResponder()
		ObjCInstance(main_view).addSubview_(v)

		main_view.present('sheet')
		main_view.scene = game_view

if __name__ == '__main__':
		main()
