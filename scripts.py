import argparse
import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

COMMENDATION_TEXT = ('Молодец!', 'Хвалю!', 'Отлично!', 'Прекрасно!', 'Хорошо!')


def fix_marks(kid_name):
    schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    schoolkid_bad_grades = Mark.objects.filter(
            schoolkid=schoolkid,
            points__in=[2, 3]
    )
    for grade in schoolkid_bad_grades:
        grade.points = 5
        grade.save()


def remove_chastisements(kid_name):
    schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    schoolkid_chastiments = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastiments.delete()


def create_commendation(kid_name, subject_title):
    schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject_title
    ).order_by('date').first()
    Commendation.objects.create(
            text=random.choice(COMMENDATION_TEXT),
            created=lesson.date, schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('function')
    parser.add_argument('name')
    parser.add_argument('subject')
    args = parser.parse_args()
    if args.function == 'marks' and args.name:
        fix_marks(args.name)
    elif args.function == 'chastisements' and args.name:
        remove_chastisements(args.name)
    elif args.function == 'commendation' and args.name and args.subject:
        create_commendation(args.name, args.subject)
    else:
        print('Введите правильные аргументы')


if __name__ == '__main__':
    main()