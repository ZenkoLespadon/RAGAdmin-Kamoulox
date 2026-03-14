from pydantic import BaseModel, Field, ValidationError, field_validator

class RequestAPI(BaseModel):
    req: str = Field(..., title="Requête utilisateur", description="Texte de la requête")

    # ✅ Vérification de la validité de la requête
    @field_validator("req")
    @classmethod
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Le champ 'req' ne peut pas être vide.")
        return v

