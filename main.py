from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from scraper_new import get_linkedin_profiles
from typing import List

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search_companies(
    request: Request,
    companies: str = Form(...),
    num_results: int = Form(3),
    search_terms: str = Form(...)
):
    company_list = [company.strip() for company in companies.split(',') if company.strip()]
    search_terms_list = [term.strip() for term in search_terms.splitlines() if term.strip()]
    
    all_profiles = []
    for company in company_list:
        profiles = get_linkedin_profiles(company, search_terms_list, num_results)
        for profile in profiles:
            all_profiles.append({
                "name": profile[0],
                "company": company,
                "role": profile[1],
                "url": profile[2]
            })
    
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "profiles": all_profiles}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )

