from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from django.contrib import messages


import random

from . import models


def home(request):
    return HttpResponseRedirect(
        reverse(
            'minerals:first_letter',
            kwargs={'start_letter': 'A'}
        )
    )


def one_mineral(request, pk):
    try:
        show_mineral = models.Mineral.objects.values().get(pk=pk)
        basis_name = show_mineral['name']
        try:
            next_mineral = models.Mineral.objects.order_by('name').filter(name__gt=basis_name)[0]
        except IndexError:
            next_mineral = models.Mineral.objects.order_by('name').all()[0]
        try:
            previous_mineral = models.Mineral.objects.order_by('name').filter(name__lt=basis_name)[0]
        except IndexError:
            previous_mineral = models.Mineral.objects.order_by('-name').all()[0]
    except models.Mineral.DoesNotExist:
        raise Http404('Mineral Does Not Exist')
    return render(
        request=request,
        template_name='minerals/mineral_detail.html',
        context={
            'show_mineral': show_mineral,
            'next_mineral': next_mineral.pk,
            'previous_mineral': previous_mineral.pk,
        },
    )


def random_mineral(request):
    random_number = random.randint(1, models.Mineral.objects.count())
    return HttpResponseRedirect(
        reverse(
            'minerals:see_mineral',
            kwargs={
                'pk': random_number,
            }
        )
    )


def first_letter(request, start_letter):
    first_letter_minerals = models.Mineral.objects.filter(name__startswith=start_letter).values_list('pk', 'name')
    return render(
        request=request,
        template_name='minerals/searched.html',
        context={
            'search_results': first_letter_minerals,
            'page_title': start_letter
        }
    )


def group_minerals(request, grouping):
    mineral_group = models.Mineral.objects.filter(group__icontains=grouping).values_list('pk', 'name')
    return render(
        request=request,
        template_name='minerals/searched.html',
        context={
            'search_results': mineral_group,
            'page_title': grouping,
        }
    )


def streak_minerals(request, streak_color):
    streak_color_minerals = models.Mineral.objects.filter(streak__icontains=streak_color).values_list('pk', 'name')
    return render(
        request=request,
        template_name='minerals/searched.html',
        context={
            'search_results': streak_color_minerals,
            'page_title': streak_color
        }
    )


def search(request):
    term = request.GET.get('q')
    search_results = models.Mineral.objects.filter(name__icontains=term).values_list('pk', 'name')
    if search_results:
        return render(
            request=request,
            template_name='minerals/searched.html',
            context={
                'search_results': search_results,
                'page_title': 'Search Results'
            },
        )
    else:
        messages.add_message(
            request=request,
            level=messages.INFO,
            message='Could not find anything to match your search of "{}"...'.format(term),
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
