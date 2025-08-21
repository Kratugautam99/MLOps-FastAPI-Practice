from pydantic import BaseModel, EmailStr, constr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class ContactDetails(BaseModel):
    Email: Optional[EmailStr]    
    Phone: Optional[constr(pattern=r'^\d{10}$')]
    LinkedIn: Optional[AnyUrl]
    @field_validator("Email")
    @classmethod
    def validate_email(cls, value, mode="after"):
        if value.split("@")[-1] not in ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]:
            raise ValueError("Email domain must be one of: gmail.com, yahoo.com, outlook.com, hotmail.com")
        return value

class User(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=1, max_length=50, title="Name of the Customer", description="Full name of the customer in First Name and Last Name format", examples=["Kohn Dogsman", "Fim Jikandu"])]
    age: int = Field(gt=0, le=125)  
    expenditure: float = Field(gt=0.0, strict=True)  
    married: bool = None
    prev_orders: List[str] = Field(max_length=5)
    contact_details: ContactDetails # for flexibility=> Dict[str, str]
    @model_validator(mode="after")
    @classmethod
    def validate_user(cls, user):
        if user.age < 18 and user.married:
            raise ValueError("Users under 18 cannot be married.")
        return user
    
    @computed_field
    @property
    def worth(self) -> str:
        if self.expenditure > 100000:
            return "Premium Customer"
        elif self.expenditure > 5000:
            return "Loyal Customer"
        elif self.expenditure > 1000:
            return "Occassional Customer"
        else:
            return "Newbie Customer"



customer = {'id': 27, 'name': 'Kratu Gautam', 'age': 20, 'expenditure': 700000.99,
            'married': False, 'prev_orders': ['Asus Laptop', 'Creatine', 'Tempeh'],
            'contact_details': {'Email': 'kg@gmail.com', 'Phone': '9876543210', 'LinkedIn': 'https://www.linkedin.com/in/kg'}}
user = User(**customer)

def display_user(user: User):
    print("\n\nUser Details:")
    print(f"ID: {user.id}")
    print(f"Name: {user.name}")
    print(f"Age: {user.age}")
    print(f"Expenditure: ${user.expenditure:.2f}")
    print(f"Worth: {user.worth}")
    print(f"Married: {'Yes' if user.married else "No" if not user.married else 'N/A'}")
    print(f"Previous Orders: {', '.join(user.prev_orders)}")
    #print(f"Contact Details: {', '.join(f"{k}: {v}" for k,v in user.contact_details.items())}") for Dict[str, str]
    print(f"Contact Details: {user.contact_details}\n\n")
display_user(user)

# include, exclude, exclude_unset, include_unset are some parameters for model_dump
temp = user.model_dump(mode="json")
print(f"User Model Dump {type(temp)}:", temp) 
temp = user.model_dump(mode="dict")
print(f"User Model Dump {type(temp)}:", temp)