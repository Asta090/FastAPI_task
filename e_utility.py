from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings
from schemas import OrderOut
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_order_email(email: str, order: OrderOut):
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=[email],
        body=f"""
        Order ID: {order.order_id}
        Product: {order.product}
        Quantity: {order.quantity}
        Status: {order.status}
        """,
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)