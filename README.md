# Othello_AI

Developed two versions of Othello AI using a Minimax and an Alpha-beta algorithm. The code written by me is in agent.py and the rest of the file is provided by the University of Toronto..

To play with the AI. Please use the following input format in cmd or Terminal:

$python3 othello_gui.py -d <dimension> [-a <agentA> -b <agentB> -l <depth-limit> -c -o]

-d flag: specify the dimension of the board.
  
-a flag: specify which AI to play with. You can choose between agent.py or randy_ai.py (an AI that plays randomly).
 
-b flag: specify another AI. You can choose between agent.py or randy_ai.py. By setting this flag, you will watch AI in the -a flag play with AI in the -b flag.
 
-l flag: specify the depth limit for the algorithm to search. Higher means AI plays better. Recommended limit is 5 unless you have a beefy computer.

-c flag: enables caching which speeds up the AI.

-o flag: enables node ordering which speeds up the AI further. This flag works only on Alpha-beta version of the AI.
 
-m flag: use this flag when you want to play with the Minimax version of the AI.

Example 1:
'''
  $python3 othello_gui.py -d 8 -a agent.py -l 5 -m -c
'''
This allows you to play with the Minimax version of the AI on a 8x8 board.

Example 2:
'''
  $python3 othello_gui.py -d 8 -a agent.py -l 5 -c -o
'''
This allows you to play with the Alpha-beta version of the AI on a 8x8 board.
