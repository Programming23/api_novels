from django.core.management.base import BaseCommand, CommandError
import requests
import json
import time
from django.conf import settings
import os
from main.models import *


class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        headers = {
            "Cookie": "_fbp=fb.1.1660480602612.1324652329; aiADB_PV=1; antihacker_cookie=%23Africa/Casablanca%23-60%23linux%20x86_64%23Linux%230%2Cfalse%2Cfalse%23Google%20Inc.%20%28Intel%20Open%20Source%20Technology%20Center%29%7EANGLE%20%28Intel%20Open%20Source%20Technology%20Center%2C%20Mesa%20DRI%20Intel%28R%29%20HD%20Graphics%205500%20%28Broadwell%20GT2%29%20%2C%20OpenGL%204.5%29; recaptcha_cookie=%23Africa/Casablanca%23-60%23linux%20x86_64%23Linux%230%2Cfalse%2Cfalse%23Google%20Inc.%20%28Intel%20Open%20Source%20Technology%20Center%29%7EANGLE%20%28Intel%20Open%20Source%20Technology%20Center%2C%20Mesa%20DRI%20Intel%28R%29%20HD%20Graphics%205500%20%28Broadwell%20GT2%29%20%2C%20OpenGL%204.5%29",
            "User-Agent": "Mozilla/5.0 (X11; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        path = os.path.join(settings.BASE_DIR, 'data-novels.json')

        file = open(path, 'r')
        data = json.load(file)
        print(len(data))

        for k in data[0]:
            print(k)
            if k == 'cols':
                for ki in data[0][k][0]:
                    print('    ' + ki)
                    if ki == 'chapters':
                        for ke in data[0][k][0][ki][0]:
                            print('        ' + ke)

        Novel.objects.all().delete()
        Genre.objects.all().delete()
        Chapters.objects.all().delete()
        ColNovel.objects.all().delete()

        pk = 1
        pk_col = 1
        pk_genre = 1
        pk_chapter = 1

        for novel in data:
            genres = novel['genres']

            link = novel['img']
            r = requests.get(link, headers=headers)
            print(r.status_code)
            name_img = novel['name'].replace(' ', '_')
            ex = link.split('.')[-1]
            img = open(f'photos/novels/{name_img}.{ex}', 'wb')
            img.write(r.content)
            img.close()

            nv = Novel(
                name=novel['name'],
                link=novel['link'],
                img=f'photos/novels/{name_img}.{ex}',
                story=novel['story'],
                novel_type=novel['type'],
                lang=novel['lang'],
                author=novel['author'],
                date=novel['date'],
                pk=pk
            )
            nv.save()
            pk += 1
            for genre in genres:
                g = Genre(name=genre, pk=pk_genre)
                g.save()
                pk_genre += 1
                nv.genres.add(g)

                nv.save()

            for col in novel['cols']:
                c = ColNovel(title=col['title'], novel=nv, pk=pk_col)
                c.save()
                pk_col += 1
                for chapter in col['chapters']:
                    ch = Chapters(
                        col=c,
                        title=chapter['title'],
                        date=chapter['date'],
                        chapter=chapter['chapter'],
                        content=chapter['prgs'],
                        pk=pk_chapter
                    )
                    ch.save()
                    pk_chapter += 1

                print(f'finish col of {col["title"]}')

        file.close()

        self.stdout.write('Deleted objects older than 10 days')
