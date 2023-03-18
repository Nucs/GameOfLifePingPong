# Game Of Life Ping Pong
An experiment using ChatGPT 4. Created Game of Life with Ping Pong with almost no manual changes.<br/>
The game is split into two halves, on the left is a Game of Life and on the right is the classic Ping Pong.


![image](https://user-images.githubusercontent.com/649919/226140828-b47b4db9-1191-4eea-b662-15fb4defe191.png)

## Game features
- Physics Collision using numpy with slight randomization for more rebust gameplay
- When the ball is in the game of life side, the cells are frozen
- When the ball hits the paddle, 3 clumps of 7 cells are added to the game of life, keeping it fueled.
- When the paddle misses the ball, the score halves.

## Running the game
```sh
pip install numpy
pip install pygame
```

Start the game by executing: 
```sh
python main.py
```
