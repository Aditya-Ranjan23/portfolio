import json
import os
import re

def slugify(text):
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def main():
    base_dir = r"d:\.Study\pep class\portfolio"
    
    with open(os.path.join(base_dir, "repos.json"), "r", encoding="utf-8") as f:
        repos = json.load(f)
        
    # filter out portfolio
    repos = [r for r in repos if r["name"].lower() != "portfolio"]
    
    # generate individual pages
    template_path = os.path.join(base_dir, "case-studies", "breathe-india-a-data-driven-exploration-of-air-quality-patterns.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    for r in repos:
        slug = slugify(r["name"])
        filename = f"{slug}.html"
        filepath = os.path.join(base_dir, "case-studies", filename)
        
        # basic replacements
        title = r["name"].replace("-", " ")
        desc = r["desc"] or f"A placeholder description for {title}. Please edit this later."
        link = r["url"]
        lang = r["lang"] or "Unknown"
        
        page_html = re.sub(r'<title>.*?</title>', f'<title>{title} | Case Study</title>', template)
        page_html = re.sub(r'<h1 class="text-gradient">.*?</h1>', f'<h1 class="text-gradient">{title}</h1>', page_html)
        page_html = re.sub(r'<p class="hero-desc mt-4">.*?</p>', f'<p class="hero-desc mt-4">{desc}</p>', page_html, flags=re.DOTALL)
        
        # update tags
        tags_html = f'<div class="badges mt-8" aria-label="Tools used">\n          <span class="badge">{lang}</span>\n        </div>'
        page_html = re.sub(r'<div class="badges mt-8" aria-label="Tools used">.*?</div>', tags_html, page_html, flags=re.DOTALL)
        
        # update link
        page_html = re.sub(r'href="https://github.com/Aditya-Ranjan23"[^>]*>(\s*View GitHub Repository)', f'href="{link}" target="_blank" rel="noopener noreferrer" class="read-more" style="justify-content: flex-start; font-size: 1.125rem;">\\1', page_html)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(page_html)
            
    # update case-studies.html
    cards_html = []
    for i, r in enumerate(repos):
        slug = slugify(r["name"])
        title = r["name"].replace("-", " ")
        desc = r["desc"] or f"A placeholder description for {title}."
        if len(desc) > 100:
            desc = desc[:97] + "..."
        lang = r["lang"] or "Unknown"
        delay = ' style="transition-delay: 150ms;"' if i % 2 != 0 else ''
        
        card = f'''      <a href="case-studies/{slug}.html" class="card col-6 reveal"{delay}>
        <div class="card-inner">
          <div class="card-header">
            <span class="tag">{lang}</span>
          </div>
          <h3>{title}</h3>
          <p>{desc}</p>
          <div class="badges" aria-label="Tools used">
            <span class="badge" style="padding: 0.25rem 0.75rem; font-size: 0.75rem;">{lang}</span>
          </div>
          <div class="card-footer mt-4">
            <span class="read-more">Read Case Study <span class="arrow">→</span></span>
          </div>
        </div>
      </a>'''
        cards_html.append(card)
        
    case_studies_path = os.path.join(base_dir, "case-studies.html")
    with open(case_studies_path, "r", encoding="utf-8") as f:
        cs_html = f.read()
        
    cs_html = re.sub(r'(<h2 class="section-title reveal">Projects</h2>\s*<div class="grid">)(.*?)(    </div>\s*</main>)', 
                     lambda m: m.group(1) + "\n" + "\n\n".join(cards_html) + "\n" + m.group(3), 
                     cs_html, flags=re.DOTALL)
                     
    with open(case_studies_path, "w", encoding="utf-8") as f:
        f.write(cs_html)
        
    # update index.html
    featured_names = [
        "Customer-Churn-Analysis-Dashboard-using-Power-BI",
        "E-Commerce-Sales-Analytics-SQL-Data-Warehouse-Power-BI-Dashboard",
        "Intelligent-IT-Ticketing",
        "Nexa-Analytics-AI"
    ]
    featured_repos = [r for r in repos if r["name"] in featured_names]
    
    latest_cards = []
    for r in featured_repos:
        slug = slugify(r["name"])
        title = r["name"].replace("-", " ")
        desc = r["desc"] or f"A placeholder description for {title}."
        if len(desc) > 100:
            desc = desc[:97] + "..."
        lang = r["lang"] or "Unknown"
        
        card = f'''        <a href="case-studies/{slug}.html" class="card col-6 reveal">
          <div class="card-inner">
            <div class="card-header">
              <span class="tag">{lang}</span>
            </div>
            <h3>{title}</h3>
            <p>{desc}</p>
            <div class="card-footer mt-4">
              <span class="read-more">Read Case Study <span class="arrow">→</span></span>
            </div>
          </div>
        </a>'''
        latest_cards.append(card)
        
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        idx_html = f.read()
        
    idx_html = re.sub(r'(<div class="grid" aria-label="Featured projects">)(.*?)(      </div>\s*</section>)',
                      lambda m: m.group(1) + "\n\n" + "\n\n".join(latest_cards) + "\n\n" + m.group(3),
                      idx_html, flags=re.DOTALL)
                      
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx_html)

if __name__ == "__main__":
    main()
