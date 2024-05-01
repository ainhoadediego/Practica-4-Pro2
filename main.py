# Lucía Vega Navarrete. lucia.vega.navarrete@udc.es
# Ainhoa de Diego Silva. ainhoa.dediego.silva@udc.es

from course import Course
from paquete.avl_tree import AVL
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
        academy = AVL() # Creates an empty AVL tree 
        
        for line in lines[1:]: # The first line does not contain valid data.
            parts = line.split(",") 
            name = parts[0]
            duration = int(parts[1])
            n_students = int(parts[2])
            level = parts[3]
            language = parts[4]
            price = float(parts[5])

            # Instantiates a course object with the read data and adds it to the AVL
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
        Returns None if the file could not be read.
    """

    file_name = name + ".txt"
    try:
        with open(file_name) as f:
            courses_text = f.read()
            simulator = CourseSimulator()
            academy = simulator.parse_file(courses_text)
    except: # An error may occur if the name given does not correspond to any file in the current directory
        print("The file could not be read.\n")
        return None
    else:
        f.close()
        print("File read succesfully.\n")
        return academy
    
def file_input(file_number: str):
    """Reads the file after requesting the name and creates a tree from it.

    If the given name does not correspond to any file, returns None.

    Parameters
    ----------
    file_number: str
        To know if the file being read is the first or the second one.

    Returns
    -------
    academy: str
        Tree created from the file.
        Returns None if the file could not be read.
    """
    f_name = input(f"Enter the name of the {file_number} file you want to read (without the '.txt' extension): ")
    print()
    academy = read_file(f_name)
    return academy

def file(file_number: str):
    """Request an input for the name of the file until it is read correctly.

    Parameters
    ----------
    file_number: str
        To know if the file being read is the first or the second one.

    Returns
    -------
    academy: str
        Tree created from the file.
    """
    academy = file_input(file_number)
    while academy == None:
        academy = file_input(file_number)
    return academy
    
def search(tree: AVL, position, key):
    """Performs the search of a key in a tree.

    Parameters
    ----------
    tree: AVL
        Given binary search tree.

    position: Position(PositionalBinaryTree.Position)
        Position to start the search from.

    key: str
        Key that is wished to be found.

    Returns
    -------
    position: Position(PositionalBinaryTree.Position)
        Returns the position corresponding to the key value.
        If the key is not found, returns None.
    """
    if position is None: # Has reached a leaf node and has not found the key
        return None
    elif key == position.key(): # The key is in the root node
        return position
    elif key < position.key(): # If the key is lower, looks in the left
        return search(tree, tree.left(position), key)
    else: # If the key is greater, searches in the right
        return search(tree, tree.right(position), key)

def common_course(tree_A: AVL, tree_B: AVL, key_A, key_B):
    """Combines two identical courses in one course.
    
    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing course A.

    tree_B: AVL(BST)
        Tree representing course B.

    key_A: 
        Key for course A.

    key_B: 
        Key for course B.

    Returns
    -------
    new_course: Course()

    Creates a new course from the most profitable one by combining the students.
    Precondition: the same course is in both trees."""

    course_A = tree_A[key_A] # Returns a course object
    course_B = tree_B[key_B] 
    # The number of students is added
    n_students = course_A.number_students + course_B.number_students
    # Checks which course is more profitable.
    # Creates a new course object based on the most (or equally) profitable
    # with the new number of students so as not to modify the original 
    # courses if used in the statistics.
    if course_A.ge_benefit(course_B):
        new_course = Course(course_A.name, course_A.duration, n_students, course_A.level, course_A.language, course_A.price)
    else: 
        new_course = Course(course_B.name, course_B.duration, n_students, course_B.level, course_B.language, course_B.price)
    return new_course

def common_offer(tree_A: AVL, tree_B: AVL) -> AVL:
    """Creates a common tree with the courses present in both academies (tree_A and tree_B).
    
    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing academy A.

    tree_B: AVL(BST)
        Tree representing academy B.

    Returns
    -------
    common_tree: AVL(BST)

    Creates a tree for a new academy C (that includes courses from A and B) representing the 
    'common offer', adding only the common courses between A and B."""

    common_tree = AVL() # Creates an empty tree (equivalent to academy C)
    for key_A in iter(tree_A): # Go through the courses of academy A
        # Since we have used a name_level_language type key, 
        # the same course in 2 trees will have the same key 
        # and we can do an efficient search in the other tree.
        aux = search(tree_B, tree_B.root(), key_A) # look for the same course at Academy B
        # aux is the position where the course is
        # If aux is None it has not been found, if not it is in the root
        if aux is not None:
            new_course = common_course(tree_A, tree_B, key_A, aux.key())
            common_tree[new_course.label()] = new_course
    # It is not necessary to go through the courses of academy B 
    return common_tree

def add_courses(tree_A: AVL, tree_B: AVL, tree_C: AVL, key_A: str, academy_name: str):
    """
    Searches a course from tree_A with 'key_A' as key in tree_B and adds it to tree_C.
    
    In case a course with the same name (but not language and level) is found,
    a new course based on it is created with the name of the company added to its own.

    In other case, the course is added to tree_C without modifications. 

    tree_A: AVL(BST)
        Tree representing academy A.
        Tree whose course will be compared.

    tree_B: AVL(BST)
        Tree representing academy B.
        Tree whose courses will be iterated in order to find a course with the same 
        name as the course in tree_A.

    tree_C: AVL(BST)
        Tree representing academy C in which the courses will be added.

    key_A: str
        Key corresponding to the course in tree_A that will be searched in tree_B and
        added to tree_C.

    academy_name: str
        Name of the academy that tree_A represents.

    Returns
    -------
    None.

    Precondition: course corresponding to key_A in tree_A does not exist in tree_B
    """
    existing_course = False # To know if a course with the same name has been found.
    # existing_course will remain as False if it has not been found when the loop ends.
    for key_B in iter(tree_B): # All courses of academy B
        # If they have the same name but are not the same course
        if (tree_A[key_A].name == tree_B[key_B].name[:len(tree_A[key_A].name)]) and not (tree_A[key_A] == tree_B[key_B]):
            existing_course = True
            course_A = tree_A[key_A]
            new_course = Course(course_A.name + " " + academy_name, course_A.duration, course_A.number_students, course_A.level, course_A.language, course_A.price)
            tree_C[new_course.label()] = new_course
    if not existing_course: # The course is not in tree_B
        tree_C[key_A] = tree_A[key_A]

def added_offer(tree_A: AVL, tree_B: AVL, academy_names: tuple) -> AVL:
    """Creates an 'added_tree' with the courses of both academies.

    In case of equal courses, the course with the greatest benefit is selected. 
    The number of students is added in the merged course.

    In case of the same course names, add the name of the company.

    In other case, the course is added to the tree without modifications. 

    Parameters
    ----------
    tree_A: AVL(BST)
        Tree representing academy A.

    tree_B: AVL(BST)
        Tree representing academy B.

    academy_names: tuple
        Tuple of two strings that represent the names of tree_A and tree_B.

    Returns
    -------
    added_tree: AVL(BST)

    Creates a tree for a new academy C (that includes A and B) representing the 
    courses of both academies.
    """
    added_tree = AVL() # Creates an empty tree (equivalent to academy C)
    for key_A in iter(tree_A): # Go through the courses of academy A
        # If an equal course is found, the most profitable is added       
        aux = search(tree_B, tree_B.root(), key_A)
        if aux is not None: # aux is different from none if it has been found
            new_course = common_course(tree_A, tree_B, key_A, aux.key())
            added_tree[new_course.label()] = new_course
        else: # Adds courses with same name and courses that are not in tree B
            add_courses(tree_A, tree_B, added_tree, key_A, academy_names[0])
    
    for key_B in iter(tree_B): # Go through the courses of academy B
        # Look for an equal course in added_tree
        # If found, it already exists so nothing is done
        aux = search(added_tree, added_tree.root(), key_B)
        if aux is None: # Adds courses with same name and courses that are not in tree C
            add_courses(tree_B, added_tree, added_tree, key_B, academy_names[1])
        
    return added_tree

def show_courses(tree: AVL):
    """Displays the courses stored in 'tree'.

    Parameters
    ----------
    tree: AVL(BST)
        Tree in which the courses are stored.

    Returns
    -------
    None.
    """
    print("-"*63)
    print("Key, name, duration, number of students, level, language, price")
    print("-"*63)
    for course_key in iter(tree):
        print(f"{course_key}, {tree[course_key]}")
    print()

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
        print("Not valid.\n")
        n = input("Select an option [0-4]:")
        print()
    return n

def show_data(data, group_column: str, target_column: str, academy_name: str):
    """Shows a statistics table that informs of the mean of 'target_variable' grouped by 'group_column'.
    
    Parameters
    ----------
    data: DataFrame

    group_column: str
        Parameter the data will be grouped by.
        Identifies a constant variable. 
        
    target_column: str
        Target variable.
    
    academy_name: str
        Name of the academy the data belongs to.
    
    Returns
    -------
    None.
    """
    data = data.groupby(group_column).agg({target_column:["mean"]})
    print ("-"*63)
    print (f" {target_column} grouped by {group_column} ({academy_name})")
    print ("-"*63, "\n")
    print (data, "\n")
            
def tree_data(tree: AVL, column_1: str, column_2: str, column_3: str):
    """Stores the courses' data of a given tree in a DataFrame.
    
    Parameters
    ----------
    tree: AVL
        An AVL tree which data will be stored in a DataFrame.

    column_1: str
        Header of the column corresponding to the data stored in the first position of 'info_list'.
        It will represent the 'language' atribute of each course of the tree.

    column_2: str
        Header of the column corresponding to the data stored in the second position of 'info_list'.
        It will represent the 'number_students' atribute of each course of the tree.

    column_3: str
        Header of the column corresponding to the data stored in the third position of 'info_list'.
        It will represent the 'level' atribute of each course of the tree.

    Returns
    -------
    data: DataFrame
        DataFrame organising the given data of the simulation.
    """
    info_list = [] # list in which the information will be stored
    for key in iter(tree):
        info_list.append([tree[key].language, tree[key].number_students, tree[key].level])
    
    # create a dataframe from the pandas library
    data = pandas.DataFrame(info_list, columns=[column_1, column_2, column_3])
    return data

def total_benefit(tree: AVL, tree_name: str):
    """Stores the benefit of each course of 'tree' in a pandas Series and
    calculates the total income of the academy that the tree represents.
    
    Parameters
    ----------
    tree: AVL(BST)
        Tree which total income will be calculated.

    tree_name: str
        Name of the academy that the tree represents. 

    Returns
    -------
    None.
    """
    benefits = []
    for key in iter(tree):
        benefits.append(tree[key].benefit)
    # creates a series from the pandas library
    s = pandas.Series(benefits, dtype='float')
    print(f"{tree_name}: {s.sum()} € \n")
    
def main():

    OPTIONS = ("0", "1", "2", "3", "4")
    MAIN_MENU_OP = ("Exit.","Read course files A and B and insert them into AVL trees.",
                    "Show 'added offer'.", "Show 'common offer'.",
                    "Display metrics about the trees (metric of choice by the user).")
    SIDE_MENU_OP = ("Return to the main menu.", "Average number of students per language.",
                    "Average number of students per level.", "Total possible income.")
    ACADEMIES = ("Academy A", "Academy B", "Added offer", "Common offer")
    LANGUAGE = "Language"
    STUDENTS = "Number of students"
    LEVEL = "Level"

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
            academy_a = file("first")
            academy_b = file("second")
            # reinicia los árboles añadido y común para los nuevos archivos
            added_tree = common_tree = None
            trees_data = [] # reinicia los datos

        elif main_op == OPTIONS[2]: # Realizar la operación “oferta agregada” y visualizar el resultado
            print(f"You selected:{MAIN_MENU_OP[2]}\n")
            added_tree = added_offer(academy_a, academy_b, ACADEMIES[:2]) # The first 2 elements of the tuple are the names of academies A and B
            print(f"Added offer of {ACADEMIES[0]} and {ACADEMIES[1]}: \n") # Added offer of Academy A and Academy B
            show_courses(added_tree)

        elif main_op == OPTIONS[3]: # Realizar la operación “oferta común” y visualizar el resultado.
            print(f"You selected: {MAIN_MENU_OP[3]}\n")
            common_tree = common_offer(academy_a, academy_b)
            print(f"Common offer of {ACADEMIES[0]} and {ACADEMIES[1]}:: \n") # Common offer of Academy A and Academy B
            show_courses(common_tree)

        else: # Display metrics about the trees (metric of choice by the user).
            print(f"You selected: {MAIN_MENU_OP[4]}\n")

            show_menu(OPTIONS[:4], SIDE_MENU_OP) 
            side_op = select_option(OPTIONS[:4]) 

            if side_op == OPTIONS[0]: # Return to the main menu.
                print(f"You selected: {SIDE_MENU_OP[0]}\n")
            # Since we show statistics of the 4 trees, the user must have created
            # added_tree and common_tree before showing the stats
            elif added_tree == None or common_tree == None: 
                print(f"Options 2 and 3 ({ACADEMIES[2]} and {ACADEMIES[3]}) must be selected before showing any data.\n")
            else:
                # tree_data list resets every time new files are read
                if len(trees_data) == 0: # If it has not already been created with these files
                    trees = (academy_a, academy_b, added_tree, common_tree)
                    for tree in trees:
                        trees_data.append(tree_data(tree, LANGUAGE, STUDENTS, LEVEL)) 

                if side_op == OPTIONS[1]: # Average number of students per language.
                    print(f"You selected: {SIDE_MENU_OP[1]}\n")
                    for i in range(len(ACADEMIES)):
                        show_data(trees_data[i], LANGUAGE, STUDENTS, ACADEMIES[i])

                elif side_op == OPTIONS[2]: # Average number of students per level.
                    print(f"You selected: {SIDE_MENU_OP[2]}\n")
                    for i in range(len(ACADEMIES)):
                        show_data(trees_data[i], LEVEL, STUDENTS, ACADEMIES[i])

                else: # Ingresos totales posibles.
                    print(f"You selected: {SIDE_MENU_OP[3]}\n")
                    
                    print ("-"*63)
                    print (f"Total income grouped by tree.")
                    print ("-"*63, "\n")
                    for i in range(len(ACADEMIES)):
                        total_benefit(trees[i], ACADEMIES[i])

        show_menu(OPTIONS, MAIN_MENU_OP)
        main_op = select_option(OPTIONS)

    print(f"You selected: {MAIN_MENU_OP[0]}")
    
if __name__ == "__main__":
    main()
