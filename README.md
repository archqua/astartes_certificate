# Astartes Certificate
## Description
IIII python course final project.
The concept is spacemarine fighting while sad music is playing in background.
No fun, no scores, no achievements, no winning.
Our choice of music is the group "Death Certificate" (rus Свидетельство о Смерти).

## Dependencies
`python` version 3.10.8.
`pygame` version 2.1.2 can be installed via provided `install_env.sh`
or manually.
There are decent chances that everything will work with older versions
but it was never tested.

## Install and run
```
git clone https://github.com/archqua/astartes_certificate.git
cd astartes_certificate
./install_env.sh
./run_game.sh
```

To run after install just `./run_game.sh`.

If you have pygame in your environment you can just `./main.py`.

## Artwork
[Space marine head](https://www.pinterest.com/pin/790241065842390785/),
[orc heads](https://itchynick.artstation.com/projects/L3aVr),
[boltgun](https://warhammer40k.fandom.com/wiki/Weapons_of_the_Imperium?file=ImperialWeapons2.jpg) and
[bullet (bolt)](https://www.reddit.com/r/Warhammer40k/comments/9slits/on_the_scale_mismatch_between_bolts_and_bolters/).

Death Certificate's tracks were downloaded using [catpy vk bot](https://vk.com/catpy).

## Playing
WASD or arrows to move, mouse to aim and shoot, ESC to exit.

Initially enemies spawn every 2 seconds,
this time gradually shortens to less than a second
and the game gets rather intense.

You have 3 shields that restore (and are wasted) rather quickly and
2 health points, health doesn't restore.



