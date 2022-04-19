import random

from datacenter.models import Lesson, Mark, Commendation, Chastisement, Schoolkid


def fix_marks(schoolkid):
    for mark in Mark.objects.filter(schoolkid=schoolkid, points__lt=4):
        points = [4, 5]
        mark.points = random.choice(points)
        mark.save()


def remove_chastisements(schoolkid):
    all_schoolkid_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    all_schoolkid_chastisement.delete()


def create_commendation(fullname, subject):
    commendation_phrases = create_commendation_phrases()
    child = Schoolkid.objects.get(full_name__contains=fullname)
    lesson = Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter,
                                   subject__title=subject).order_by('date').last()
    Commendation.objects.create(text=random.choice(commendation_phrases), created=lesson.date, schoolkid=child,
                                subject=lesson.subject, teacher=lesson.teacher)


def create_commendation_phrases() -> list:
    commendations = []
    with open("Commendations.txt", "r") as commendations_file:
        for line in commendations_file:
            commendations.append(line.split(maxsplit=1)[1].strip())
    return commendations
