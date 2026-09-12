# Elephant Chaser
A top-down 2D game I built in Python with Pygame. You fight off enemies, try to keep your animal allies alive, and grab gold coins while surviving as many levels as you can — each one throws more enemies at you than the last.


Controls:
- Move using **WASD** or the **arrow keys**
- Fire bullets with **F** or **Space** in the direction you're facing
- Adjust movement speed with **Z** (slower) and **C** (faster), or stop with **E**
- Destroy enemies (dragons, lizards, rats, ghosts) before they reach you — contact with an enemy ends the game
- Keep friendly animals (elephants, giraffes, sloths) alive — enemies will kill them on contact
- Collect gold doubloons scattered around the map for points
- Shoot through stone-wall blocks, which take multiple hits to break
- Clearing all enemies on a level advances you to the next, which spawns more enemies, animals, and obstacles


Running the game:
```bash
pip install pygame
python main.py
```
​

Project Structure:
- main.py — entry point, launches the game
- objects.py — game entities and core logic: the player, enemies, animals, bullets, blocks, and coins, plus the `Game` class managing the level loop
- images.py — image loading and asset management
- sounds.py — sound effect handling
- colors.py — color constants used across rendering
- images/, sounds/ — game assets

Design notes:

Collisions between objects are resolved using a double-dispatch pattern: every object implements a hit_by() method and a set of hit_<type>() methods, so any pair of object types (e.g. a bullet hitting a block, an enemy hitting an animal) resolves through its own pair of methods rather than a large conditional chain. This keeps collision logic contained within each class and made it straightforward to add new object types.

About:

Built as a personal project for fun and to practice game design implementing OOP and real-time collision handling in Python.
