# -*- coding:utf-8 -*-
"""
Author : Junwu Chen
Time   : 2021/09/27
E-mail : 845017597@qq.com
Desc.  :
"""


def remove_repeats(old_list):
    """ Remove redundant (repetitive) elements (string) in a list

    Args:
        old_list (list): original list (1 dimension)

    Returns:
        list: a new list without repeat (1 dimension)
    """
    new_list = []
    for element in old_list:
        element = element.strip()
        if element not in new_list:
            new_list.append(element)
    return new_list


# load the SMILES of cations
filename = './smiles/cation.smi'
with open(filename, 'r') as file_object1:
    ca_smi_list = file_object1.readlines()
print('*** {:>5d} cations were loaded. ***'.format(len(ca_smi_list)))
ca_smi_list = remove_repeats(ca_smi_list)
print('*** After removing duplicates, there are {} cations. ***\n'.format(len(ca_smi_list)))

# load the SMILES of anions
filename = './smiles/anion.smi'
with open(filename, 'r') as file_object2:
    an_smi_list = file_object2.readlines()
print('*** {:>5d} anions were loaded. ***'.format(len(an_smi_list)))
an_smi_list = remove_repeats(an_smi_list)
print('*** After removing duplicates, there are {} anions. ***\n'.format(len(an_smi_list)))

# combine SMILES of all cations and anions
# to generate the SMILES of theoretical structures of ILs
ils_smi = []
for cation in ca_smi_list:
    for anion in an_smi_list:
        new_ils_smi = anion + '.' + cation
        ils_smi.append(new_ils_smi)
print('*** {:>9d} theoretical ILs were generated. ***\n'.format(len(ils_smi)))

# output the generated SMILES to .txt file
out_filename = './smiles/ils.smi'
with open(out_filename, 'w') as file_object:
    for il_smi in ils_smi:
        file_object.write(il_smi + '\n')
print('Finished! The generated SMILES were output to ils.smi file.')
