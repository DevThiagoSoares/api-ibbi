from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.repositories.shopping_cart_repository import ShoppingCartRepository
from src.api.schemas.shopping_cart import AddToCartRequest, UpdateCartRequest
from src.api.models.shopping_cart import ShoppingCart
from src.api.models.purchase import Purchase

class ShoppingCartService:
    def __init__(self, db: Session):
        self.repo = ShoppingCartRepository(db)

    def add_product_to_cart(self, user_id: int, request: AddToCartRequest):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        product = self.repo.get_product_by_id(request.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        if product.quantity < request.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade solicitada não disponível em estoque")

        shopping_cart = self.repo.get_shopping_cart_by_user_id(user_id)
        if not shopping_cart:
            shopping_cart = ShoppingCart(user_id=user.id)
            self.repo.add_shopping_cart(shopping_cart)

        existing_purchase = None
        for purchase in shopping_cart.purchases:
            if purchase.product_id == request.product_id:
                existing_purchase = purchase
                break

        if existing_purchase:
            existing_purchase.quantity += request.quantidade
        else:
            new_purchase = Purchase(
                shopping_cart_id=shopping_cart.id,
                product_id=request.product_id,
                quantity=request.quantidade
            )
            self.repo.add_purchase(new_purchase)

        product.quantity -= request.quantidade
        self.repo.commit()

        response_items = [
            {"product_id": purchase.product_id, "quantity": purchase.quantity}
            for purchase in shopping_cart.purchases
        ]
        return {"user_id": shopping_cart.user_id, "items": response_items}

    def list_cart_products(self, user_id: int):
        shopping_cart = self.repo.get_shopping_cart_by_user_id(user_id)
        if not shopping_cart:
            return []

        response_items = [
            {
                "product_id": purchase.product_id,
                "quantity": purchase.quantity,
                "price_per_unit": purchase.product.price,
                "total_price": purchase.product.price * purchase.quantity,
                "image": purchase.product.image,
                "name": purchase.product.name,
            }
            for purchase in shopping_cart.purchases
        ]

        total_cart_value = sum(item["total_price"] for item in response_items)
        return {
            "user_id": user_id,
            "total_cart_value": total_cart_value,
            "products": response_items
        }

    def update_cart(self, user_id: int, items_to_update: list[UpdateCartRequest]):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        shopping_cart = self.repo.get_shopping_cart_by_user_id(user_id)
        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")

        purchase_dict = {purchase.product_id: purchase for purchase in shopping_cart.purchases}

        for item in items_to_update:
            product = self.repo.get_product_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Produto com ID {item.product_id} não encontrado")

            current_quantity = purchase_dict[item.product_id].quantity if item.product_id in purchase_dict else 0
            difference = current_quantity - item.quantity

            if difference > 0:
                product.quantity += difference
            elif difference < 0:
                if item.quantity > (product.quantity + current_quantity):
                    raise HTTPException(status_code=400, detail=f"Quantidade solicitada para o produto {product.name} não disponível em estoque")
                product.quantity -= abs(difference)

            if item.quantity == 0:
                if item.product_id in purchase_dict:
                    self.repo.delete_purchase(purchase_dict[item.product_id])
            else:
                if item.product_id in purchase_dict:
                    purchase_dict[item.product_id].quantity = item.quantity
                else:
                    new_purchase = Purchase(
                        shopping_cart_id=shopping_cart.id,
                        product_id=item.product_id,
                        quantity=item.quantity
                    )
                    self.repo.add_purchase(new_purchase)

        self.repo.commit()

        response_items = [
            {
                "product_id": purchase.product_id,
                "quantity": purchase.quantity,
                "price_per_unit": purchase.product.price,
                "total_price": purchase.product.price * purchase.quantity
            }
            for purchase in shopping_cart.purchases
        ]

        total_cart_value = sum(item["total_price"] for item in response_items)
        return {
            "user_id": user_id,
            "total_cart_value": total_cart_value,
            "products": response_items
        }