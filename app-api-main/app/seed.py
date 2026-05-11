from sqlmodel import Session

from app.core.database import engine
from app.seeders.permission_seeder import PermissionSeeder
from app.seeders.role_permission_seeder import RolePermissionSeeder
from app.seeders.role_seeder import RoleSeeder


def seed() -> None:
    with Session(engine) as session:
        seeders = [
            PermissionSeeder(session),
            RoleSeeder(session),
            RolePermissionSeeder(session),
        ]
        for seeder in seeders:
            seeder.run()
            session.commit()


if __name__ == "__main__":
    seed()
