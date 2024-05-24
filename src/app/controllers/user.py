from pydantic import TypeAdapter
from sqlalchemy import select

from src.app.models.user import User as UserModel
from src.app.schemas.user import User as UserSchema
from .base import Controller


class UserController(Controller[UserModel]):

    def list_users(self) -> list[UserSchema]:
        stmt = select(UserModel)
        users = self.session.scalars(stmt.order_by(UserModel.user_id)).fetchall()
        return TypeAdapter(list[UserSchema]).validate_python(users)

    def get_user_by_email(self, email: str) -> UserSchema:
        stmt = select(UserModel).where(UserModel.email == email)
        user = self.session.scalars(stmt).one_or_none()

        if user is None:
            raise ValueError("No user found with this email")

        return TypeAdapter(UserSchema).validate_python(user)

    def get_user_by_id(self, user_id: int) -> UserSchema:
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        user = self.session.scalars(stmt).one_or_none()

        if user is None:
            raise ValueError("No user found with this user id")

        return TypeAdapter(UserSchema).validate_python(user)

    def update_password(self, email: str, new_password_hash: str) -> None:
        user = self.get_user_by_email(email)

        try:
            user.password = new_password_hash
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update_profile(self, email: str, first_name: str, last_name: str, address1: str, address2: str, zipcode: str,
                       city: str, state: str, country: str, phone: str) -> None:
        user = self.get_user_by_email(email)

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.address1 = address1
            user.address2 = address2
            user.zipcode = zipcode
            user.city = city
            user.state = state
            user.country = country
            user.phone = phone

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def insert_user(self, email: str, password: str, first_name: str, last_name: str, address1: str, address2: str,
                    zipcode: str, city: str, state: str, country: str, phone: str) -> None:
        try:
            new_user = UserModel(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                address1=address1,
                address2=address2,
                zipcode=zipcode,
                city=city,
                state=state,
                country=country,
                phone=phone
            )

            self.session.add(new_user)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
