# CSEFest18Bomberman
Map Description:

I 		          : Indestructible Wall

W		            : Destructible Wall

B            		: Bomb

P1, P2, P3, P4 	: Player

\+ 		          : Increase Bomb Size

O 		          : Increase Bomb Count

. 		          : Empty Space


Classes:

Visualizer : Pygame handler, not the contestant's concern

    MapData : Contains game information
    	Every Function need to be called with the player object as the first parameter.
       (Functions starting with __ is private and not normally callable)
       schedule_bomb                        -> Place a bomb on current position
       schedule_move (Direction: N/S/E/W)   -> move to given direction
       skip_turn                            -> Do nothing in current turn
       get_full_map                         -> Provides the current map
       get_self_data                        -> Provides own info
       get_player_data (Index: 1,2,3,4)     -> provides information

    Player Data : A Dictionary Containing
        "coordinate"                        -> Position
        "bomb_size"                         -> Explosion Radius
        "bomb_count"                        -> Number of Bombs that can be deployed at a time
        "index"                             -> Player Index
	
Player : Written by contestants, a sample is given.

    What has to be done:
        1. Have parameters restart, done, success, index
          restart   -> Start next round
          done      -> Indicate game over
          success   -> Notifies if last action was successful
	  index     -> Your position in game
	  		1 -> Upper Left
			2 -> Lower Right
			3 -> Lower Left
			4 -> Upper Right
        2. Have exactly one call to any of
          -> schedule bomb
          -> schedule_move
          -> skip_turn
        3. reset restart to false when it's true and then starting next round
        3. Calling any of aforementioned functions before restart is triggered will
           result in a disqualification
        4. Attempting to call private functions or edit internal variables will result
           in disqualification

