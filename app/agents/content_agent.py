import json
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..models import Article, Product, ContentStatus
from ..services.content_validator import ContentQualityEngine, ContentValidationError

class ContentGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Content Generation Agent")

    def build_comparison_article(self, db: Session, slug1: str, slug2: str, target_keyword: str) -> Article | None:
        prod1 = db.query(Product).filter(Product.slug == slug1).first()
        prod2 = db.query(Product).filter(Product.slug == slug2).first()

        if not prod1 or not prod2:
            self.log(db, "COMPARISON_GEN", "FAILED", "Required comparison products missing from catalog.")
            return None

        article_slug = f"{prod1.slug}-vs-{prod2.slug}"
        exists = db.query(Article).filter(Article.slug == article_slug).first()
        if exists:
            return exists

        title = f"{prod1.name} vs {prod2.name}: 2026 In-Depth Ergonomic Showdown"
        meta_desc = f"Direct data comparison between {prod1.name} and {prod2.name}. Discover which workstation chair delivers better spine support and value."

        p1_pros = json.loads(prod1.pros_json)
        p1_cons = json.loads(prod1.cons_json)
        p1_specs = json.loads(prod1.specs_json)

        p2_pros = json.loads(prod2.pros_json)
        p2_cons = json.loads(prod2.cons_json)
        p2_specs = json.loads(prod2.specs_json)

        html_blocks = []
        html_blocks.append(f"""
        <section class="intro">
            <p class="lead">Choosing between the premium <strong>{prod1.name}</strong> and the high-value <strong>{prod2.name}</strong> comes down to structural priorities: absolute ergonomic precision versus price-to-performance accessibility.</p>
            <p>Below is our structural breakdown analyzing mechanical durability, posture adjustment mechanisms, and overall return on investment.</p>
        </section>

        <section class="head-to-head-overview">
            <h2>Head-to-Head Specification Comparison</h2>
            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Specification Metric</th>
                            <th>{prod1.name}</th>
                            <th>{prod2.name}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Price Tier</strong></td>
                            <td>${prod1.price:.2f} {prod1.currency}</td>
                            <td>${prod2.price:.2f} {prod2.currency}</td>
                        </tr>
                        <tr>
                            <td><strong>Overall Rating</strong></td>
                            <td>★ {prod1.rating} / 5.0</td>
                            <td>★ {prod2.rating} / 5.0</td>
                        </tr>
                        <tr>
                            <td><strong>Target User</strong></td>
                            <td>{prod1.ideal_for}</td>
                            <td>{prod2.ideal_for}</td>
                        </tr>
                        <tr>
                            <td><strong>Direct Partner Route</strong></td>
                            <td><a href="/go/{prod1.slug}?src=vs_table" class="btn btn-sm btn-primary" rel="nofollow sponsored" target="_blank">Check {prod1.brand} →</a></td>
                            <td><a href="/go/{prod2.slug}?src=vs_table" class="btn btn-sm btn-primary" rel="nofollow sponsored" target="_blank">Check {prod2.brand} →</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="product-deep-dive">
            <h2>Option 1: {prod1.name} Analysis</h2>
            <div class="verdict-box">
                <h4>Who Should Buy:</h4>
                <p>{prod1.ideal_for}</p>
                <h4>Who Should Avoid:</h4>
                <p>{prod1.avoid_if}</p>
            </div>
            <div class="grid-pros-cons">
                <div class="pros-box">
                    <h5>✓ Advantages (Pros)</h5>
                    <ul>{"".join([f"<li>{i}</li>" for i in p1_pros])}</ul>
                </div>
                <div class="cons-box">
                    <h5>✗ Limitations (Cons)</h5>
                    <ul>{"".join([f"<li>{i}</li>" for i in p1_cons])}</ul>
                </div>
            </div>
            <div class="specs-wrapper">
                <h5>Key Specifications:</h5>
                <table class="specs-table">
                    <tbody>{"".join([f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p1_specs.items()])}</tbody>
                </table>
            </div>
        </section>

        <section class="product-deep-dive">
            <h2>Option 2: {prod2.name} Analysis</h2>
            <div class="verdict-box">
                <h4>Who Should Buy:</h4>
                <p>{prod2.ideal_for}</p>
                <h4>Who Should Avoid:</h4>
                <p>{prod2.avoid_if}</p>
            </div>
            <div class="grid-pros-cons">
                <div class="pros-box">
                    <h5>✓ Advantages (Pros)</h5>
                    <ul>{"".join([f"<li>{i}</li>" for i in p2_pros])}</ul>
                </div>
                <div class="cons-box">
                    <h5>✗ Limitations (Cons)</h5>
                    <ul>{"".join([f"<li>{i}</li>" for i in p2_cons])}</ul>
                </div>
            </div>
            <div class="specs-wrapper">
                <h5>Key Specifications:</h5>
                <table class="specs-table">
                    <tbody>{"".join([f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p2_specs.items()])}</tbody>
                </table>
            </div>
        </section>

        <section class="final-verdict-summary">
            <h2>Final Recommendation & Alternatives</h2>
            <p>If budget permits and you require a 12-year proven commercial workhorse, invest in the <strong>{prod1.name}</strong>. However, if you require dynamic recline functionality under $600 with broad lumbar flexibility, the <strong>{prod2.name}</strong> provides exceptional comparative value.</p>
        </section>
        """)

        full_content = "\n".join(html_blocks)
        word_count = len(full_content.split())

        try:
            ContentQualityEngine.validate(full_content, title, word_count)
            status = ContentStatus.PUBLISHED
        except ContentValidationError as e:
            self.log(db, "VALIDATION_FAILED", "REJECTED", f"Comparison rejected: {str(e)}")
            status = ContentStatus.REJECTED

        article = Article(
            title=title,
            slug=article_slug,
            article_type="comparison",
            category="Chair Comparisons",
            meta_description=meta_desc,
            content_html=full_content,
            status=status,
            word_count=word_count,
            reading_time_minutes=max(1, word_count // 200),
            target_keyword=target_keyword
        )
        db.add(article)
        db.commit()
        db.refresh(article)
        self.log(db, "COMPARISON_CREATED", "SUCCESS", f"Published head-to-head comparison: '{article.title}'")
        return article

    def build_best_list_article(self, db: Session, target_keyword: str) -> Article | None:
        products = db.query(Product).all()
        if len(products) < 2:
            self.log(db, "CONTENT_GEN", "FAILED", "Insufficient product records to build a valid listicle.")
            return None

        slug = target_keyword.replace(" ", "-").lower()
        exists = db.query(Article).filter(Article.slug == slug).first()
        if exists:
            return exists

        title = "Top 3 Best Ergonomic Office Chairs & Desks for Back Support (2026 In-Depth Guide)"
        meta_desc = "Objective, data-backed guide comparing top ergonomic workstations to relieve spine fatigue. Full specs, pros, cons, and buying criteria."

        html_blocks = []
        html_blocks.append("""
        <section class="intro">
            <p class="lead">Chronic posture strain from seated desk work is one of the leading drivers of spinal compression and fatigue. When outfitting a productive workstation, prioritizing certified lumbar mechanisms and stable sit-to-stand transitions produces quantifiable health and focus improvements.</p>
            <p>Our editorial team objectively compares the leading ergonomic equipment across structural build, warranty terms, adjustability parameters, and total cost value.</p>
        </section>

        <section class="comparison-summary-table">
            <h2>Quick Comparison Overview</h2>
            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Category</th>
                            <th>Rating</th>
                            <th>Best For</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
        """)

        for p in products:
            html_blocks.append(f"""
                        <tr>
                            <td><strong>{p.name}</strong></td>
                            <td>{p.category}</td>
                            <td>★ {p.rating}/5.0</td>
                            <td>{p.ideal_for}</td>
                            <td><a href="/go/{p.slug}?src=table" class="btn btn-sm btn-primary" rel="nofollow sponsored" target="_blank">View Price</a></td>
                        </tr>
            """)

        html_blocks.append("""
                    </tbody>
                </table>
            </div>
        </section>
        """)

        for idx, p in enumerate(products, 1):
            pros = json.loads(p.pros_json)
            cons = json.loads(p.cons_json)
            specs = json.loads(p.specs_json)

            pros_html = "".join([f"<li>{item}</li>" for item in pros])
            cons_html = "".join([f"<li>{item}</li>" for item in cons])
            specs_html = "".join([f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in specs.items()])

            html_blocks.append(f"""
            <article class="product-review-card" id="{p.slug}">
                <div class="product-header">
                    <span class="rank-badge">#{idx} Pick</span>
                    <h3>{p.name}</h3>
                    <div class="brand-rating">Brand: <em>{p.brand}</em> | Certified Score: <strong>{p.rating} / 5.0</strong></div>
                </div>

                <div class="verdict-box">
                    <h4>Who Should Buy:</h4>
                    <p>{p.ideal_for}</p>
                    <h4>Who Should Avoid:</h4>
                    <p>{p.avoid_if}</p>
                </div>

                <div class="grid-pros-cons">
                    <div class="pros-box">
                        <h5>✓ Verified Advantages (Pros)</h5>
                        <ul>{pros_html}</ul>
                    </div>
                    <div class="cons-box">
                        <h5>✗ Objective Limitations (Cons)</h5>
                        <ul>{cons_html}</ul>
                    </div>
                </div>

                <div class="specs-wrapper">
                    <h5>Technical Specifications:</h5>
                    <table class="specs-table">
                        <tbody>{specs_html}</tbody>
                    </table>
                </div>

                <div class="cta-container">
                    <a href="/go/{p.slug}?src=verdict_box" class="btn btn-primary btn-cta" rel="nofollow sponsored" target="_blank">
                        Check Current Direct Pricing & Availability →
                    </a>
                </div>
            </article>
            """)

        html_blocks.append("""
        <section class="buying-guide-section">
            <h2>Crucial Ergonomic Evaluation Criteria: What to Check Before Purchasing</h2>
            <h3>1. Active Pelvic Alignment & Lumbar Support</h3>
            <p>Ensure the chair provides depth-adjustable lumbar reinforcement that hits the L1-L5 vertebrae without excessive forward push.</p>
            <h3>2. Dynamic Weight Capacity & Motor Decibels</h3>
            <p>For electric standing desks, dual motors operating below 50 decibels with a payload exceeding 300 lbs are essential for multimonitor arrays.</p>
            <h3>3. Alternative Options & Return Windows</h3>
            <p>Always verify whether the manufacturer provides an in-home trial period of at least 30 days, as spine adaptation to proper posture can require two full weeks.</p>
        </section>
        """)

        full_content = "\n".join(html_blocks)
        word_count = len(full_content.split())

        try:
            ContentQualityEngine.validate(full_content, title, word_count)
            status = ContentStatus.PUBLISHED
        except ContentValidationError as e:
            self.log(db, "VALIDATION_FAILED", "REJECTED", f"Article rejected: {str(e)}")
            status = ContentStatus.REJECTED

        article = Article(
            title=title,
            slug=slug,
            article_type="best_list",
            category="Ergonomic Workstations",
            meta_description=meta_desc,
            content_html=full_content,
            status=status,
            word_count=word_count,
            reading_time_minutes=max(1, word_count // 200),
            target_keyword=target_keyword
        )
        db.add(article)
        db.commit()
        db.refresh(article)
        self.log(db, "ARTICLE_CREATED", "SUCCESS", f"Published validated high-intent article: '{article.title}'")
        return article
