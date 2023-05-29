# -*- coding:utf-8 -*-
"""
Author : Junwu Chen
Time   : 2021/08/25
E-mail : 845017597@qq.com
Desc.  :
"""


import os
import subprocess
# import pandas as pd


def smi2xyz(smiles):
    """ convert a list of SMILES to .xyz coordinate files

    Args:
        smiles (list): a list of SMILES that need to be converted

    Returns:
        int: the number of SMILES that can't be converted
    """

    err_xyz = 0  # the number of error during conversion

    for i, smi in enumerate(smiles):
        _out = subprocess.Popen(
            ['obabel', f'-:{smi}', '--gen3d', '-oxyz', '-O', '{:0>6d}.xyz'.format(i)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        _out = _out.stdout.readline()
        if _out == b'1 molecule converted\n':
            subprocess.run(['sed', '-i', f'2c{smi}', '{:0>6d}.xyz'.format(i)])
        else:
            err_xyz += 1
            subprocess.run(['rm', '{:0>6d}.xyz'.format(i)])
            with open('error.smi', 'a') as file_object:
                print(smi, file=file_object)

    return err_xyz


def smi2mopac(smiles):
    """ convert a list of SMILES to MOPAC input files

    Args:
        smiles (list): a list of SMILES that need to be converted

    Returns:
        int: the number of SMILES that can't be converted
    """

    err_mop = 0  # the number of error during conversion

    for i, smi in enumerate(smiles):
        _out = subprocess.Popen(
            ['obabel', f'-:{smi}', '--gen3d', '-omop', '-O', '{:0>6d}.mop'.format(i)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        _out = _out.stdout.readline()
        if _out == b'1 molecule converted\n':
            subprocess.run(['sed', '-i', '1cPM7\ precise', '{:0>6d}.mop'.format(i)])
            subprocess.run(['sed', '-i', '2cmolecule', '{:0>6d}.mop'.format(i)])
            subprocess.run(['sed', '-i', '3cAll\ coordinates\ are\ Cartesian', '{:0>6d}.mop'.format(i)])
        else:
            err_mop += 1
            subprocess.run(['rm', '{:0>6d}.mop'.format(i)])
            with open('error.smi', 'a') as file_object:
                print(smi, file=file_object)

    return err_mop


with open('./smiles/cation.smi', 'r') as file_object:
    ca_smi = file_object.readlines()

with open('./smiles/anion.smi', 'r') as file_object:
    an_smi = file_object.readlines()

with open('./smiles/ils.smi', 'r') as file_object:
    ils_smi = file_object.readlines()

# df = pd.read_csv('raw.csv')
# smiles = df['Smiles'].values.tolist()
# obabel -:C --gen3d -omol -O C.mol

root_path = os.path.split(os.path.realpath(__file__))[0]
dir_exit = os.path.exists('coord')
os.system('rm -rf coord')
os.mkdir('coord')
os.chdir('coord')

os.mkdir('cation')
os.chdir('cation')
err_ca_xyz = smi2xyz(ca_smi)

os.chdir('..')
os.mkdir('anion')
os.chdir('anion')
err_an_xyz = smi2xyz(an_smi)

os.chdir(root_path)
print('{:*>27s} Summary {:*>27s}'.format('', ''))
print('%4d incorrect cation SMILES occurred in generating .xyz files' %(err_ca_xyz))
print('%5d incorrect anion SMILES occurred in generating .xyz files' %(err_an_xyz))
