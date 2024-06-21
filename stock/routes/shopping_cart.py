from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload
from stock.models.shopping_cart import ShoppingCart
from stock.models.user import User
from stock.models.product import Product
from stock.models.purchase import Purchase
from stock.schemas.shopping_cart import UpdateCartRequest, AddToCartRequest
from shared.dependencies import get_db
from shared.security import get_current_user

router = APIRouter(prefix="/api", tags=["shopping_cart"])

@router.post("/shopping-cart")
async def adicionar_produto_ao_carrinho(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user
    product_id = request.product_id
    quantidade = request.quantidade

    # Verifica se o usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Verifica se o produto existe
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    # Verifica se há estoque suficiente
    if product.quantity < quantidade:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Quantidade solicitada não disponível em estoque")

    # Verifica se há um carrinho ativo para o usuário, senão cria um novo
    if not user.shopping_cart:
        shopping_cart = ShoppingCart(user_id=user.id)
        db.add(shopping_cart)
        db.commit()
        db.refresh(shopping_cart)
    else:
        shopping_cart = user.shopping_cart

    # Carrega as compras do carrinho usando selectinload para garantir que sejam carregadas junto
    shopping_cart = (
        db.query(ShoppingCart)
        .filter(ShoppingCart.user_id == user.id)
        .options(selectinload(ShoppingCart.purchases))
        .first()
    )

    # # Verifica se o produto já está no carrinho
    existing_purchase = None
    for purchase in shopping_cart.purchases:
        if purchase.product_id == product_id:
            existing_purchase = purchase
            break

    if existing_purchase:
        # Atualiza a quantidade se já estiver no carrinho
        existing_purchase.quantity += quantidade
    else:
        # Adiciona um novo item ao carrinho
        new_purchase = Purchase(
            shopping_cart_id=shopping_cart.id,
            product_id=product_id,
            quantity=quantidade
        )
        db.add(new_purchase)

    # Atualiza a quantidade disponível do produto
    product.quantity -= quantidade
    db.commit()

    # Recarrega o carrinho com as compras atualizadas
    shopping_cart = db.query(ShoppingCart).filter_by(id=shopping_cart.id).first()

    # Constrói a resposta conforme o modelo Pydantic ShoppingCartResponse
    response_items = [
        {"product_id": purchase.product_id, "quantity": purchase.quantity}
        for purchase in shopping_cart.purchases
    ]
    return {"user_id": shopping_cart.user_id, "items": response_items}


@router.get("/shopping-cart")
async def listar_produtos_do_carrinho(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user

    # Verifica se há um carrinho ativo para o usuário
    shopping_cart = (
        db.query(ShoppingCart)
        .filter(ShoppingCart.user_id == user_id)
        .options(selectinload(ShoppingCart.purchases))
        .first()
    )

    if not shopping_cart:
        return []

    # Calcula o valor total do carrinho
    total_value = sum(purchase.product.price * purchase.quantity for purchase in shopping_cart.purchases)

    # Constrói a resposta conforme o modelo Pydantic ShoppingCartDetailResponse
    response_items = [
        {
            "product_id": purchase.product_id,
            "quantity": purchase.quantity,
            "price_per_unit": purchase.product.price,
            "total_price": purchase.product.price * purchase.quantity,
            "image":db.query(Product)
            .filter(Product.id == purchase.product_id)
            .first().image,
            "name": db.query(Product)
            .filter(Product.id == purchase.product_id)
            .first().name,
        }
        for purchase in shopping_cart.purchases
    ]

    # Adiciona o total de todos os produtos do carrinho à resposta
    total_cart_value = sum(item["total_price"] for item in response_items)

    return {
        "user_id": user_id,
        "total_cart_value": total_cart_value,
        "products": response_items
    }


@router .put("/shopping-cart")
async def update_shopping_cart(
    request: List[UpdateCartRequest],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user
    items_to_update = request
    # Verifica se o usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Obtém o carrinho de compras do usuário
    shopping_cart = (
        db.query(ShoppingCart)
        .filter(ShoppingCart.user_id == user_id)
        .first()
    )

    if not shopping_cart:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Carrinho não encontrado")

    # Cria um dicionário para mapear product_id para purchase
    purchase_dict = {purchase.product_id: purchase for purchase in shopping_cart.purchases}

    # Itera sobre os itens a serem atualizados
    for item in items_to_update:
        product_id = item.product_id
        quantity = item.quantity

        # Verifica se o produto existe
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Produto com ID {product_id} não encontrado")

        # Calcula a diferença entre a quantidade atual no carrinho e a quantidade passada
        if product_id in purchase_dict:
            current_quantity = purchase_dict[product_id].quantity
        else:
            current_quantity = 0

        difference = current_quantity - quantity

        # Atualiza a quantidade no carrinho
        if difference > 0:
            # Se a quantidade no carrinho for maior que a quantidade passada, adicionar a diferença aos produtos
            product.quantity += difference
        elif difference < 0:
            # Se a quantidade no carrinho for menor que a quantidade passada, remover a diferença dos produtos
            # Verifica se há estoque suficiente
            if quantity > (product.quantity + current_quantity):
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    detail=f"Quantidade solicitada para o produto {product.name} não disponível em estoque")
            product.quantity -= abs(difference)

        # Atualiza o item no carrinho
        if quantity == 0:
            # Se a quantidade for zero, remover o item do carrinho
            if product_id in purchase_dict:
                db.delete(purchase_dict[product_id])
        else:
            if product_id in purchase_dict:
                purchase_dict[product_id].quantity = quantity
            else:
                new_purchase = Purchase(
                    shopping_cart_id=shopping_cart.id,
                    product_id=product_id,
                    quantity=quantity
                )
                db.add(new_purchase)

    db.commit()

    # Recarrega o carrinho com as compras atualizadas
    shopping_cart = (
        db.query(ShoppingCart)
        .filter(ShoppingCart.user_id == user_id)
        .first()
    )

    # Constrói a resposta conforme o modelo Pydantic ShoppingCartDetailResponse
    response_items = [
        {
            "product_id": purchase.product_id,
            "quantity": purchase.quantity,
            "price_per_unit": purchase.product.price,
            "total_price": purchase.product.price * purchase.quantity
        }
        for purchase in shopping_cart.purchases
    ]

    # Calcula o valor total do carrinho
    total_cart_value = sum(item["total_price"] for item in response_items)

    return {
        "user_id": user_id,
        "total_cart_value": total_cart_value,
        "products": response_items
    }
