from webapp.app import create_app

app = create_app()
print(app.view_functions)
app.run()
