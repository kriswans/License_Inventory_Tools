from re import search
from sys import argv
from collections import Counter as ct

'''Create a group on lambda functions to perform RegEx searches'''
###Find Header Row based on LDoS string.
ldos = lambda s: search('Last Date of Support',s)
###Find any SKU containing 3K nomenclature.
is_3x50 = lambda s: search('3[68]50',s)
###Find any top level traditonal hardware SKU that also contains license level.
non_C1_3x50 = lambda s: search('WS-C3[68]50.*-[SE]',s)
###Find individual 3K on-box license SKUs.
lic_C1_3x50 = lambda s: search('C3[68]50-[24][48]-[SL]-[ES]',s)
###Find any C1 SKU that is less than 24 ports. These have license level as part of the top-level part.
non_24_48_port_C1 = lambda s: search('C1-WS.*-12.*',s)


def create_3K_lic_rpt(input_file, output_file, smart_account):
    '''Creates a CSV formatted Report of 3K licensing content from a file input
    of a CCW-R file export'''
    with open(input_file,'r') as f:
        rl=f.readlines()
    ### Find CCW-R header row to place into a list
    header=[i for i in rl if ldos(i)]
    ###Parse CCW-R lines with any 3x50 SKUs into a list of rows
    dev_3x50=[i for i in rl if is_3x50(i)]
    ###Parse CCW-R lines for traditional top-level SKU rows
    non_C1_dev=[i for i in dev_3x50 if non_C1_3x50(i)]
    ###Parse CCW-R lines for individual on-box SW upgrade licensing rows
    upg_lics=[i for i in dev_3x50 if lic_C1_3x50(i)]
    ###Parse C1 SKUs for 3Ks less than 12 ports b/c SW licenses appear in top-level
    non_24_48_port=[i for i in dev_3x50 if non_24_48_port_C1(i)]
    ###Concatenate all parsed lists
    parsed_ccwr_rows_list=header+non_C1_dev+upg_lics+non_24_48_port
    ###Perform count of elements in concatenated list and place in dict
    devdict=dict(ct([(i.split(','))[0] for i in parsed_ccwr_rows_list][1:]))
    ###Extract top-level SKUs and convert to list of actual licensing SKU that appear in CSSM.
    C3x50=[((i.split(','))[0][3:11]+'-'+(i.split(','))[0][-1]) for i in parsed_ccwr_rows_list if i.split(',')[0].startswith('WS-C3')]
    C3x50=C3x50+[((i.split(','))[0][:12].replace((i.split(','))[0][:5],'C')+'-'+(i.split(','))[0][-1]) for i in parsed_ccwr_rows_list if i.split(',')[0].startswith('C1-WS')]
    C3x50_E=[i.replace(i[-2:],'-S-E') for i in C3x50 if i.endswith('E')]
    C3x50_S=[i.replace(i[-2:],'-L-S') for i in C3x50 if i.endswith('S')]
    ###Extract top-level upgrade license SKUs and convert to list
    upg_lics_indiv=[i.split(',')[0] for i in upg_lics]
    ###Concatenate license lists
    total_upg_lics=C3x50_E+C3x50_S+upg_lics_indiv
    ###Perform count of elements in concatenated list and place in dict
    licdict=dict(ct(total_upg_lics))
    ###Create output file
    with open (output_file,'w') as f:
        f.write('Top-Level Device OR License,-----,Count\n')
        for i in devdict:
            f.write(i+',-----,'+str(devdict[i])+'\n')
        f.write(4*'\n')
        f.write("LICENSES to be deposited in %s\n\n"%smart_account+'License,-----,Count\n')
        for i in licdict:
            f.write(i+',-----,'+str(licdict[i])+'\n')
        f.write(4*'\n')
        f.write("Full License/Device Breakout from CCW-R\n\n")
        for i in parsed_ccwr_rows_list:
            f.write(i)

if __name__=="__main__":
    try:
        input_file, output_file, smart_account=argv[1:4]
        create_3K_lic_rpt(input_file, output_file, smart_account)
    except Exception as Ex:
        print('\nEncountered exception:\n%s\n'%Ex)
        print('Example syntax:\npython 3K_license_finder.py inputfile.csv report.csv sa.domain.mil\n')
