from googlesearch import search
from urllib import parse
import re
import time

def get_linkedin_profiles(company_name, search_terms, num_results=3):
    profiles = []
    seen_profiles = set()

    for term in search_terms:
        query = f"{company_name} linkedin india {term}"

        try:
            search_results = list(search(query, num_results=num_results))
            time.sleep(0.5)  # Add small delay to avoid rate limiting
        except Exception as e:
            print(f"Error performing search for {query}: {e}")
            continue

        for result in search_results:
            if "linkedin.com" in result:
                path = parse.urlparse(result).path
                
                if path.split("/")[1] == "in":
                    profile_name = result.split("/in/")[-1].split("-")
                    pattern = re.compile(r"^[A-Za-z]+$")
                    filtered_profile_name = [
                        item for item in profile_name if pattern.match(item)
                    ]
                    profile_name = " ".join(filtered_profile_name).title()

                    if profile_name and profile_name not in seen_profiles:
                        seen_profiles.add(profile_name)
                        profiles.append((profile_name, term, result))

    return profiles

