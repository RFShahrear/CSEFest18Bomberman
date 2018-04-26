Map Description:

I : Indestructible Wall
W : Destructible Wall
B : Bomb (WIP)
P : Player
+ : Increase Bomb Size (NYI)
O : Increase Bomb Count (NYI)
. : Empty Space


Classes:

Visualizer : Pygame handler, not the contestant's concern
MapData : Contains game information
	 (Functions starting with __ is private and not callable)
	 schedule_bomb				-> Place a bomb on current position (WIP)
	 schedule_move (Direction: N/S/E/W) 	-> move to given direction
	 skip_turn				-> Do nothing in current turn
	 get_full_map 				-> Do you really need a written explanation?
	 get_player_data 			-> Take a wild guess 

 	 Player Data : A Dictionary Containing
		"coordinate"	-> Position
		"bomb_size"	-> Explosion Radius
		"bomb_count" 	-> Number of Bombs that can be deployed at once (WIP)
	
Player : Written by contestants, a sample is given.

  	 What has to be done:
		1. Have parameter restart, done, success
			restart -> Start next round
			done 	-> Indicate game over
			success	-> Notifies if last action was successful
		2. Have exactly one call to any of
			-> schedule bomb
			-> schedule_move
			-> skip_turn
		3. reset restart to false when it's true and then starting next round
		3. Calling any of aforementioned functions before restart is triggered will
		   result in a disqualification
		4. Attempting to call private functions or edit internal variables will result
		   in disqualification

