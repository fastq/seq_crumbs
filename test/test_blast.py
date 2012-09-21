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
import os.path
from tempfile import NamedTemporaryFile

from crumbs.blast import get_blast_db, do_blast, BlastMatcher
from crumbs.utils.file_utils import TemporaryDir
from crumbs.settings import LINKERS, TITANIUM_LINKER
from crumbs.utils.test_utils import TEST_DATA_DIR

# pylint: disable=R0201
# pylint: disable=R0904


class BlastTest(unittest.TestCase):
    'It tests the blast infraestructure'

    def test_blastdb(self):
        'It creates a blast database.'
        db_name = 'arabidopsis_genes'
        seq_fpath = os.path.join(TEST_DATA_DIR, db_name)
        db_dir = TemporaryDir(prefix='blast_dbs_')
        try:
            db_path1 = get_blast_db(seq_fpath, directory=db_dir.name,
                                    dbtype='nucl')
            db_path = os.path.join(db_dir.name, db_name)
            assert 'CATAGGGTCACCAATGGC' in open(db_path1).read(100)
            assert db_path1 == db_path
            assert os.path.exists(db_path)
            index_fpath = os.path.join(db_dir.name, db_name + '.nsq')
            assert os.path.exists(index_fpath)

            db_path2 = get_blast_db(seq_fpath, directory=db_dir.name,
                                    dbtype='nucl')
            assert db_path1 == db_path2
        finally:
            db_dir.close()

    def test_blast_search(self):
        'It does a blast search'
        db_name = 'arabidopsis_genes'
        seq_fpath = os.path.join(TEST_DATA_DIR, db_name)
        db_dir = TemporaryDir(prefix='blast_dbs_')
        try:
            db_fpath = get_blast_db(seq_fpath, directory=db_dir.name,
                                    dbtype='nucl')
            query_fhand = NamedTemporaryFile()
            query_fhand.write(open(seq_fpath).read(200))
            query_fhand.flush()
            out_fhand = NamedTemporaryFile()
            do_blast(seq_fpath, db_fpath, program='blastn',
                     out_fpath=out_fhand.name)
            assert '</BlastOutput>' in open(out_fhand.name).read()
        finally:
            db_dir.close()


def create_a_matepair_file():
    'It creates a matepair fasta file'

    seq_5 = 'CTAGTCTAGTCGTAGTCATGGCTGTAGTCTAGTCTACGATTCGTATCAGTTGTGTGAC'
    seq_3 = 'ATCGATCATGTTGTATTGTGTACTATACACACACGTAGGTCGACTATCGTAGCTAGT'
    mate_seq = seq_5 + TITANIUM_LINKER + seq_3
    mate_fhand = NamedTemporaryFile(suffix='.fasta')
    mate_fhand.write('>seq1\n' + mate_seq + '\n')
    mate_fhand.flush()
    return mate_fhand


class BlastMater(unittest.TestCase):
    'It tests the splitting of mate pairs'
    def test_matching_segments(self):
        'It tests the detection of oligos in sequence files'
        seq_5 = 'CTAGTCTAGTCGTAGTCATGGCTGTAGTCTAGTCTACGATTCGTATCAGTTGTGTGAC'
        mate_fhand = create_a_matepair_file()

        expected_region = (len(seq_5), len(seq_5 + TITANIUM_LINKER) - 1)
        matcher = BlastMatcher(mate_fhand, LINKERS, program='blastn',
                               elongate_for_global=True)
        linker_region = matcher.get_matched_segments_for_read('seq1')[0]
        assert [expected_region] == linker_region

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'SffExtractTest.test_items_in_gff']
    unittest.main()
