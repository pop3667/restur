from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Image,Spacer,HRFlowable
from reportlab.lib.pagesizes import letter

from django.db.models.signals import post_save,post_delete
from django.dispatch.dispatcher import receiver
from .models import  Food
from django.conf import settings
import os
def add_products(products):
    product_tables= []

    for product in products:
        product_table  = Table(
            [
                [product["title"],""],
                [product["category"]],
                [product["description"]],
                [f"{product["price"]}$"],
                [Image(product["image"],width=120,height=90)],
                [Spacer(30,30)],
            ]
        )
        product_tables.append(product_table)
    return product_tables

@receiver([post_save,post_delete],sender=Food)
def deal_with_food(sender,instance,**kwargs):
    elements = []
    data=[]
    product_tables=[]
    doc = SimpleDocTemplate(os.path.join(settings.BASE_DIR,"menu.pdf"),pagesize=letter)
    products = [{
        "title":f.title,
        "category":f.category,
        "price":f.price_after_discount,
        "description":f.description,
        "image":f.image.path,
        }
        for f in Food.objects.all()]
    

    product_tables  = add_products(products)
    table_style_data = [
        ("LINEBEFORE",(1,0),(1,-1),1,colors.black),
    ]
    
    for  i in range(0,len(product_tables),2):
        lista = product_tables[i:i+2]
        data.append(lista)
        table_style_data.append(("LINEBELOW",(0,data.index(lista)),(1,data.index(lista)),1,colors.black) )

    table_style = TableStyle(table_style_data)


    all_table  =Table(
        data=data,style=table_style
    )
    elements.append(all_table)
    doc.build(elements)




