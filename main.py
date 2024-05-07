from app.api.application import Application
from app.api.routes.entry import entry
from app.api.routes.element_sets import elements

app = Application()
app.add_routes(entry)
app.add_routes(elements)
app.run_application(debug=True)