import random

from datacenter.models import Lesson, Mark, Commendation, Chastisement, Schoolkid


class IncorrectFullname(Exception):
    """Класс неправильного ввода имени ученика"""
    pass


class IncorrectSubject(Exception):
    """Класс неправильного ввода предмета"""
    pass


def fix_marks(fullname: str):
    """Исправляем плохие оценки определенного ученика на хорошие"""
    child = get_child_from_fullname(fullname)
    for mark in Mark.objects.filter(schoolkid=child, points__lt=4):
        points = [4, 5]
        mark.points = random.choice(points)
        mark.save()


def remove_chastisements(fullname: str):
    """Удаляем замечания определенного ученика"""
    child = get_child_from_fullname(fullname)
    all_schoolkid_chastisement = Chastisement.objects.filter(schoolkid=child)
    all_schoolkid_chastisement.delete()


def create_commendation(fullname: str, subject: str):
    """Создаем похввалу для определенного ученика по определенному предмету"""
    commendation_phrases = create_commendation_phrases()
    child = get_child_from_fullname(fullname)
    lesson = Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter,
                                   subject__title=subject).order_by('date').last()
    if lesson is None:
        raise IncorrectSubject(f"Неправильно указан предмет. Ваш ввод: {subject}") from None
    Commendation.objects.create(text=random.choice(commendation_phrases), created=lesson.date, schoolkid=child,
                                subject=lesson.subject, teacher=lesson.teacher)


def get_child_from_fullname(fullname: str):
    """Получаем экземпляр класса Schoolkid определенного ученика"""
    try:
        child = Schoolkid.objects.get(full_name__contains=fullname)
    except Schoolkid.DoesNotExist:
        raise IncorrectFullname(f"Неправильно указано имя. Ваш ввод: {fullname}") from None
    except Schoolkid.MultipleObjectsReturned:
        raise IncorrectFullname(f"Неправильно указано имя. Уточните фамилию имя и отчество.") from None
    return child


def create_commendation_phrases() -> list:
    """Получаем список фраз для похвалы"""
    commendations = []
    with open("Commendations.txt", "r") as commendations_file:
        for line in commendations_file:
            commendations.append(line.split(maxsplit=1)[1].strip())
    return commendations
