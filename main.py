# Lucía Vega Navarrete. lucia.vega.navarrete@udc.es
# Ainhoa de Diego Silva. ainhoa.dediego.silva@udc.es

#from .paquete import * (???)
from course import Course
from avl_tree import AVL
import pandas

class CourseSimulator:
    """Class that prepares the environment for handling Course objects.

    It is responsible for dividing the given files into Course class objects with their respective parameters.

    Attributes
    ----------
    None.

    Methods
    -------
    parse_file(text):
        Splits each line of the file (text) and separates it into parameters separated by the "," character.
    """

    def parse_file(self, text: str):
        """Divides the given text into parameters of a Course object.

        Parameters
        ----------
        text: str
            Each line of the given file.

        Returns
        -------
        academy: AVL
            It is an AVL tree that stores each course with its specific characteristics.
        """

        lines = text.split("\n") 
        # Creates an empty AVL tree 
        academy = AVL()
        
        for line in lines[1:]:
            parts = line.split(",") 
            name = parts[0]
            duration = int(parts[1])
            n_students = int(parts[2])
            level = parts[3]
            language = parts[4]
            price = float(parts[5])

            # instantiates a course object with the read data and adds it to the AVL
            course = Course(name, duration, n_students, level, language, price)
            academy[course.label()] = course

        return academy
    
def read_file(name):
    """Reads the given file.

    Parameters
    ----------
    name: str
        Name of the file to read.

    Returns
    -------
    academy: AVL
        It is an AVL tree that stores each course with its specific characteristics.
    """

    file_name = name + ".txt"
    try:
        with open(file_name) as f:
            courses_text = f.read()
            simulator = CourseSimulator()
            academy = simulator.parse_file(courses_text)
    except: # An error may occur if the name given does not correspond to any file in the current directory
        print("The file could not be read.")
    else:
        f.close()
        print("File read succesfully.\n")
        return academy
    
def preorder_indent_BST(T, p, d):
    """Returns the graphical representation of the preorder (root, left, right) traversal of the tree T.

    Parameters
    ----------
    T: AVL(BST)
        Given AVL binary search tree.

    p: Node(BST._Node)
        Starting node to begin the traversal.

    d: int
        Depth at which the current node is to begin the traversal.

    Returns
    -------
    str
        Prints the preorder representation of a binary subtree of T rooted at p at depth d.
        To print the entire tree, call preorder_indent_BST(aTree, aTree.root(), 0).
"""

    
    if p is not None:
        # use depth for indentation
        print(2*d*' ' + "(" + str(p.key()) + "; " +  str(p.value()) + ")") 
        preorder_indent_BST(T, T.left(p), d+1) # left child depth is d+1
        preorder_indent_BST(T, T.right(p), d+1) # right child depth is d+1

def search(tree, position, key):
    """Performs the search in a tree.

    Parameters
    ----------
    tree: Tree()
        Given binary search tree.

    position: Position(PositionalBinaryTree.Position)
        Position to start the search from.

    key: 
        Key-value pair.

    Returns
    -------
    str
        Returns the position corresponding to the key value.
        If not found, returns None.
"""


    if position is None: # has reached a leaf
        return None
    elif key == position.key(): # the key is in the root
        return position
    elif key < position.key(): # if the key is smaller, search to the left
        return search(tree, tree.left(position), key)
    else: # if the key is greater, search to the right
        return search(tree, tree.right(position), key)

def common_course(tree_A: AVL, tree_B: AVL, key_A, key_B):
    """Combines two identical courses in two course trees.
    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing course A.

    tree_B: AVL(BST)
        Tree representing course B.

    key_A: 
        Key-value pair for course A.

    key_B: 
        Key-value pair for course B.

    Returns
    -------
    new_course: Course()

    Creates a new course from the most profitable one by combining the students.
    Precondition: the same course is in both trees."""

    course_A = tree_A[key_A] # returns a course object
    course_B = tree_B[key_B] # returns a course object
    # the number of students is added
    n_students = course_A.number_students + course_B.number_students
    # checks which course is more profitable
    #adds it if it is more profitable or equally profitable
    if course_A.g_benefit(course_B) or course_A.eq_benefit(course_B):
        new_course = Course(course_A.name, course_A.duration, n_students, course_A.level, course_A.language, course_A.price)
    else: 
        new_course = Course(course_B.name, course_B.duration, n_students, course_B.level, course_B.language, course_B.price)
    return new_course

def common_offer(tree_A: AVL, tree_B: AVL) -> AVL:
    """Creates a common tree with the trees of both academies.
    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing course A.

    tree_B: AVL(BST)
        Tree representing course B.

    Returns
    -------
    common_tree: AVL(BST)

    Creates a tree for a new academy C (that includes A and B) representing the 
    courses of both academies, adding only the common activities of A and B."""

    common_tree = AVL() # creates an empty tree (equivalent to academy C)
    for key_A in iter(tree_A): # iterates over the courses of academy A
        aux = search(tree_B, tree_B.root(), key_A) # searches for a matching course in academy B.
        # aux is the position where it is
        #aux is None if not found, otherwise, it is at the root
        if aux is not None:
            new_course = common_course(tree_A, tree_B, key_A, aux.key())
            common_tree[new_course.label()] = new_course
    return common_tree

def added_offer(tree_A: AVL, tree_B: AVL) -> AVL:
    """Creates a common tree with the trees of both academies
    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing course A.

    tree_B: AVL(BST)
        Tree representing course B.

    Returns
    -------
    added_tree: AVL(BST)

    Creates a tree for a new academy C (that includes A and B) representing the 
    courses of both academies.

    """
    added_tree = AVL() # creates an empty tree (equivalent to academy C)
    for key_A in iter(tree_A): # iterates over the courses of academy B
        # if it finds a matching course, adds the more profitable one
        aux = search(tree_B, tree_B.root(), key_A)
        if aux is not None: 
            new_course = common_course(tree_A, tree_B, key_A, aux.key())
            added_tree[new_course.label()] = new_course
        else: # if it doesn't find a matching cours
            for key_B in iter(tree_B): # iterates over the courses of academy B
                # if they have the same name but are not identical
                if (tree_A[key_A].name == tree_B[key_B].name) and not (tree_A[key_A] == tree_B[key_B]):
                    course_A, course_B = tree_A[key_A], tree_B[key_B]
                    new_course = Course(course_A.name + " Academia A", course_A.duration, course_A.number_students, course_A.level, course_A.language, course_A.price)
                    new_course_2 = Course(course_B.name + " Academia B", course_B.duration, course_B.number_students, course_B.level, course_B.language, course_B.price)
                    added_tree[new_course.label()] = new_course
                    added_tree[new_course_2.label()] = new_course_2
        
    return added_tree

def show_menu(OPTIONS: tuple, MENU_OP: tuple):
    """Displays the main menu.

    Parameters
    ----------
    OPTIONS: tuple
        A tuple of constants to indicate which number corresponds to each option
        for the program to execute correctly.

    MENU_OP: tuple
        A tuple of constants to indicate which option corresponds to each number
        for the program to execute correctly.

    Returns
    -------
    None.

    Precondition: OPTIONS and MENU_OP must have the same length.
    """

    for i in range(len(OPTIONS)):
        print(f"{OPTIONS[i]} – {MENU_OP[i]}")
    print("\n")

def select_option(OPTIONS: list) -> int:
    """Requests a number from those shown in the menu.
    If the number is not in the range [0, 4], the input is requested again until it is valid.

    Parameters
    ----------
    OPTIONS: tuple
        Tuple containing the valid inputs.

    Returns
    -------
    n: str
        Option chosen by the user.
    """
    
    n = input(f"Select an option [{OPTIONS[0]}-{OPTIONS[-1]}]: ")
    print()
    while n not in OPTIONS: # requests data again until the input is valid
        print("Not valid.")
        n = input("Select an option [0-4]:")
        print()
    return n

def create_data(info_list, column_1: str, column_2: str):
    """Stores the given data of the simulation in a DataFrames.
    
    Parameters
    ----------
    info_list: list
        A list of two elements with relevant information about the simulation.

    column_1: str
        Header of the column corresponding to the data stored in the first position of 'info_list'.

    column_2: str
        Header of the column corresponding to the data stored in the second position of 'info_list'.

    Returns
    -------
    data: DataFrame
        DataFrame organising the given data of the simulation.
    """

    data = pandas.DataFrame(info_list, columns=[column_1,column_2])
    return data

def show_data(data, group_column: str, target_column: str):
    """Shows a statistics table that informs of the mean of 'target_variable' grouped by 'group_column'.
    
    Parameters
    ----------
    data: DataFrame

    group_column: str
        Parameter the data will be grouped by.
        Identifies a constant variable. 
        
    target_column: str
        Target variable.
    
    Returns
    -------
    None.
    """
    data = data.groupby(group_column).agg({target_column:["mean"]})
    print ("#############################################")
    print (f" {target_column} grouped by {group_column} ")
    print ("#############################################\n")
    print (data, "\n")
            
def main():

    OPTIONS = ("0", "1", "2", "3", "4")
    MAIN_MENU_OP = ("Exit.","Read course files A and B and insert them into AVL trees.",
                    "Show 'added offer'.", "Show 'common offer'.",
                    "Display metrics about the trees (metric of choice by the user).")
    SIDE_MENU_OP = ("Return to the main menu.", "Average number of students per language.",
                    "Average number of students per level.", "Total possible income.")

    show_menu(OPTIONS, MAIN_MENU_OP) # shows the main menu
    main_op = select_option(OPTIONS) # input

    # asks the user to select an option again until they choose '1: read files' or '0: exit'
    # as it is not possible to execute the remaining options without reading a file first
    while main_op != OPTIONS[1] and main_op != OPTIONS[0]:
        print("The files must be read before selecting another option.\n")
        show_menu(OPTIONS, MAIN_MENU_OP) 
        main_op = select_option(OPTIONS)

    while main_op !=OPTIONS[0 ]: # the loop finishes when the user presses 0
        
        if main_op == OPTIONS[1]: # Read two course files and store them in AVLs.
            print(f"You selected: {MAIN_MENU_OP[1]}\n")
            f_name = input("Enter the name of the first file you want to read (without the '.txt' extension): ")
            print()
            academy_a = read_file(f_name)
            f_name = input("Enter the name of the second file you want to read (without the '.txt' extension): ")
            print()
            academy_b = read_file(f_name)

        elif main_op == OPTIONS[2]: # Realizar la operación “oferta agregada” y visualizar el resultado
            print(f"You selected:{MAIN_MENU_OP[2]}\n")
            # COMPLETAR

        elif main_op == OPTIONS[3]: # Realizar la operación “oferta común” y visualizar el resultado.
            print(f"You selected: {MAIN_MENU_OP[3]}\n")

        else: # Display metrics about the trees (metric of choice by the user).
            print(f"You selected:{MAIN_MENU_OP[4]}\n")
            show_menu(OPTIONS[:3], SIDE_MENU_OP) 
            side_op = select_option(OPTIONS[:3]) 

            if side_op == OPTIONS[0]: # Return to the main menu.
                print(f"You selected: {SIDE_MENU_OP[0]}\n")
            else:

                if side_op == OPTIONS[1]: # Número medio de alumnos por idioma.
                    print(f"You selected: {SIDE_MENU_OP[1]}\n")

                elif side_op == OPTIONS[2]: # Número medio de alumnos por nivel.
                    print(f"You selected: {SIDE_MENU_OP[2]}\n")

                else: # Ingresos totales posibles.
                    print(f"You selected: {SIDE_MENU_OP[3]}\n")


        show_menu(OPTIONS, MAIN_MENU_OP)
        main_op = select_option(OPTIONS)

    print(f"You selected: {MAIN_MENU_OP[0]}")
    
if __name__ == "__main__":

    # pruebas
    
    a = read_file('ejA')
    b = read_file('ejB')
    preorder_indent_BST(a,a.root(),0)
    print()
    preorder_indent_BST(b,b.root(),0)
    print()
    position = a.find_position(a.root().key())

    c = common_offer(a, b)
    preorder_indent_BST(c,c.root(),0)
    print()
    d = added_offer(a, b)
    preorder_indent_BST(d,d.root(),0)