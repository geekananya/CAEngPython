# multiple inheritance

class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

class Engineer(Person):
    def __init__(self, name, age, city, sub_dept):
        super().__init__(name, age, city)
        self.sub_dept = sub_dept

    def get_sub_dept(self):
        return self.sub_dept

    def __set_sub_dept(self, new_sub_dept):     # private member
        self.sub_dept = new_sub_dept

class Employee(Person):
    def __init__(self, name, age, city, id, salary, dept):
        super().__init__(name, age, city)
        self.id = id
        self.salary = salary
        self.dept = dept

class EngineeringManager(Engineer, Employee):
    def __init__(self, name, age, city, id, salary, dept, sub_dept, company):
        super().__init__(name, age, city, sub_dept)
        super().__init__(name, age, city, id, salary, dept)
        self.company = company

    def get_company(self):
        return self.company

    def set_company(self, new_company):
        self.company = new_company

    def get_details(self):
        return f"Name: {self.name}\nAge: {self.age}\nCity:{self.city}\nSalary:{self.salary}\nCompany:{self.company}"