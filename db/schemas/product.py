def product_schema (product) -> dict:

    return {"id":str(product["_id"]),
            "name":product["name"],
            "type":product["type"],
            "author":product["author"],
            "quantity":product["quantity"],
            "price":product["price"],
            "img":product["img"],
            "deshab":product["deshab"]
            }

def products_schema (products)->list:
    return [product_schema(product) for product in products]
