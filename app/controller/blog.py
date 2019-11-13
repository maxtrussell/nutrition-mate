from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)

from app import flatpages

blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route("/blog", methods=["GET"])
def blog_index():
    published = [p for p in flatpages if 'published' in p.meta]
    return render_template("blog_index.html", pages=published)

@blog_bp.route("/blog/<page>", methods=["GET"])
def blog_handler(page: str):
    page = flatpages.get_or_404(page)
    if "published" in page.meta:
        return render_template("blog.html", page=page)
    flash("Page not yet published.")
    return redirect(url_for('blog_bp.blog_index'))
