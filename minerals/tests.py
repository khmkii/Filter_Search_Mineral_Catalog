from django.core.urlresolvers import reverse
from django.test import TestCase

import random, string

from minerals import models
from minerals.templatetags import mineral_tags


class MineralsViewTests(TestCase):

    def setUp(self):
        self.mineral = models.Mineral.objects.create(
            name='unobtainium',
            formula='unknown',
            group='mystery',
            image_caption='difficult to find'
        )
        self.mineral2 = models.Mineral.objects.create(
            name='kryptonite',
            color='green',
            image_caption='not liked by Superman'
        )

    def test_home_view(self):
        home_url = reverse('minerals:home')
        resp = self.client.get(home_url, follow=True)
        self.assertIn(resp.status_code, [200, 302])
        self.assertTemplateUsed(resp, 'minerals/searched.html')

    def test_one_mineral_view(self):
        one_mineral_url = reverse(
            'minerals:see_mineral',
            kwargs={'pk': self.mineral.pk}
        )
        resp = self.client.get(one_mineral_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/mineral_detail.html')

    def test_one_mineral_fails_ok(self):
        failing_mieneral_url = reverse(
            'minerals:see_mineral',
            kwargs={'pk': 12}
        )
        resp = self.client.get(failing_mieneral_url)
        self.assertTrue(resp.status_code, 404)

    def test_random_mineral_view(self):
        random_url = reverse('minerals:random_mineral')
        resp = self.client.get(random_url, follow=True)
        self.assertIn(resp.status_code, [200, 302])
        self.assertTemplateUsed(resp, 'minerals/mineral_detail.html')

    def test_search_view_success(self):
        good_search_url = reverse('minerals:search') + '?q=kryptonite'
        resp = self.client.get(good_search_url)
        self.assertIn(resp.status_code, [302, 200])
        self.assertTemplateUsed(resp, 'minerals/searched.html')
        self.assertIn((self.mineral2.pk, self.mineral2.name), resp.context['search_results'])

    def test_search_view_failure(self):
        bad_search_url = reverse('minerals:search') + '?q=THis should not return anything'
        resp = self.client.get(bad_search_url, follow=True)
        self.assertIn(resp.status_code, [200, 302])
        self.assertTrue(resp.context['messages'])

    def test_letter_mineral_list(self):
        test_letter = random.choice([let for let in string.ascii_lowercase])
        letter_url = reverse(
            'minerals:first_letter',
            kwargs={'start_letter': test_letter}
        )
        resp = self.client.get(letter_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/searched.html')

    def test_streak_minerals_work(self):
        colors = mineral_tags.streak_nav()['streak_names']
        color = random.choice(colors)
        streak_url = reverse(
            'minerals:streaks',
            kwargs={'streak_color': color}
        )
        resp = self.client.get(streak_url)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/searched.html')

    def test_group_minerals_work(self):
        groups = mineral_tags.groups_nav()['group_names']
        group = random.choice(groups)
        streak_url = reverse(
            'minerals:groups',
            kwargs={'grouping': group}
        )
        resp = self.client.get(streak_url)
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'minerals/searched.html')
