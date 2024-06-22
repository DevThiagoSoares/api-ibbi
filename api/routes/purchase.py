from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from shared.security import get_current_user
from api.models.user import User
from api.services.purchase_service import PurchaseService

router = APIRouter(prefix="/api", tags=["purchase"])

@router.post("/purchase/finalize")
async def finalize_purchase(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    purchase_service = PurchaseService(db)
    return purchase_service.finalize_purchase(current_user)