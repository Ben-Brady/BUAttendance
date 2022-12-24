from modules import students
import pytest


def test_From_name():
    all_students = students.search_name("ben bra")
    assert all_students[0].name == "Ben Brady"


def test_From_id():
    student = students.from_id(5524995)
    assert student
    assert student.name == "Ben Brady"
