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
       get_all_bombs			    -> provides bomb data

    Player Data : A Dictionary Containing
        "coordinate"                        -> Position
        "bomb_size"                         -> Explosion Radius
        "bomb_count"                        -> Number of Bombs that can be deployed at a time
        "index"                             -> Player Index
	"point"				    -> Current Point of Player

    Bomb Data : A Dictionary Containing
        "coordinate"                        -> Position
        "radius"                            -> Explosion Radius
        "player_index"                      -> Index of the player placing the bomb
	"time_till_detonation"		    -> Ticks remaining till the bomb explodes (this is initially 7)

	
Player : Written by contestants, a sample is given.

    What has to be done:
        1. Have variables reset, done, success, index initialized at __init__ function
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
	  in the main playing loop. While it is encouraged to name this method "play", it is not mandatory.
        3. Execution of a round :
	  -> After all players schedule their moves, the processor will execute all necessary actions to complete those moves.
	  -> After execution, the reset variable of each living player will be set to true.
	  -> If a player dies, over variable of that player will be set to true.
	  -> It will be the players' duty to make sure it does not schedule any more move after the over variable is set to true.
	  -> If reset is true and over is false, the player can attempt to schedule the next move. Note that if you do not set the reset variable back to false you will not be able to prevent scheduling multiple times before one round is over.
	  -> Attempting to schedule multiple action in one round will result in disqualification.
        4. Attempting to call private functions or edit internal variables will result
           in disqualification
	   
Game End:

	1. The game will last for 300 turns (subject to change)
	2. Every block broken will award one point to the breaking player.
	3. If there is only one player on the field, that player will be the winner.
	4. A dead player cannot win, regardless of points accumulated.

