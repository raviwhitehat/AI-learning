import sys

def main():
    if len(sys.argv) != 2:
        raise Exception("No FIle Given")
    maze = Maze(sys.argv[1])
    maze.print_()
    print("Solving...")
    maze.solve()
    print(f"Number of State Explored = {maze.num_explored}")
    print("Solution :")
    maze.print_()
    
   


class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action
    

class StackFrontier():
    def __init__(self):
         self.frontier = []
    
    def add(self,node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Maze():

    def __init__(self,filename) :
        #read the file and set height and width of maze
        with open(filename) as f:
            contents  = f.read()

        #Validate Start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly only one starting point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly only one Ending point")
        
        #Detemine hight and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        #Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    
                    elif contents[i][j] == " ":
                        row.append(False)
                    
                    else:
                        row.append(True)

                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None



    def print_(self):
        solution =self.solution[1] if self.solution is not None else None
        print()
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("#",end="")
                elif (i,j) == self.start:
                    print("A",end="")
                elif (i,j) == self.goal:
                    print("B",end="")
                elif solution is not None and (i, j) in solution:
                    print(".", end="")
                else:
                    print(" ",end="")
                
            print()
        print()
        


    def neighbours(self,state):
        row,col = state


        #All Possible Actions
        
        candidates = [
            ("up",(row -1,col)),
            ("down",(row +1 ,col)),
            ('left',(row,col -1)),
            ("right",(row,col +1))
        ]
        #Ensure Actions are valid
        result = []
        for action,(r,c) in candidates:
            try :
                if not self.walls[r][c]:
                    result.append((action,(r,c)))
            
            except IndexError:
                continue

        return result


                
                            



        
    def solve(self):
        #Find a solution to maze if one exits
        
        #keep traks of number of states explored
        self.num_explored = 0

        #Intialize frontier to just the start position
        start = Node(state=self.start,parent=None,action=None)
        frontier = StackFrontier()
        frontier.add(start)

        #Intialize an empty explored set
        self.explored = set()

        #keep looping ubntil the solution founds
        while True:

            #if nothing lkeft in frontier then , there is n9o path
            if frontier.empty():
                raise Exception("no Solution")
            #choose a node fromhe frontier
            node = frontier.remove()
            self.num_explored += 1

            # if this is a goal then stop
            if node.state == self.goal:
                actions = []
                cells = []
                
                #folow the path to find the solution path cost
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            #Mark node as explored
            self.explored.add(node.state)
            
            #Add neighbours to the frontier
            for action,state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state,parent=node,action=action)
                    frontier.add(child)
    #this function not yet completed by me.
    # def output_image(self,filename,show_Solution=True,State_Explored=False):
    #     from PIL import Image, ImageDraw
    #     cell_size = 50
    #     cell_border = 2

    #     img = Image.new("RGBA",(self.width * cell_size,self.height * cell_border),"black")
    #     draw = ImageDraw.Draw(img)
    #     solution =self.solution[1] if self.solution is not None else None
    #     for i,row in enumerate(self.walls):
    #         for j,col in enumerate(row):

    #             if col:
    #                 #walls
    #                 fill = (40,40,40)
    #             elif(i,j) == self.start:
    #                # Start
    #                 fill = (255,0,0)
    #             elif (i,j) == self.goal:
    #                 #Goal
    #                 fill= (0,0,255)
    #             elif solution is not None and show_Solution and(i, j) in solution:
    #                 #Solution
    #                 fill = (220,235,113)
                
    #             elif solution is not None and self.explored and(i, j) in self.explored:
    #                 fill =(212, 97, 85)
                
    #             # Empty cell
    #             else:
    #                 (237, 240, 252)
    #                 fill =(237, 240, 252)
    #             draw.rectangle(
    #                 ([j*cell_size,i *cell_size,cell_border*j,cell_border*i]),
    #             ((j+1)*cell_size - cell_border*(i+1) * cell_size),
    #             fill =fill
    #             )
    #     img.save(filename)




if __name__ == "__main__":
    main()