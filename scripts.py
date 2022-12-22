import argparse
import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

COMMENDATION_TEXT = ('Молодец!', 'Хвалю!', 'Отлично!', 'Прекрасно!', 'Хорошо!')


def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
        return schoolkid
    except MultipleObjectsReturned:
        print('Найдено несколько учеников, введите точное ФИО')
    except DoesNotExist:
        print('Ученик не найден, введите верное имя')


def fix_marks(kid_name):
    schoolkid = get_schoolkid(kid_name)
    if schoolkid:
        Mark.objects.filter(
                schoolkid=schoolkid,
                points__in=[2, 3]
        ).update(points=5)


def remove_chastisements(kid_name):
    schoolkid = get_schoolkid(kid_name)
    if schoolkid:
        schoolkid_chastiments = Chastisement.objects.filter(
                schoolkid=schoolkid
        )
        schoolkid_chastiments.delete()


def create_commendation(kid_name, subject_title):
    schoolkid = get_schoolkid(kid_name)
    if schoolkid:
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
