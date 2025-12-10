from pydantic import BaseModel
from typing import Optional

class MarketingPlanRequest(BaseModel):
    businessName: str
    industry: str
    targetAudience: str
    productService: str
    budget: str
    goals: str
    timeline: str
    competitors: Optional[str] = ""
    uniqueSellingPoint: Optional[str] = ""
    marketingPlatforms: Optional[str] = ""


class BlogRequest(BaseModel):
    topic: str
    targetKeyword: str
    targetAudience: str
    blogLength: str
    tone: str
    businessName: Optional[str] = None
    industry: Optional[str] = None
    additionalNotes: Optional[str] = None
