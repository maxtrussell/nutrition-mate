from flask import (
    Blueprint,
    render_template,
    request,
    flash,
)

from app import flatpages

blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route("/blog", methods=["GET"])
def blog_index():
    return render_template("blog_index.html", pages=flatpages)

@blog_bp.route("/blog/<page>", methods=["GET"])
def blog_handler(page: str):
    page = flatpages.get_or_404(page)
    return render_template("blog.html", page=page)
