from .models import Element, Sale

message1="{product_name} está por acabarse. Solo quedan {quantity} unidades en stock."
message2="{product_name} se ha agotado. No hay unidades disponibles en stock."
message3="Se ha registrado una venta de {quantity} unidades de {product_name}."

for sale in Sale.objects.select_related("element").order_by("-date", "-id"):
    product = sale.element
    if product.quantity <= product.min_quantity:
        if product.quantity == 0:
            message = message2.format(product_name=product.name)
        else:
            message = message1.format(product_name=product.name, quantity=product.quantity)
        print(message)  

    sale_message = message3.format(quantity=sale.quantity, product_name=product.name)
    print(sale_message) 
