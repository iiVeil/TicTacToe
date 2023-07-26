import curses
from pyTermUI.ui import UI
from pyTermUI.region import Region
from pyTermUI.position import Position
from pyTermUI.text import Text
from pyTermUI.Toolkit.asciiart import AsciiArt
from random import randint

def main(stdscr):
    
    turn = 0
    def on_click(text):
        nonlocal turn
        cell_id = text.region.data.get("id")
        
        if cells[cell_id] != None:
            return
        cells[cell_id] = turn
        turn = not turn
        
        update_grid()

        ui.draw()
        
    def update_grid():

        colors = [204, 42]
        for cell in cells:
            if cells[cell] is not None:
                center = regions[cell-1].size.half() + regions[cell-1].start
                arts[cell-1] = AsciiArt(states[cells[cell]], mainRegion, center)
                arts[cell-1].create()
                for text in arts[cell-1].elements:
                    text.color = colors[cells[cell]]
            
        check_win()
                
    def check_win():
        wins = [
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,5,9],
            [3,5,7]
        ]
        for win in wins:
            if None in [cells[win[0]], cells[win[1]], cells[win[2]]]:
                continue
            if (cells[win[0]] == cells[win[1]] == cells[win[2]]):
                print(f"{'O' if cells[win[0]] else 'X'} WINS!")
                ui.deactivate()
            
        for cell in cells:
            if cells[cell] == None:
                break
            if cell == 9:
                print(f"Draw!")
                ui.deactivate()
                    
                
             
                
        
    ui = UI(stdscr)

    mainRegion = Region("Test", Position.ORIGIN(), Position.DEFAULT_TERM_SIZE())
    mainRegion.framed = False

    cellwidth = 16
    cellheight = 6

    states = ["\    /\n \  / \n  \/  \n  /\  \n /  \ \n/    \\", "╭────╮\n│    │\n│    │\n│    │\n│    │\n╰────╯"]

    arts = [None, None, None, None, None, None, None, None, None]
    board = "                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                \n────────────────┼────────────────┼────────────────\n                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                \n────────────────┼────────────────┼────────────────\n                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                \n                │                │                "
    art = AsciiArt(board, mainRegion, mainRegion.size.half())
    
    cells = {
        1: None, 2: None, 3: None,
        4: None, 5: None, 6: None,
        7: None, 8: None, 9: None
        }
    
            
    
    art.create()
    
            
    regions = []
    
    for y in range(3):
        for x in range(3):
            region = Region(f"{x+1*y+1}", art.startpos + (Position((cellwidth*x+x), (cellheight*y+y)) + Position(1,1)), Position(cellwidth, cellheight))
            region.data = {"id": len(regions)+1}
            region.framed = False
            regions.append(region)
    
    for region in regions:
        for y in range(region.size.y+1):
            text = Text(" "*region.size.x, Position(0-1, y-1))
            text.callback = on_click
            region.add_element(text)
    
    
    for region in regions:
        ui.add_region(region)
    

    

    

    ui.add_region(mainRegion)

    ui.activate()


if __name__ == "__main__":
    curses.wrapper(main)
