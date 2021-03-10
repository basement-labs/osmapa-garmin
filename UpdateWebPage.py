"""Script updating the distribution webpage with links to current distributions.  
"""
import osmapa.www

osmapa.www.refresh_index_html(
    product_dir="/home/atalarczyk/osmapa-garmin/products", 
    product_list=[
        "OSMapaPL-PODSTAWOWA", 
        "OSMapaPL-OGONKI", 
        "OSMapaPL-LIGHT", 
        "OSMapaPL-WARSTWICE", 
        "OSMapaPL-SZLAKI",
        "OSMapaPLext-PODSTAWOWA", 
        "OSMapaPLext-OGONKI", 
        "OSMapaPLext-LIGHT", 
        "OSMapaPLext-WARSTWICE", 
        "OSMapaPLext-SZLAKI",
        ], 
    template_file="/home/atalarczyk/osmapa-garmin/www/TEMPLATE_index.html", 
    target_file="/home/atalarczyk/osmapa-garmin-www/index.html")
