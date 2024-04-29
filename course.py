# Lucía Vega Navarrete. lucia.vega.navarrete@udc.es
# Ainhoa de Diego Silva. ainhoa.dediego.silva@udc.es

class Course:

    """Class that initializes the Course object. 
    
    Objects of this class represent courses of different languages and levels
stored with their data regarding type, duration, price, and number of enrolled students.

Attributes
----------
name: str
    Identifies a particular course object.
    Name used solely to identify the object, but there may be multiple courses with the same name.

duration: int
    Number of hours to complete the course.

number_students: int
    Number of students enrolled in the course.

level: str
    Language level to quantify the course material (A, B, C...).

language: str
    Language on which the class will be taught.

price: float
    Price to be paid per student.

Methods
-------
@property
name:
    Method that returns the course name.

@name.setter
name(self, value: str):
    Method that updates the course name, giving it a new one.

@property
duration:
    Method that returns the course duration.

@property
number_students:
    Method that returns the number of students enrolled in the course.

@number_students.setter
number_students(self, value:int):
    Method that updates the number of enrolled students, giving it a new value.

@property
level:
    Method that returns the course level.

@property
language:
    Method that returns the language to be taught in the course.

@property
price:
    Method that returns the price to be paid per enrolled student.

__eq__(self, other_course: 'Course'):
    Method that returns a boolean value when comparing parameters (name, level, and language) to determine if they are equal.

g_benefit(self, other_course: 'Course'):
    Method that returns a boolean value when comparing if the current course provides greater benefit than other_course.

eq_benefit(self, other_course: 'Course'):
    Method that returns a boolean value when comparing if the current course provides equal benefit to other_course.

label(self):
    Method that returns a string with the characteristics of the name, level, and language of the course.

__str__(self):
    Method that returns all the characteristics of the Course object in question.

    """ 
     
    def __init__(self, name: str, duration: int, number_students: int, level: str, language: str, price: float):
        '''Assigns the different attributes to the Course object.
 
            Parameters
            ----------
            name: str
                Identifies a particular course object.
                Name used solely to identify the object, but there may be multiple courses with the same name.

            duration: int
                Number of hours to complete the course.

            number_students: int
                Number of students enrolled in the course.

            level: str
                Language level to quantify the course material (A, B, C...).

            language: str
                Language on which the class will be taught.

            price: float
                Price to be paid per student.

            Returns
            -------
            None.
            '''


        self._name = name
        self._duration = duration
        self._number_students = number_students
        self._level = level
        self._language = language
        self._price = price

    @property
    def name(self):
       """Returns what is stored in the variable self._name.

        Returns
        --------
        name: str
           Identifying name of the course.

        Given by default.
        """

       return self._name
    
    @name.setter
    def name(self, value):
        """Modifies the value of what is stored in the variable self._name.

            Parameters
            ----------
            value: str
                New name to be set for the course.

            Returns
            --------
            None

            It changes when two courses have the same name, the company name is added.
            """

        self._name = str(value)
    
    @property
    def duration(self):
       """Returns what is stored in the variable self._duration.

        Returns
        --------
        duration: int
           Duration of the course (in hours).

        Given by default.
        """
       return self._duration
    
    @property
    def number_students(self):
        """Returns what is stored in the variable self._number_students.

        Returns
        --------
        number_students: int
           Value of the number of students enrolled in the course.

        Given by default.
        """

        return self._number_students
    
    @number_students.setter
    def number_students(self, value):
       """Modifies the value of what is stored in the variable self._number_students.

            Parameters
            ----------
            number_students: int
                Value of the number of students enrolled in the course.

            Returns
            --------
            None

            It changes when two courses are equal, so the students from both groups are added
            in the course with the highest profits.
        """

       if value >= 0:
            self._number_students = int(value)
       else:
            print("The number of students must be greater than 0.")
    
    @property
    def level(self):
        """Returns what is stored in the variable self._level.

        Returns
        --------
        level: str
           Level of the students enrolled in the course.

        Given by default.
        """

        return self._level

    @property
    def language(self):
        """Returns what is stored in the variable self._language.

        Returns
        --------
        language: str
           Language taught in the course.

        Given by default.
        """

        return self._language
    
    @property
    def price(self):
        """Returns what is stored in the variable self._price.

        Returns
        --------
        price: int
           Monetary value that each student should contribute according to the course.

        Given by default.
        """

        return self._price
    
    def __eq__(self, other_course: 'Course'):
        """Method that returns a boolean value when comparing the current course with another.

        Returns
        --------
        bool

        Returns True if the parameters (name, level, and language) are the same in both courses.
        """

        return self._name == other_course.name and self._level == other_course.level and self._language == other_course.language
    
    def g_benefit(self, other_course: 'Course'):
        """Method that returns a boolean value when comparing the benefits of the current course with another.

        Returns
        --------
        bool

       Returns True if the self course provides more benefits than the other_course.
       A course is more profitable than another if it generates more money:
       we calculate the price per hour and multiply it by the number of students.

       """

        return (self._price/self._duration * self._number_students) > (other_course.price/other_course.duration * other_course.number_students)
    
    def eq_benefit(self, other_course: 'Course'):
        """Method that returns a boolean value when comparing the current course with another.

        Returns
        --------
        bool

        Returns True if the self course provides the same benefits as the other_course.
        A course is as profitable as another if it generates the same amount of money:
        we calculate the price per hour and multiply it by the number of students.
        """
        return (self._price/self._duration * self._number_students) == (other_course.price/other_course.duration * other_course.number_students)
    
    def label(self):
        """Returns a string with information collected about the current course.

            Returns
            --------
            str:
                Returns the name, level, and language of the course in question.
            """

        return f'{self._name}_{self._level}_{self._language}'
    
    def __str__(self):
         """Returns a string with all the information gathered about the current course.

            Returns
            --------
            str:
                Returns all the information set about the course in question.
            """

         return f"{self._name}, {self._duration}, {self._number_students}, {self._level}, {self._language}, {self._price}"
    
    

