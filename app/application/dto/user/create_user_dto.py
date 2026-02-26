from pydantic import BaseModel, EmailStr, Field

class CreateUserDTO(BaseModel):
    email: EmailStr 
    
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full user name"
    )
    
    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
        description="User password"
    )
