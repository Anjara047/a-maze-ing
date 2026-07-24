*This project has been created as part of the 42 curriculum by tsiarran, tsanjara.*

# A-Maze-ing

## Description

### Generality
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A-Maze-ing is a maze generation project developed as part of the 42 curriculum. The program generates a maze according to parameters provided in a configuration file and writes the generated maze to an output file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The project focuses on algorithmic thinking, configuration parsing, maze representation, error handling, and the organization of reusable Python code.

### Goal
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Goal of this project is to generate a Maze from valid parameters in config.txt file, which contains the width, the length of the maze.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After generating the maze, this project requires the solution of the generated
maze from the entry to the exit, which is finding the path from the given entry to the exit

### Rules
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The program reads all required parameters from a configuration file. The maze dimensions, entry point, exit point, output file, and maze type are defined before generation.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The program validates the configuration before generating the maze. Invalid dimensions, coordinates, values, or configuration formats must produce an appropriate error.

## Instructions

### Compilation

```bash
make install:        # Install the required dependencies(mlx) via poetry
make run    :        # Run the program after the dependencies are all installed
make clean  :        # Remove generated files, caches and temporary files
make lint   :        # Run flake8 and mypy
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; After cloning the project, the first command to run is `make install`. This command installs all the dependencies required by the project through Poetry, including MLX. This step is mandatory before running the application. If the dependencies are not installed, the project will not be able to execute correctly, and some features may fail to work.


## Resources

* Thanks to the 42 School learning system, particularly the peer-to-peer methodology, which greatly helped in understanding the project's objectives and expectations.
* Online documentation and tutorials(Google, youtube, etc.), which provided ideas and inspiration for Algorithms, strategies, and implementation technics

### Use of AI

* AI tools were used as learning aids to better understand expected behaviors, clarify edge cases, and verify reasoning while debugging.
* AI was not used to directly generate the project solution, but to assist with explanations, documentation writing, and overall project organization.

## About The project

From here we're gonna talk much more about the project

### Structure and Format of the Configuration File

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  This project really depend on this file, this file contains all the mandatory parametrs

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The maze generator reads its settings from a configuration file. Each parameter controls a specific aspect of the maze generation, such as its dimensions, the positions of the entry and exit, the output file, and the generation options. The available parameters are described below.

```text
# Maze width
WIDTH
Defines the width of the maze (and the MLX window), in cells.

# Maze height
HEIGHT
Defines the height of the maze (and the MLX window), in cells.

# Entry coordinates (x,y)
ENTRY
Specifies the coordinates of the maze entry in the format x,y.

# Exit coordinates (x,y)
EXIT
Specifies the coordinates of the maze exit in the format x,y.

# Output filename
OUTPUT_FILE
Specifies the name of the file where the generated maze will be saved.

# Is the maze perfect?
PERFECT
Set to True to generate a perfect maze, or False to allow multiple possible paths.

# Seed
SEED
An optional value used to initialize the random number generator. Using the same seed always generates the same maze. Leave it commented out or omit it to generate a different maze each time.
```

There is default config file at the root of the directory if an example is needed

## Algorithm

### Generate Maze

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Generating maze was built through the idea of the algorithm hunt and kill, but this is for the perfect maze, in this file also to generate the name of the output file which contains the hexadecimal the maze, this file also contains on whether the perfect or not maze is and the one is seed.


We tried to create our own algorithm but due to its difficulty in builting the maze as which is the real labirynth, we had to take the inspiration from the existed algorithm

#### The concept of hunt and kill:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The hunt and kill algorithm is one the easiest way to generate a labirynth by visiting all cell while creating passages between them. So everytime a cell is visited, we will mark it as already visited to be able to generate the real maze and avoid conflict

The concept is based on chosing a starting cell and choosing the next randomly wich has not yet visited, carve the wall between them to create a path

##### Kill Phase

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The algorithm starts from the ENTRY(from config.txt), the choosing cell from randomly its neighbord to be the next cell and removes the wall between, after that the current moves into the next cell and the next cell cell becomes the new current to choose randomly its next cell and looping untill all the cell are all visited.

The algorithm moving unvisited neighbor to the another unvisited until it reaches a cell with no unvisited neighbor.
Here is the algorithm becomes difficult because all the neighbor are already visited while there is still unvisited cell and now Hunt Phase comes in action.

##### Hunt Phase

        When a dead end is reached, the behavior depends on the type of maze required.

* **If an imperfect maze is required:** before starting the Hunt phase, the algorithm randomly chooses one of the neighbors of the current cell, excluding the previous cell, and removes the wall between them. The selected neighbor may already have been visited. This additional connection can create loops and multiple possible paths in the maze. After that, the algorithm continues with the Hunt phase.

* **If a perfect maze is required:** no additional wall is removed at the dead end, and the algorithm directly starts the Hunt phase.

        During the Hunt phase, the algorithm searches through the maze for an unvisited cell that has at least one already visited neighbor. Once such a cell is found, a wall between the unvisited cell and one of its visited neighbors is removed. The unvisited cell becomes the new current cell, and the Kill phase starts again.

The algorithm repeatedly alternates between the Kill and Hunt phases until all cells in the maze have been visited.

### Perfect and Imperfect Mazes

A **perfect maze** contains exactly one path between any two cells. In this mode, no additional connection is created when a dead end is reached.

An **imperfect maze** can contain loops and multiple possible paths. In our modified version of the Hunt-and-Kill algorithm, an additional wall can be removed at a dead end before continuing with the Hunt phase.

### Find solution

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The solution path is found using the Breadth-First Search (BFS) algorithm. The algorithm starts from the entry point and explores the maze level by level until reaching the exit.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During the search, visited cells are stored to avoid revisiting the same position, and previous positions are saved to reconstruct the path once the exit is reached.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For this implementation, we used `deque()` from Python's `collections` module as a queue because it allows efficient insertion and removal of elements during the search process.

---

## Why this algorithm?

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We chose the Hunt-and-Kill algorithm because, among the different maze generation algorithms we explored, it was the one that caught our attention the most.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After testing several maze generation approaches, we found that its behavior suited our needs. During the implementation, we encountered some difficulties, so we adapted the algorithm and created our own approach based on its principles.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The final implementation does not strictly follow the original Hunt-and-Kill algorithm. Instead, it uses a custom approach inspired by it, although some parts may unintentionally resemble other known algorithms.

---

## Reusable Code

### Maze Generator

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The **Maze Generator** is the main reusable part of the project because it contains most of the functions responsible for building and generating a maze.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The `MazeGenerator` class can be reused in another file by importing it and creating an instance with the required parameters. Its methods allow users to generate a maze, retrieve the generated maze, solve it, and retrieve the solution path.

**Usage**:

> `get_maze:`  Get the generated maze <br>
> `get_solution:` Get the maze's solution(the path) <br>
> `solve:` Compute the shortest solution <br>
> `generate:` Generate the maze by calling the strategies which has been created above and Initializing all walls before using the hunt & kill algorithm

To install the mazegen package, run this command below:  
        `pip install <path-to>/mazegen-0.1.0-py3-none-any.whl`

Example:   
        `pip install mazegen-0.1.0-py3-none-any.whl`

---
Once the package is installed, you can import the `mazegen` dependency from anywhere within the venv.
---

```
from mazegen import MazeGenerator

generator = MazeGenerator(
    seed=42,
    perfect=True,
    coord_entry=[0, 0],
    coord_exit=[9, 9],
    width=10,
    height=10
)

generator.generate()

maze = generator.get_maze()

generator.solve()
solution = generator.get_solution()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The use of Object-Oriented Programming (OOP) helps organize these features into a structured and reusable module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This reusable component is distributed as the `mazegen` package, which can be installed with pip and reused in other Python projects.

---

## Our Journey During the Project

### Anticipated Planning and How It Evolved

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;At the very beginning of the project, we started by reading and understanding the subject. Then, we learned how to use MLX for the graphical display and explored different maze generation algorithms before choosing an approach that suited our project.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;At one point, we successfully generated a maze structure, but it did not behave like a proper labyrinth. Because of this, we had to reconsider our approach, search for another algorithm, and modify our implementation until we obtained a result that better suited our needs.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Our planning evolved during the development because some parts required more time and testing than expected. Our workflow became iterative:

```
Implement → Test → Debug → Fix → Improve
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The pathfinding part was implemented at the very end of the project, after the maze generation and the main features were working correctly.

---

## Team Organization

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;There was no strict division of tasks between team members. We chose to work together on the different parts of the project to ensure that both members had a complete understanding of the codebase.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If the tasks had been completely divided, each member might only understand their own part of the project. After merging the work, it could become difficult to identify and solve problems related to another section of the code.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Working together allowed us to share knowledge, discuss solutions, understand the evolution of the project, and debug problems more efficiently.


---
## What Worked Well and Future Improvements

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Throughout this project, we dedicated a great deal of time and effort to designing, implementing, and improving our maze generator. We carefully tested the application, handled many edge cases, and resolved numerous issues encountered during development. Our goal was to produce a reliable, maintainable, and reusable project while following the specifications as closely as possible.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Although we are satisfied with the current result, we recognize that there is always room for improvement. If you encounter any bugs, unexpected behavior, or have suggestions that could make the project better, your feedback is greatly appreciated. Every comment or recommendation can help us improve the quality of future versions.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; One feature we would like to improve in the future is the maze animation. A smoother and more interactive animation could better illustrate both the maze generation process and the pathfinding algorithm, making the application more engaging and easier to understand. Additional visual customization, such as adjustable animation speed, themes, or step-by-step visualization, could also further enhance the overall user experience.

---

## Specific Tools

### MLX 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We used **MLX** as the graphical tool for displaying the maze in a window.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It allowed us to represent the generated maze visually by drawing walls, paths, entry, exit, and the solution. This made the result easier to understand compared to displaying the maze only in the terminal.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using MLX also helped us connect the algorithmic part of the project with a graphical interface, making the project more interactive and easier to test.

### deque()

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We used `deque()` from the Python `collections` module for the pathfinding part of the project.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It was used as a queue in the Breadth-First-Search algorithm, allowing us to efficiently add and remove cells while searching for a path from the entry point to the exit.

## Displaying mode
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; All the keyboard control has already been shown on the mlx window once the program works without errors, So just press the keyboard and the maze will change with its instruction related to it

These are all the displaying mode even tought it has been mentionned on the mlx window
```
R: Regenerate the maze, so once R is pressed, the maze will automatically change 
C: Change the color of the maze maze displayed
S: Show the shortest path from the entrypoint to the exit, wich can be the solution as well
X: Closing the mlx window
```


