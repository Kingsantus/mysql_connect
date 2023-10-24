class Person():
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        print("All data is saved")

    def show_details(self):
        print("Personal details :")
        print("Name : ", self.name)
        print("Age : ", self.age)
        print("Gender : ", self.gender)


class Student(Person):
    def __init__(self, name, age, gender, yearofgrad):
        super().__init__(name, age, gender)
        self.yearofgrad = yearofgrad

    def show_grad_date(self):
        self.show_details()
        print("Year of Graduation : ", self.yearofgrad)


johann = Student('will burg', 21, 'male', 2025)

johann.show_grad_date ()