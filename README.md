![](Assets/Cat_Avatar_Rounded.png)
# Cat vs Rat

## Requirements:
* Python 3.10 or higher
* pygame 2.1.2 or higher
> If your python version is not so high, you can change all the match case statements to if else statements or you can install the exe


## How to run

Run main file:
```batch
python main.py
```
Arguments:
```batch
[--map [MAP]] [--sound | --no-sound]
```
Map: The map you want to play
Sound: To decide if you want sound in the game, default as yes

Run map maker:
```batch
python map_maker.py
```
Arguments:
```batch
[--map [MAP]]
```
Map: The map you want to play

## How to play
### Cat:
* **Type:** Player sprite
* **Size:** 1 x 1
* **Controls:** Keyboard arrow keys &#8593; &#8592; &#8595; &#8594;
* **Game goal:** Kill all rats and protect tomato
* **Atributes:** Can't walk over tomato and other cats

### Rat:
* **Type:** Player sprite
* **Size:** 1 x 1
* **Controls:** <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>
* **Game goal:** Eat all tomatoes and don't get eaten by cat
* **Atributes:** Can't walk pass other rats
> Player sprites will have special ability in the future

### Box
* **Type:** Map object
* **Size:** 1 x 1
* **Attributes:** Player sprites cannot walk pass it

### Hole:
* **Type:** Map object
* **Size**: 2 x 1
* **Attributes:** If sprite go into the hole, the sprite will com out from the other hole in the map. Every sprites can access this hole but have a 2 seconds cooldown everytime using the hole
* **Quantity:** 0 or 2

### Spike:
* **Type:** Map object
* **Size:** 1 x 1
* **Attributes:** When active, sprites can't walk pass through it, the form will change every 2 seconds

# More:
**[Asset source](https://comigo.itch.io/farm-puzzle-animals)**\
**Download game at [itch.io](https://mortis-666.itch.io/cat-vs-rat)**

