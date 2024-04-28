class Course:

    def __init__(self, name: str, duration: int, number_students: int, level: str, language: str, price: float):
        self._name = name
        self._duration = duration
        self._number_students = number_students
        self._level = level
        self._language = language
        self._price = price

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value)
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def number_students(self):
        return self._number_students
    
    @number_students.setter
    def number_students(self, value):
        if value >= 0:
            self._number_students = int(value)
        else:
            print("The number of students must be greater than 0.")
    
    @property
    def level(self):
        return self._level

    @property
    def language(self):
        return self._language
    
    @property
    def price(self):
        return self._price
    
    def __eq__(self, other_course: 'Course'):
        return self._name == other_course.name and self._level == other_course.level and self._language == other_course.language
    
    def g_benefit(self, other_course: 'Course'):
        """Devuelve True si el curso self da más beneficios que el curso other_course.
        Un curso es más rentable que otro si da más dinero:
        calculamos el precio por hora y lo multiplicamos por el número de estudiantes.
        """
        return (self._price/self._duration * self._number_students) > (other_course.price/other_course.duration * other_course.number_students)
    
    def eq_benefit(self, other_course: 'Course'):
        """Devuelve True si el curso self da los mismos beneficios que el curso other_course.
        Un curso es más rentable que otro si da más dinero:
        calculamos el precio por hora y lo multiplicamos por el número de estudiantes.
        """
        return (self._price/self._duration * self._number_students) == (other_course.price/other_course.duration * other_course.number_students)
    
    def label(self):
        return f'{self._name}_{self._level}_{self._language}'
    
    def __str__(self):
        return f"{self._name}, {self._duration}, {self._number_students}, {self._level}, {self._language}, {self._price}"
    
    

