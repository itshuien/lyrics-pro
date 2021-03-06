from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Lyric, LyricNotation, PhoneticNotation
from .utils import words_tokenizer

import json

@login_required(login_url='/accounts/login/')
def index(request):
    lyrics = Lyric.objects.all().order_by('id') if request.user.is_superuser else Lyric.objects.filter(user=request.user.id)

    context = { 'lyrics': lyrics }

    return render(request, 'lyrics/index.html', context)

@login_required(login_url='/accounts/login/')
def show(request, pk):
    lyric = Lyric.objects.get(pk=pk)

    if not request.user.is_superuser and request.user != lyric.user:
        return HttpResponseRedirect(reverse('lyrics:index'))

    lyric_notations = lyric.lyricnotation_set.all()
    phonetic_notations = lyric.phoneticnotation_set.all()

    context = {
        'lyric': lyric,
        'lyric_lines': json.dumps(lyric.lines),
        'lyric_notations': json.dumps([record for record in lyric_notations.values()]),
        'tokenized_lyric_lines': [words_tokenizer(line) for line in lyric.lines],
        'phonetic_notations': json.dumps([record for record in phonetic_notations.values()]),
    }

    return render(request, 'lyrics/show.html', context)

def add_lyric_notation(request, lyric_id):
    lyric = Lyric.objects.get(pk=lyric_id)

    lyric_notation = LyricNotation(lyric=lyric,
                                    selected_text=request.POST['selected_text'],
                                    content=request.POST['content'],
                                    start_line=request.POST['start_line'],
                                    start_offset=request.POST['start_offset'],
                                    end_line=request.POST['end_line'],
                                    end_offset=request.POST['end_offset'])
    lyric_notation.save()

    return HttpResponseRedirect(reverse('lyrics:show', args=(lyric_id,)))

def update_lyric_notation(request, lyric_notation_id):
    lyric_notation = LyricNotation.objects.get(pk=lyric_notation_id)
    lyric_notation.content = request.POST['content']
    lyric_notation.save()

    return HttpResponseRedirect(reverse('lyrics:show', args=(lyric_notation.lyric_id,)))

def delete_lyric_notation(request, lyric_notation_id):
    lyric_notation = LyricNotation.objects.get(pk=lyric_notation_id)
    lyric_notation.delete()

    return HttpResponseRedirect(reverse('lyrics:show', args=(lyric_notation.lyric_id,)))

def create_phonetic_notation(request, lyric_id):
    lyric = Lyric.objects.get(pk=lyric_id)

    phonetic_notation = PhoneticNotation(lyric=lyric,
                                        selected_text=request.POST['selected_text'],
                                        content=request.POST['content'],
                                        line=request.POST['line'],
                                        offset=request.POST['offset'])
    phonetic_notation.save()

    return HttpResponseRedirect(reverse('lyrics:show', args=(lyric_id,)))

def update_phonetic_notation(request, phonetic_notation_id):
    phonetic_notation = PhoneticNotation.objects.get(pk=phonetic_notation_id)
    phonetic_notation.content = request.POST['content']
    phonetic_notation.save()

    return HttpResponseRedirect(reverse('lyrics:show', args=(phonetic_notation.lyric_id,)))

def delete_phonetic_notation(request, phonetic_notation_id):
    phonetic_notation = PhoneticNotation.objects.get(pk=phonetic_notation_id)
    phonetic_notation.delete()

    return HttpResponseRedirect(reverse('lyrics:show', args=(phonetic_notation.lyric_id,)))
