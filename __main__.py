print("Wiki.py Server")

# Import http.server, cgi and sqlite3 libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import sqlite3

# Define the path to the database file that stores the wiki data
DB_FILE = "wiki.db"

# Define the path to the configuration file that stores the wiki options
CONFIG_FILE = "wikipy-options.py"

# Execute the contents of the configuration file and get the wiki options as a dictionary
options = {}
exec(open(CONFIG_FILE).read(), options)

# Define a function that creates the wiki table in the database if it does not exist
def create_table():
    print("Setting up database")
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SQL statement to create the table with two columns: title and content
    cur.execute("CREATE TABLE IF NOT EXISTS wiki (title TEXT PRIMARY KEY, content TEXT)")
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Define a function that reads the wiki data from the database and returns a dictionary
def read_wiki():
    print("Reading the wiki page")
    wiki = {}
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SQL statement to select all rows from the table
    cur.execute("SELECT * FROM wiki")
    # Fetch all the results as a list of tuples
    rows = cur.fetchall()
    # Loop through each row and store the title-content pair in the dictionary
    for row in rows:
        title, content = row
        wiki[title] = content
    # Close the connection and return the dictionary
    conn.close()
    return wiki

# Define a function that writes the wiki data to the database from a dictionary
def write_wiki(wiki):
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SQL statement to delete all rows from the table
    cur.execute("DELETE FROM wiki")
    # Loop through each key-value pair in the dictionary and insert them as rows in the table
    for key, value in wiki.items():
        cur.execute("INSERT INTO wiki (title, content) VALUES (?, ?)", (key, value))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Define a class that handles HTTP requests
class WikiHandler(BaseHTTPRequestHandler):

    # Define a method that handles GET requests
    def do_GET(self):
        # Read the wiki data from the database
        wiki = read_wiki()
        # Get the path from the request
        path = self.path.strip("/")
        # Check if the path is empty or "home"
        if path == "" or path == "home":
            # If so, send a 200 OK response with HTML content type
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Create an HTML string that lists all the pages as links
            html = f"<h1>{options['wikiViewerName']}</h1>"
            html += "<ul>"
            for key in wiki:
                html += f"<li><a href='/{key}'>{key}</a></li>"
            html += "</ul>"
            # Add a link to create or edit a page
            html += "<p><a href='/edit'>Create or edit a page</a></p>"
            # Write the HTML string as the response body
            self.wfile.write(html.encode())
        # Check if the path is "edit"
        elif path == "edit":
            # If so, send a 200 OK response with HTML content type
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Create an HTML string that shows a form to create or edit a page
            html = f"<h1>{options['wikiViewerName']}</h1>"
            html += "<h2>Edit <input type='text' name='title'></h2>"
            html += "<form method='POST'>"
            html += "<p><textarea name='content' rows='10' cols='50'></textarea></p>"
            html += "<p><input type='submit' value='Save changes'></p>"
            html += "</form>"
            # Write the HTML string as the response body
            self.wfile.write(html.encode())
            # Check if the path is an existing page title
            elif path in wiki:
            # If so, send a 200 OK response with HTML content type
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Create an HTML string that shows the page title and content
            html = f"<h1>{options['wikiViewerName']}</h1>"
            html += f"<h2>{path}</h2>"
            html += f"<p>{wiki[path]}</p>"
            # Add a link to edit or delete the page
            html += f"<p><a href='/edit?title={path}'>Edit this page</a></p>"
            html += f"<p><a href='/delete?title={path}'>Delete this page</a></p>"
            # Write the HTML string as the response body
            self.wfile.write(html.encode())
            else:
            # Return a 404 error if the path does not match any of the above cases
            self.send_error(404, "Page not found")
# Define a method that handles POST requests
def do_POST(self):
    # Read the wiki data from the database
    wiki = read_wiki()
    # Get the path from the request
    path = self.path.strip("/")
    # Check if the path is "edit"
    if path == "edit":
        # Parse the form data from the request body
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"}
        )
        # Get the title and content from the form data
        title = form.getvalue("title")
        content = form.getvalue("content")
        # Check if the title is empty
        if not title:
            # Return an error message if so
            self.send_error(400, "Invalid title")
            return
        else:
            # Add or update the page to the dictionary
            wiki[title] = content
            # Write the wiki data to the database
            write_wiki(wiki)
            # Redirect to the newly created or edited page
            self.send_response(303)
            self.send_header("Location", f"/{title}")
            self.end_headers()
    else:
        # Return a 405 error if the path is not "edit"
        self.send_error(405, "Method not allowed")

# Define a method that handles DELETE requests
def do_DELETE(self):
    # Read the wiki data from the database
    wiki = read_wiki()
    # Get the path from the request
    path = self.path.strip("/")
    # Check if the path is "delete"
    if path == "delete":
        # Parse the query string from the request URL
        query = cgi.parse_qs(self.path.split("?", 1)[1])
        # Get the title from the query string
        title = query.get("title", [""])[0]
        # Check if the title is an existing page title
        if title in wiki:
            # Delete the page from the dictionary
            del wiki[title]
            # Write the wiki data to the database
            write_wiki(wiki)
            # Redirect to the home page
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            # Return a 404 error if the title does not exist
            self.send_error(404, "Page not found")
    else:
        # Return a 405 error if the path is not "delete"
        self.send_error(405, "You must preform this operation through a specific page. See the Wiki.py docs for more information.")
# Define the main function that runs the wiki server
def main():
    # Create the wiki table in the database if it does not exist
    create_table()
    # Create an HTTP server object with the wiki handler class and a port number
    server = HTTPServer(("", 8000), WikiHandler)
    # Start the server and print a message
    print("Starting wiki server on http://localhost:8000")
    server.serve_forever()
