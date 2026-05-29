from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, or_, select

from app.enums.models.roles_names_enum import RolesNamesEnum
from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType
from app.models.role import Role
from app.models.tenant_user import TenantUser
from app.models.user import User
from app.utils.uuid import is_valid_uuid


class DoctorRepository:
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def paginate(self, page: int, limit: int, search: str | None) -> Page[TenantUser]:
        query = (
            select(TenantUser)
            .where(
                TenantUser.tenant_id == self.tenant_id,
                TenantUser.member_type == TenantUserMemberType.DOCTOR,
            )
            .join(User, User.id == TenantUser.user_id)
            .join(Role, Role.id == TenantUser.role_id)
            .where(Role.name == RolesNamesEnum.DOCTOR.value)
            .options(selectinload(TenantUser.user))
            .order_by(User.first_name.asc(), User.last_name.asc())
        )

        if search:
            search_value = search.strip()
            conditions = [
                User.first_name.ilike(f"%{search_value}%"),
                User.last_name.ilike(f"%{search_value}%"),
                User.email.ilike(f"%{search_value}%"),
                User.document.ilike(f"%{search_value}%"),
                User.crm_number.ilike(f"%{search_value}%"),
            ]

            if is_valid_uuid(search_value):
                conditions.append(User.id == UUID(search_value))

            query = query.where(or_(*conditions))

        return paginate(self.session, query, Params(page=page, size=limit))

    def find_user_by_doctor_id(self, doctor_id: UUID) -> User | None:
        query = (
            select(User)
            .join(TenantUser, TenantUser.user_id == User.id)
            .join(Role, Role.id == TenantUser.role_id)
            .where(
                User.id == doctor_id,
                TenantUser.tenant_id == self.tenant_id,
                TenantUser.member_type == TenantUserMemberType.DOCTOR,
                Role.name == RolesNamesEnum.DOCTOR.value,
            )
        )
        return self.session.exec(query).first()

    def find_tenant_user_by_user_id(self, doctor_id: UUID) -> TenantUser | None:
        query = (
            select(TenantUser)
            .join(Role, Role.id == TenantUser.role_id)
            .where(
                TenantUser.user_id == doctor_id,
                TenantUser.tenant_id == self.tenant_id,
                TenantUser.member_type == TenantUserMemberType.DOCTOR,
                Role.name == RolesNamesEnum.DOCTOR.value,
            )
        )
        return self.session.exec(query).first()

    def find_user_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).first()

    def find_user_by_document(self, document: str) -> User | None:
        return self.session.exec(select(User).where(User.document == document)).first()

    def find_user_by_crm(self, crm_state: str, crm_number: str) -> User | None:
        return self.session.exec(
            select(User).where(
                User.crm_state == crm_state,
                User.crm_number == crm_number,
            )
        ).first()

    def save_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def save_tenant_user(self, tenant_user: TenantUser) -> TenantUser:
        self.session.add(tenant_user)
        self.session.commit()
        self.session.refresh(tenant_user)
        return tenant_user

    def delete_tenant_user_by_user_id(self, doctor_id: UUID) -> None:
        self.session.exec(
            delete(TenantUser).where(
                TenantUser.user_id == doctor_id,
                TenantUser.tenant_id == self.tenant_id,
                TenantUser.member_type == TenantUserMemberType.DOCTOR,
            )
        )
        self.session.commit()
