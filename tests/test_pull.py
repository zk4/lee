
from lee.cli import Cli
from lee.enhancer import Enhancer
from lee import main,createParse
import os
import pytest
import shutil


@pytest.fixture
def parser():
    return  createParse()
       


def test_generate_source_md_html(parser):
    directory ="../leetcode_output"
    args = parser.parse_args(['pull', '-m', '-html',"-o",directory,"2"])
    predict_files = ["2.add-two-numbers.py","2.add-two-numbers.md",'2.add-two-numbers.html']
    predict_files= [os.path.join(directory,x) for x in predict_files]
    main(args)
    for f in predict_files:
        assert os.path.exists(f)
    shutil.rmtree(directory)

def test_generate_source_md_html_language(parser):
    directory ="../leetcode_output"
    args = parser.parse_args(['pull', '-m', '2-3',"-o",directory])
    predict_files = ["2.add-two-numbers.py","2.add-two-numbers.md"]
    predict_files= [os.path.join(directory,x) for x in predict_files]
    main(args)
    for f in predict_files:
        assert os.path.exists(f)
    shutil.rmtree(directory)

