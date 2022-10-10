from asyncore import read
import imp
from django.contrib import auth
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from main.models import *
from django.http import Http404
# Create your views here.


class GetNovelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Novel
        fields = ['id', 'name', 'img',
                  'novel_type', 'date', 'lang', 'author']


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapters
        fields = ['id', 'title', 'chapter', 'date']


class ColSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    def get_chapters(self, obj):
        query = Chapters.objects.filter(
            col__id=obj.id)
        serializer = ChapterSerializer(query, many=True)

        return serializer.data

    class Meta:
        model = ColNovel
        fields = ['id', 'title', 'chapters']


class SnippetSerializer(serializers.ModelSerializer):
    # chapters = Chapter.objects.
    cols = serializers.SerializerMethodField()

    def get_cols(self, obj):
        customer_account_query = ColNovel.objects.filter(
            novel__id=obj.id)
        serializer = ColSerializer(customer_account_query, many=True)

        return serializer.data

    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Novel
        fields = ['genres', 'story', 'cols']


@api_view(['GET', 'POST'])
def get_novels(request):
    serializer = GetNovelsSerializer(Novel.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_novel(request, pk):
    try:
        novel = Novel.objects.get(pk=pk)
    except:
        raise Http404()

    serializer = SnippetSerializer(novel, many=False)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_content(request, pk):

    try:
        chapter = Chapters.objects.get(pk=pk)
    except:
        raise Http404()

    return Response({'content': chapter.content.split('--split--')})


@api_view(['GET', 'POST'])
def get_last_chapters(request):
    data = []
    novels = Novel.objects.all()
    for novel in novels:
        last_col = ColNovel.objects.filter(novel=novel).latest('publish_date')
        last = Chapters.objects.filter(col=last_col).latest('id')
        data.append({
            'name': novel.name,
            'id': novel.id,
            'link': novel.link,
            'last_chapter': {
                'id': last.id,
                'chapter': last.chapter,
                'title': last.title,
            },
            'last_col': {
                'id': last_col.id,
                'title': last_col.title,
            }})
    return Response(data)


@api_view(['GET', 'POST'])
def add_chapters(request):
    #  Initial the variables
    nvs = Novel.objects.all()
    novels = {}
    for nv in nvs:
        novels[f'{nv.id} : {nv.name}'] = nv

    ln = len(request.data)
    for index in range(ln):
        pk = f"{request.data[index]['id']} : {request.data[index]['name']}"
        ln_cols = len(request.data[index]['cols'])
        cls = ColNovel.objects.filter(novel=novels[pk])
        cols = {}
        for cl in cls:
            cols[cl.title] = cl

        for index_col in range(ln_cols):
            if request.data[index]['cols'][index_col]['title'] in cols:
                col = cols[request.data[index]['cols'][index_col]['title']]
            else:
                col = ColNovel(
                    title=request.data[index]['cols'][index_col]['title'], novel=novels[pk])
                col.save()
                cols[col.title] = col

            ln_chapters = len(
                request.data[index]['cols'][index_col]['chapters'])
            for index_chapter in range(ln_chapters):
                if not (Chapters.objects.filter(
                    title=request.data[index]['cols'][index_col]['chapters'][index_chapter]['title'],
                    date=request.data[index]['cols'][index_col]['chapters'][index_chapter]['date'],
                    chapter=request.data[index]['cols'][index_col]['chapters'][index_chapter]['chapter']
                ).exists()):

                    chapter = Chapters(
                        title=request.data[index]['cols'][index_col]['chapters'][index_chapter]['title'],
                        date=request.data[index]['cols'][index_col]['chapters'][index_chapter]['date'],
                        chapter=request.data[index]['cols'][index_col]['chapters'][index_chapter]['chapter'],
                        col=col,
                        content=request.data[index]['cols'][index_col]['chapters'][index_chapter]['prgs']
                    )
                    chapter.save()

    return Response({'data': request.data})
