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
        Language in which the class will be taught.

    price: float
        Price to be paid per hour and student.

    benefit: float
        Total income obtained by the course (price * duration * number_students).

    Methods
    -------
    @property
    name:
        Method that returns the course name.

    @property
    duration:
        Method that returns the course duration.

    @property
    number_students:
        Method that returns the number of students enrolled in the course.

    @property
    level:
        Method that returns the course level.

    @property
    language:
        Method that returns the language to be taught in the course.

    @property
    price:
        Method that returns the price to be paid per enrolled student.

    @property
    benefit:
        Method that returns the benefit obtained.

    __eq__(self, other_course: 'Course'):
        Method that returns a boolean value when comparing parameters (name, level, and language) to determine if they are equal.

    ge_benefit(self, other_course: 'Course'):
        Method that returns a boolean value when comparing if the current course provides greater or equeal benefit than other_course.

    label(self):
        Method that returns a string with the characteristics of the name, level, and language of the course.

    __str__(self):
        Method that returns all the characteristics of the Course object in question.
    """ 

    def __init__(self, name: str, duration: int, number_students: int, level: str, language: str, price: float):
        """Assigns the different attributes to the Course object.
 
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
        """       
        self._name = name
        self._duration = duration
        self._number_students = number_students
        self._level = level
        self._language = language
        self._price = price
        self._benefit = self._price * self._duration * self._number_students

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
        price: float
           Monetary value that each student should contribute according to the course.

        Given by default.
        """
        return self._price
    
    @property
    def benefit(self):
        """Returns what is stored in the variable self._benefit.

        Returns
        --------
        price: float
           Monetary value obtained by the course.
           It is calculated by price * duration * number_students

        Given by default.
        """
        return self._benefit
    
    def __eq__(self, other_course: 'Course'):
        """Method that returns a boolean value when comparing the current course with another.

        Returns
        --------
        bool

        Returns True if the parameters (name, level, and language) are the same in both courses.
        """
        return self._name == other_course.name and self._level == other_course.level and self._language == other_course.language
    
    def ge_benefit(self, other_course: 'Course'):
        """Method that returns a boolean value when comparing the benefits of the current course with another.

        Returns
        --------
        bool

        Returns True if the self course provides more or the same benefits than the other_course.
        """
        return self._benefit >= other_course.benefit
    
    def label(self):
        """Returns a string with information collected about the current course.

        Returns
        --------
        str
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
