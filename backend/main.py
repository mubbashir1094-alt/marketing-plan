from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import re
from pathlib import Path
from dotenv import load_dotenv

# Load env vars from the backend directory before importing modules
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from models import MarketingPlanRequest, BlogRequest
from generator import generate_with_google
from utils import clean_markdown_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Marketing Plan Generator API",
    description="Backend API for generating marketing plans using Google's Generative AI (Gemini)",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["https://your-app.vercel.app"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


@app.get("/")
async def root():
    return {
        "message": "AI Marketing Plan Generator API",
        "status": "running",
        "provider": "Google Generative AI (Gemini)",
        "endpoints": {
            "generate": "/generate - POST - Generate marketing plan",
            "health": "/health - GET - Health check",
            "docs": "/docs - Swagger documentation"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_provider": "Google Generative AI (Gemini)",
        "api_key_configured": bool(GOOGLE_API_KEY)
    }


@app.post("/generate")
async def generate_marketing_plan(request: MarketingPlanRequest):
    """Generate a comprehensive marketing plan based on business information"""
    
    prompt = f"""You are an expert digital marketing strategist. 

Generate a complete marketing plan using only the information provided by the user.

# USER INPUT

Business Name: {request.businessName}
Industry: {request.industry}
Product/Service: {request.productService}
Target Audience: {request.targetAudience}
Budget: {request.budget}
Goals: {request.goals}
Timeline: {request.timeline}
{f"USP: {request.uniqueSellingPoint}" if request.uniqueSellingPoint else ""}
{f"Competitors: {request.competitors}" if request.competitors else ""}
{f"Marketing Platforms: {request.marketingPlatforms}" if request.marketingPlatforms else ""}

# OUTPUT FORMAT

Return the final response as clean Markdown ONLY. No JSON.

## 1. Executive Summary

Short 3–5 sentence overview of the full marketing plan.

## 2. Market & Audience Analysis

- Industry overview  
- Customer pain points  
- Competitor positioning  

## 3. Marketing Goals (SMART)

List 3–5 high-impact goals.

## 4. Recommended Strategy

Explain the high-level approach for:
- branding  
- content  
- paid ads  
- SEO  
- social media  

## 5. Content Strategy Table

Create a Markdown table with EXACTLY these 4 columns:

| Platform | Content Type | Frequency | Goal |
| --- | --- | --- | --- |

Add **5–7 rows only**.  
Every row must have exactly 4 pipe-separated columns.

## 6. Marketing Funnel Strategy

- Awareness  
- Consideration  
- Conversion  
- Retention  

## 7. Budget Allocation Table

Create a Markdown table with EXACTLY these 3 columns:

| Channel | Percentage | Reason |
| --- | --- | --- |

Add **5 rows only**.

## 8. 30-Day Tactical Action Plan

List day-by-day or week-by-week actions.

## 9. KPIs & Measurement

Give measurable KPIs for each major channel.

## 10. Risks & Recommendations

List 3–5 risks + solutions.

# GLOBAL RULES (important)

- MUST use Markdown formatting only.  
- All tables must follow correct Markdown syntax.  
- Header → separator → rows must have SAME number of columns.  
- Never output JSON or code blocks unless they are Markdown tables.  
- If response becomes too long, shorten text but ALWAYS complete tables correctly."""

    try:
        logger.info("Generating marketing plan using Google Generative AI (Gemini)")
        
        plan = generate_with_google(prompt)
        
        if not plan:
            logger.error("Empty plan generated")
            raise HTTPException(status_code=500, detail="No response generated")
        
        logger.info("Successfully generated plan")
        
        # Log to console
        print("\n" + "="*80)
        print("GENERATED MARKETING PLAN")
        print("="*80)
        print(plan)
        print("="*80 + "\n")
        
        return {"plan": plan, "provider": "Google Generative AI (Gemini)"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate marketing plan: {str(e)}"
        )


@app.post("/generate-blog")
async def generate_blog(request: BlogRequest):
    """Generate an SEO-optimized blog post in Markdown.

    Request body must include: topic, targetKeyword, targetAudience, blogLength, tone.
    Optional: businessName, industry, additionalNotes.
    """

    # Basic validation for allowed blogLength and tone values
    allowed_lengths = {"500-800", "1000-1500", "1500-2000", "2000+"}
    allowed_tones = {"professional", "casual", "friendly", "authoritative", "conversational"}

    if request.blogLength not in allowed_lengths:
        raise HTTPException(status_code=400, detail=f"Invalid blogLength. Allowed: {', '.join(allowed_lengths)}")

    if request.tone not in allowed_tones:
        raise HTTPException(status_code=400, detail=f"Invalid tone. Allowed: {', '.join(allowed_tones)}")

    # Word count guidance to the model
    length_map = {
        "500-800": "~600 words",
        "1000-1500": "~1200 words",
        "1500-2000": "~1700 words",
        "2000+": "2000+ words (long-form, detailed)"
    }

    prompt = f"""You are an expert SEO content writer.  
Write a complete SEO-optimized blog post in **Markdown only**.

# INPUT
Topic: {request.topic}
Target Keyword: {request.targetKeyword}
Target Audience: {request.targetAudience}
Length: {length_map.get(request.blogLength)}
Tone: {request.tone}
Business Name: {request.businessName or "N/A"}
Industry: {request.industry or "N/A"}
Additional Notes: {request.additionalNotes or "None"}

# STRUCTURE
- Meta title (<= 60 chars, MUST include keyword)
- Meta description (<= 160 chars, MUST include keyword)
- Suggested URL slug  
- 3 SEO title variations  
- H1 with keyword  
- 2–4 paragraph intro (keyword within first 100 words)  
- At least 5 H2 sections  
- 3–6 H3 subsections  
- Keyword usage 4–8 times  
- 3 internal link suggestions  
- 2 external authoritative references  
- FAQ (3 questions)  
- CTA  
- Social share text (1 sentence)

# RULES
- Output must be Markdown only.
- No JSON.
- Write ACTUAL, detailed content for each section, not placeholders.
- Include real, helpful information tailored to the topic and audience.
"""

    try:
        logger.info("Generating SEO blog using Google Generative AI (Gemini)")
        
        blog = generate_with_google(prompt)

        if not blog:
            logger.error("Empty blog generated")
            raise HTTPException(status_code=500, detail="No blog content generated")

        # Small post-processing: ensure markdown only and clean tables
        blog = clean_markdown_tables(blog)

        return {"blog": blog}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate blog: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate blog: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)