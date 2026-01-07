from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher


class SecuritySettings(BaseSettings):
    """Security configuration settings"""
    
    # Password hashing settings
    password_algorithm: Literal["argon2", "bcrypt"] = Field(
        default="argon2",
        description="Password hashing algorithm"
    )
    
    # Argon2 specific settings
    argon2_memory_cost: int = Field(
        default=65536,  # 64 MB
        description="Argon2 memory cost in KB"
    )
    argon2_time_cost: int = Field(
        default=3,
        description="Argon2 time cost (iterations)"
    )
    argon2_parallelism: int = Field(
        default=1,
        description="Argon2 parallelism factor"
    )
    
    # Bcrypt specific settings
    bcrypt_rounds: int = Field(
        default=12,
        description="Bcrypt rounds (cost factor)"
    )
    
    
    class Config:
        env_prefix = "SECURITY_"
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


class PasswordHasher:
    def __init__(self, settings: SecuritySettings):
        self.settings = settings
        self.algorithm = settings.password_algorithm
        self.__context = self._create_password_context()

    def _create_password_context(self) -> PasswordHash:
        """Create password context based on configured algorithm"""
        if self.algorithm == "argon2":
            hasher = Argon2Hasher(
                memory_cost=self.settings.argon2_memory_cost,
                time_cost=self.settings.argon2_time_cost,
                parallelism=self.settings.argon2_parallelism
            )
        elif self.algorithm == "bcrypt":
            hasher = BcryptHasher(rounds=self.settings.bcrypt_rounds)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        return PasswordHash([hasher])

    def hash(self, password: str) -> str:
        return self.__context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.__context.verify(password, hashed_password)


@lru_cache()
def get_security_settings() -> SecuritySettings:
    """Get singleton security settings instance"""
    return SecuritySettings()


@lru_cache()
def get_password_hasher() -> PasswordHasher:
    """Dependency function that provides a singleton PasswordHasher instance"""
    settings = get_security_settings()
    return PasswordHasher(settings)
