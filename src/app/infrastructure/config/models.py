from dataclasses import dataclass


@dataclass
class AppConfig:
    debug: bool
    major_version: int
    minor_version: int
    patch_version: int


@dataclass
class DatabaseConfig:
    url: str

    @property
    def full_url(self) -> str:
        return self.url


@dataclass
class DefaultConfig:
    url: str

    @property
    def full_url(self) -> str:
        return self.url


@dataclass
class Config:
    app_config: AppConfig
    db_config: DatabaseConfig
    default_config: DefaultConfig
