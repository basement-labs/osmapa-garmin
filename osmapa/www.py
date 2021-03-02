"""Processor for HTML files.

Author: Andrzej Talarczyk <andrzej@talarczyk.com>

Based on work of Michał Rogalski (Rogal).

License: GPLv3.
"""

import subprocess
from shutil import move

def refresh_index_html(product_dir, product_list, template_file, target_file):
    """Find latest versions of map products and produce a correct index.html file from template. 

    Args:
        products_dir (string): directory where products are located
        product_list (array of string): a list of product names (e.g. "FAMILY-PRODUCT" in FAMILY-PRODUCT-[YYYYMMDD]V[VERSION].exe)
        template_file (string): source index.html file with placeholder tags ([YYYYMMDD] and [VERSION])
        target_file (string): target index.html file to be (over)written after tags have been replaced with values. 
    """

    # Read template.
    with open(template_file, 'r') as f:
        contents = f.read()

    for prod in product_list:
        prod_split = prod.split("-")
        latest_p_exe = get_latest_product(family=prod_split[0], product=prod_split[1], product_suffix="*.exe", product_dir=product_dir)
        latest_p_img = get_latest_product(family=prod_split[0], product=prod_split[1], product_suffix="*_IMG.zip", product_dir=product_dir)

        if latest_p_exe != None and latest_p_exe != "":
            contents = contents.replace(prod+"-[YYYYMMDD]V[VERSION].exe", latest_p_exe)
        if latest_p_img != None and latest_p_img != "":
            contents = contents.replace(prod+"-[YYYYMMDD]V[VERSION]_IMG.zip", latest_p_img)

    # Write out new HTML file.
    move(target_file, target_file + "_OLD")
    with open(target_file, 'w') as f2: 
        f2.write(contents)


def get_latest_product(family, product, product_suffix, product_dir) -> str:
    """Retrieves the name of the most current map product file.

    Args:
        family (string): map family name (e.g. "OSMapaPL" or "OSMapaPLext")
        product (string): map product name (e.g.: "PODSTAWOWA, OGONKI, LIGHT, WARSTWICE, SZLAKI)
        product_suffix (string): map product file name suffix (e.g.: "_IMG.zip" or ".exe")
        product_dir (string): directory where map products are present

    Returns:
        str: map product file name
    """
    command = "ls {product_dir}/{family}-{product}-*{product_suffix} | sort -r | head -1 | xargs -n 1 basename".format(family=family, product=product, product_suffix=product_suffix, product_dir=product_dir)
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout.rstrip()


if __name__ == "__main__":
    import sys
    primary_def_name = "osmapa.www.refresh_index_html()"
    if (len(sys.argv) < 5):
        print("You are trying to run {primary_def_name} as script but not all required parameters have been given. Stop.".format(primary_def_name=primary_def_name))
    else:
        print("Running {primary_def_name} as script...".format(primary_def_name=primary_def_name))
        refresh_index_html(product_dir=sys.argv[1], product_list=sys.argv[2], template_file=sys.argv[3], target_file=sys.argv[4])
        print("Refreshed {target_file}.".format(target_file=sys.argv[4]))