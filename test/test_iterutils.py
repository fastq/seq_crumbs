# Copyright 2012 Jose Blanca, Peio Ziarsolo, COMAV-Univ. Politecnica Valencia
# This file is part of seq_crumbs.
# seq_crumbs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# seq_crumbs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR  PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with seq_crumbs. If not, see <http://www.gnu.org/licenses/>.

import unittest

from crumbs.iterutils import (sample, sample_2, length, group_in_packets,
                              rolling_window)

# pylint: disable=R0201
# pylint: disable=R0904


class IterutilsTest(unittest.TestCase):
    'It tests the iterator tools.'

    def check_sampled_items(self, items, sampled_items, num_sampled_items):
        'It checks that the sample is valid'
        assert len(sampled_items) == num_sampled_items

        # no repeated ones
        sampled_items = set(sampled_items)
        assert len(sampled_items) == num_sampled_items

        assert sampled_items.issubset(items)

    def test_sample(self):
        'We can sample an iterator'
        items = range(100)

        num_sampled_items = 10
        for num_sampled_items in (10, 90):
            sampled_items = list(sample(items, num_sampled_items))
            self.check_sampled_items(items, sampled_items, num_sampled_items)

    def test_sample_2(self):
        'We can sample an iterator'
        length_ = 100
        items = range(length_)

        num_sampled_items = 10
        for num_sampled_items in (10, 90):
            sampled_items = list(sample_2(items, length_, num_sampled_items))
            self.check_sampled_items(items, sampled_items, num_sampled_items)

    def test_length(self):
        'We can count an iterator'
        items = xrange(10)
        assert length(items) == 10

    def test_group_in_packets(self):
        'It groups an iterator in packets of items'
        packets = [packet for packet in  group_in_packets(range(4), 2)]
        assert packets == [[0, 1], [2, 3]]

        packets = [packet for packet in  group_in_packets(range(5), 2)]
        assert packets == [[0, 1], [2, 3], [4]]

        packets = [packet for packet in  group_in_packets([], 2)]
        assert packets == []

    def test_rolling_window(self):
        'We get the items along a rolling window'
        # with series
        serie = '12345'
        assert [''.join(win) for win in rolling_window(serie, 3)] == ['123',
                                                                  '234', '345']
        assert not [''.join(win) for win in rolling_window(serie, 6)]
        assert [''.join(w) for w in rolling_window(serie, 5)] == ['12345']

        # with iterator
        iterator = iter(serie)
        assert [''.join(win) for win in rolling_window(iterator, 3)] == ['123',
                                                                  '234', '345']
        iterator = iter(serie)
        assert not [''.join(win) for win in rolling_window(iterator, 6)]
        iterator = iter(serie)
        assert [''.join(w) for w in rolling_window(iterator, 5)] == ['12345']

        # with step
        series = ['1234567890', '123456789', '12345678', '1234567']
        expected = [['1234', '3456', '5678', '7890'], ['1234', '3456', '5678'],
                    ['1234', '3456', '5678'], ['1234', '3456']]
        for serie, exp in zip(series, expected):
            wins1 = [''.join(win) for win in rolling_window(serie, 4, 2)]
            assert wins1 == exp

            iterator = iter(serie)
            wins2 = [''.join(win) for win in rolling_window(iterator, 4, 2)]
            assert wins1 == wins2

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'IterutilsTest.test_group_in_packets']
    unittest.main()
