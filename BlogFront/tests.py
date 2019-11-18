from django.test import TestCase
import sys,os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blog.settings")
django.setup()
from BlogFront.models import NoteT, NoteName, NoteInfo


# notename = NoteName.objects.get(name="python")
# print(notename)
# b = notename.belong_name.all().values()
#
# print(notename.name, b)


# c = NoteName.objects.get(id=1)
# d = c.belong_name.values()
# print(d)
# a = NoteName.objects.all().values()
# for _ in a:
#     print(_, type(_))
a = NoteInfo.objects.filter(note_info_num='1515578081cyanzoy')
li = []
for _ in a:
    li.append([_.note_info_num, _.note_info_code])

print(li)

