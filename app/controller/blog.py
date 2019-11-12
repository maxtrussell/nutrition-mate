from flask import (
    Blueprint,
    render_template,
    request,
    flash,
)

blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route("/blog/<page>", methods=["GET"])
def blog_handler(page: str):
    template_file = page + ".html"
    return render_template(template_file)
