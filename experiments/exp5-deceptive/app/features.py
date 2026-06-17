from .money import money
from .pad import format_date
from .slug import slugify_title

# NOTE: token.py / audit.py / footer.py are intentionally NOT imported or called
# by any feature below. They are dead code from the application's perspective.

def render_invoice(total_cents):        # uses money
    return f"INVOICE total: {money(total_cents)}"

def render_receipt(total_cents):        # uses money
    return f"RECEIPT: {money(total_cents)} paid"

def render_summary(total_cents):        # uses money
    return f"Summary - {money(total_cents)}"

def render_calendar(y, m, d):           # uses format_date -> _pad2
    return f"Calendar: {format_date(y, m, d)}"

def render_schedule(y, m, d):           # uses format_date -> _pad2
    return f"Scheduled for {format_date(y, m, d)}"

def export_csv_name(title):             # uses slugify_title
    return slugify_title(title) + ".csv"
