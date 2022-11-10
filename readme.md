# What is the purpose of this program?

Tentative Description: This program is a simple game of rock, paper, scissors. The user will be prompted to enter either rock, paper, or scissors. The computer will then randomly select either rock, paper, or scissors. The program will then determine the winner of the game and display the results.

## How to use Application

tentative description of how to utilize project

## How does it work

tentative description of the spooky inner workings of the project

## Changes in this version

### name of change A

tentative description of change A

### name of change B

tentative description of change B

### name of change C

tentative description of change C

### name of change D

tentative description of change D

if ingredient tree was cloned from the csv file, when the user populates the ingredient tree and is prompted an amount, 
if the user leaves their input blank, make sure that the value defaults to the one from the csv file
```py
industrial_battery: Node = Node('industrial battery', None)
protocite_bar: Node = Node('protocite bar', industrial_battery, 0, 1, 5)
protocite: Node = Node('protocite', protocite_bar, 0, 1, 2)
battery: Node = Node('battery', industrial_battery, 0, 1, 2)
pixels: Node = Node('pixels', battery, 0, 1, 2500)
quantum_processor: Node = Node('quantum processor', industrial_battery)
silicon_board: Node = Node('silicon board', quantum_processor, 0, 1, 4)
protocite_bar2: Node = Node('protocite bar', quantum_processor, 0, 1, 2)
protocite2: Node = Node('protocite', protocite_bar2, 0, 1, 2)
thorium_rod: Node = Node('thorium rod', industrial_battery, 0, 1, 5)
thorium_ore: Node = Node('thorium ore', thorium_rod, 0, 1, 2)
```