import json
from pydantic import BaseModel
import jellyfish


class Student(BaseModel):
    id: int
    seminar_group: str
    first_name: str = ""
    last_name: str = ""

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


students: list[Student] = []


def load():
    students.clear()

    with open("./data/students.json") as f:
        students_data = json.load(f)

    for data in students_data:
        student = Student.parse_obj(data)
        students.append(student)

    def sort_func(student: Student):
        return f"{student.first_name} {student.last_name}"

    students.sort(key=sort_func)


def search_name(name: str) -> list[Student]:
    distances: list[tuple[Student, int]] = []
    for student in students:
        distance = jellyfish.levenshtein_distance(student.name, name)
        distances.append((student, distance))

    sorted_distances = sorted(distances, key=lambda v: v[1])
    sorted_names = [student for student, _ in sorted_distances]
    return sorted_names


def from_id(id: int) -> Student | None:
    for student in students:
        if student.id == id:
            return student
    
    return None


try:
    load()
except Exception:
    raise FileNotFoundError(
        "Please place a valid student list at ./data/students.json\n"
        'Example File:\n'
        '[\n'
        '    {"id": 1234567, "seminar_group": "A", "first_name": "AAA", "last_name": "BBB" },\n'
        '    {"id": 7654321, "seminar_group": "B", "first_name": "CCC", "last_name": "DDD" }\n'
        ']\n'
    )