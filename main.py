import random, time
import tcod, tcod.event

GAMESTATE = 2
WIDTH, HEIGHT = 30, 17
SCORE = 1
EASY = 3
MEDIUM = 1
HARD = 0.4
dfl = [EASY,MEDIUM,HARD]
diffstate = 1
DIFFICULTY = (0.1) * dfl[diffstate]
foodlist = []
difflist = [
    'EASY',
    'MEDIUM',
    'HARD'
]
currentfood = (random.randint(1, WIDTH-3), random.randint(1, HEIGHT-3))


class Tile:
    def __init__(self, x: int, y:int, age: int):
        self.x = x
        self.y = y
        self.age = age


class Snake:
    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction
    def move(self, dx: int, dy:int) -> None:
        self.x += dx
        self.y += dy


def create_food(activetiles, player) -> None:
    global currentfood
    print('Create food called.')
    checklist = []
    for i in range(len(activetiles)):
        checklist.append((activetiles[i].x, activetiles[i].y))
    checklist.append((player.x, player.y))
    def new_random():
        return (random.randint(1, WIDTH-3), random.randint(1, HEIGHT-3))
    match = True
    newran = new_random()
    while match == True:
        if newran in checklist:
            newran = new_random()
        else:
            match = False
    currentfood = newran

def eat_food(activetiles, gameboard, currentfood, player) -> int:
    global SCORE
    print('Eat food called.')
    SCORE += 1
    print(str(SCORE) + ' is the current score.')
    gameboard[currentfood[0]][currentfood[1]] = 0
    create_food(activetiles, player)



def str_TCOD(i: int):
    this = chr(tcod.tileset.CHARMAP_TCOD[i])
    return this

def draw_border(x=0, y=0, width=WIDTH, height=HEIGHT, console = tcod.Console(WIDTH, HEIGHT, order="F")):
    for i in range(width - 2): # PRINTING TOP ROW
        console.print(x=(x + 1 + i), y=(y + 0), string=str_TCOD(47))
    for i in range(width - 2): # PRINTING BOTTOM ROW
        console.print(x=(x + 1 + i), y=(y+height-1), string=str_TCOD(47))
    for i in range(height - 2): # PRINTING LEFT COLUMN
        console.print(x=(x + 0), y=(y + 1 + i), string=str_TCOD(46))
    for i in range(height - 2): # PRINTING RIGHT COLUMN
        console.print(x=(x + width - 1), y=(y + 1 + i), string=str_TCOD(46))
    console.print(x=(x + 0),y=(y + 0), string=str_TCOD(54)) # TOP LEFT CORNER
    console.print(x=(x + width-1) ,y=(y + 0), string=str_TCOD(55)) # TOP RIGHT CORNER
    console.print(x=(x + 0), y=(y + height-1), string=str_TCOD(53)) # BOTTOM LEFT CORNER
    console.print(x=(x + width-1), y=(y + height-1), string=str_TCOD(56)) # BOTTOM RIGHT CORNER



def main() -> None:
    global GAMESTATE
    activetiles = []
    player = Snake(1,0,'right')
    create_food(activetiles, player) #temp food create
    gameboard = [[0] * (HEIGHT-2) for i in range(WIDTH-2)]
    firsttile = Tile(player.x, player.y, SCORE)
    activetiles.append(firsttile)
    tileset = tcod.tileset.load_tilesheet("MANNfont10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    root_console = tcod.Console(WIDTH, HEIGHT, order="F")
    print('Difficulty set to: ' + str(DIFFICULTY))
    with tcod.context.new(columns=WIDTH, rows=HEIGHT, tileset=tileset, title='Snake by JMANN') as context:
        while True:

            root_console.clear()

            draw_border(0, 0, WIDTH, HEIGHT, root_console)

            if player.direction == 'left':
                player.move(-1,0)
                newmove = Tile(player.x, player.y, SCORE)
                #activetiles.append(newmove)
            if player.direction == 'right':
                player.move(1,0)
                newmove = Tile(player.x, player.y, SCORE)
                #activetiles.append(newmove)
            if player.direction == 'down':
                player.move(0,1)
                newmove = Tile(player.x, player.y, SCORE)
                #activetiles.append(newmove)
            if player.direction == 'up':
                player.move(0,-1)
                newmove = Tile(player.x, player.y, SCORE)
                #activetiles.append(newmove)

            # is player out of bounds?
            if player.x < 0:
                print('Player X is less than 0.')
                GAMESTATE = 1
                return
            if player.y < 0:
                print('Player Y is less than 0.')
                GAMESTATE = 1
                return
            if player.x > WIDTH - 3:
                print('Player X is greater than WIDTH.')
                GAMESTATE = 1
                return
            if player.y > HEIGHT - 3:
                print('Player Y is greater than HEIGHT.')
                GAMESTATE = 1
                return

            # is player inside of player?
            for i in range(len(activetiles)):
                xact = activetiles[i].x
                yact = activetiles[i].y
                if player.x == xact:
                    if player.y == yact:
                        print('Player and tail exist together.')
                        GAMESTATE = 1
                        return
            
            activetiles.append(newmove)
            
            # food
            gameboard[currentfood[0]][currentfood[1]] = 2
            if currentfood[0] == player.x:
                if currentfood[1] == player.y:
                    eat_food(activetiles, gameboard, currentfood, player)

            # snake age logic
            templist = []
            for i in range(len(activetiles)):
                if activetiles[i].age > 0:
                    templist.append(activetiles[i])
                if activetiles[i].age < 1:
                    try:
                        gameboard[activetiles[i].x][activetiles[i].y] = 0
                    except:
                        print('Error out of bound.')
                        continue
            activetiles = templist          
            for i in range(len(activetiles)):
                try:
                    gameboard[activetiles[i].x][activetiles[i].y] = 1
                except:
                    print('Error out of bound.')
                    continue
                activetiles[i].age -= 1


            # gameboard printing
            for x in range(len(gameboard)):
                for y in range(len(gameboard[0])):
                    if gameboard[x][y] == 1:
                        root_console.print(x=x+1,y=y+1,string=str_TCOD(45))
                    if gameboard[x][y] == 0:
                        root_console.print(x=x+1,y=y+1,string=str_TCOD(159))
                    if gameboard[x][y] == 2:
                        root_console.print(x=x+1,y=y+1,string=str_TCOD(77))
            

            context.present(console=root_console)

            time.sleep(DIFFICULTY)

            for event in tcod.event.get():
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.LEFT':
                        if player.direction == 'right':
                            continue
                        else:
                            player.direction = 'left'
                        print(player.direction)
                    if str(event.sym) == 'KeySym.UP':
                        if player.direction == 'down':
                            continue
                        else:
                            player.direction = 'up'
                        print(player.direction)
                    if str(event.sym) == 'KeySym.RIGHT':
                        if player.direction == 'left':
                            continue
                        else:
                            player.direction = 'right'
                        print(player.direction)
                    if str(event.sym) == 'KeySym.DOWN':
                        if player.direction == 'up':
                            continue
                        else:
                            player.direction = 'down'
                        print(player.direction)
                    elif isinstance(event, tcod.event.KeyDown):
                        if str(event.sym) == 'KeySym.ESCAPE':
                            raise SystemExit()
        
def gameover() -> None:
    global GAMESTATE
    global SCORE
    global diffstate
    global DIFFICULTY
    tileset = tcod.tileset.load_tilesheet("MANNfont10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    go_console = tcod.Console(WIDTH, HEIGHT, order="F")
    with tcod.context.new(columns=WIDTH, rows=HEIGHT, tileset=tileset, title='Snake by JMANN') as context:
        while True:
            go_console.clear()
            go_console.print(x=1,y=int((HEIGHT/2)-6),string='# Difficulty: ' + str(difflist[diffstate]))
            go_console.print(x=1,y=int((HEIGHT/2)-4),string='# Score: ' + str(SCORE))
            go_console.print(x=1,y=int((HEIGHT/2)),string='# Press SPACE to PLAY AGAIN')
            go_console.print(x=1,y=int((HEIGHT/2)+2),string='# Press ESC to QUIT')
            draw_border(0, 0, WIDTH, HEIGHT, go_console)

            context.present(console=go_console)
            for event in tcod.event.get():
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.SPACE':
                        GAMESTATE = 0
                        return
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.ESCAPE':
                        raise SystemExit()
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.LEFT':
                        if diffstate > 0:
                            diffstate -= 1
                            DIFFICULTY = (0.1) * dfl[diffstate]

                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.RIGHT':
                        if diffstate < 2:
                            diffstate += 1 
                            DIFFICULTY = (0.1) * dfl[diffstate]


def start() -> None:
    global diffstate
    global GAMESTATE
    global DIFFICULTY
    tileset = tcod.tileset.load_tilesheet("MANNfont10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    st_console = tcod.Console(WIDTH, HEIGHT, order="F")
    with tcod.context.new(columns=WIDTH, rows=HEIGHT, tileset=tileset, title='Snake by JMANN') as context:
        while True:
            
            st_console.clear()
            draw_border(0, 0, WIDTH, HEIGHT, st_console)
            st_console.print(x=1,y=int((HEIGHT/2)-6),string='# Change Difficulty: ' + str(difflist[diffstate]))
            st_console.print(x=1,y=int((HEIGHT/2)),string='# Press SPACE to PLAY')
            context.present(console=st_console)
            
            for event in tcod.event.get():
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.SPACE':
                        GAMESTATE = 0
                        return
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.ESCAPE':
                        raise SystemExit()     
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.LEFT':
                        if diffstate > 0:
                            diffstate -= 1
                            DIFFICULTY = (0.1) * dfl[diffstate]
                if isinstance(event, tcod.event.KeyDown):
                    if str(event.sym) == 'KeySym.RIGHT':
                        if diffstate < 2:
                            diffstate += 1
                            DIFFICULTY = (0.1) * dfl[diffstate] 

while True:
    if GAMESTATE == 0:
        main()
    if GAMESTATE == 1:
        gameover()
    if GAMESTATE == 2:
        start()