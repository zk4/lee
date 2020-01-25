#coding: utf-8
from lee.cli import Cli
from lee.enhancer import Enhancer
from lee import main,createParse
import os
import pytest
import shutil


@pytest.fixture
def parser():
    return  createParse()
       



def test_ls_specifed(parser):
    print("\n")
    args = parser.parse_args(['show','2,3'])
    main(args)
def test_ls_one(parser):
    print("\n")
    args = parser.parse_args(['show','2'])
    main(args)

def test_ls_range(parser):
    print("\n")
    args = parser.parse_args(['show','1-2'])
    main(args)

def test_ls_solution(parser):
    print("\n")
    args = parser.parse_args(['show','2',"-s 1"])
    main(args)
