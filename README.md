- clone the repo
- run cd searchproject
- run . setup.sh
- run python manage.py runserver
- in the browser enter localhost:8000/search?q=<query>
- if you want to just test the application logic, just run python searchv1/search.py "the dark knight" and the response will print on the console
- (Optional) if you want the results from each source to be limited, use localhost:8000/search?q=<query>&limit=<limit>. Default limit is 5
- (Optional) if you want the results from a single source, use localhost:8000/search?q=<query>&source=<source>, by default results from all sources are returned. value of source can be any of these - ["google", "twitter", "duckduckgo", "wikipedia", "reddit"]
- Main application code is present in searchv1/search.py
