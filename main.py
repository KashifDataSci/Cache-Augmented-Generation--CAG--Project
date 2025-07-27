from fastapi import FastAPI
from src.routers.data_handler import router
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="CAG Project API Chatwith your pdf",
    description="API for uploading PDFs,querying content via LLM, and managing data.",
    version="0.1.0",
)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["Data Handling And Chat with PDF"],
)

@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>CAG Project API - Chat with your PDF</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #4CAF50; /* Green */
                --secondary-color: #2196F3; /* Blue */
                --text-color: #333;
                --background-color: #f4f7f6;
                --card-background: #ffffff;
                --border-color: #e0e0e0;
                --shadow-light: rgba(0, 0, 0, 0.05);
                --shadow-medium: rgba(0, 0, 0, 0.1);
            }

            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--background-color);
                color: var(--text-color);
                line-height: 1.6;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
                padding: 20px;
                box-sizing: border-box;
            }

            .container {
                background-color: var(--card-background);
                border-radius: 10px;
                box-shadow: 0 4px 15px var(--shadow-medium);
                padding: 40px;
                max-width: 900px;
                width: 100%;
                box-sizing: border-box;
            }

            header {
                text-align: center;
                padding-bottom: 20px;
                margin-bottom: 30px;
                border-bottom: 3px solid var(--primary-color);
            }

            h1 {
                color: var(--primary-color);
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                font-weight: 700;
            }

            header p {
                color: #555;
                font-size: 1.1rem;
                margin-top: 0;
            }

            header p em {
                color: var(--secondary-color);
                font-weight: 400;
            }

            h2, h3 {
                color: var(--primary-color);
                margin-top: 1.5rem;
                margin-bottom: 0.8rem;
                font-weight: 700;
            }

            section p {
                margin-bottom: 1rem;
            }

            ul {
                list-style: none;
                padding: 0;
                margin: 1.5rem 0;
            }

            ul li {
                background-color: var(--background-color);
                padding: 12px 20px;
                margin-bottom: 8px;
                border-left: 5px solid var(--secondary-color);
                border-radius: 5px;
                box-shadow: 0 2px 5px var(--shadow-light);
                transition: transform 0.2s ease-in-out;
            }

            ul li:hover {
                transform: translateX(5px);
            }

            code {
                background-color: #e8f5e9; /* Lighter green */
                color: var(--primary-color);
                padding: 4px 8px;
                border-radius: 5px;
                font-family: 'Roboto Mono', monospace;
                font-size: 0.95rem;
            }

            a {
                color: var(--secondary-color);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s ease-in-out;
            }

            a:hover {
                color: var(--primary-color);
                text-decoration: underline;
            }

            footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid var(--border-color);
                font-size: 0.85rem;
                color: #777;
            }

            /* Responsive adjustments */
            @media (max-width: 768px) {
                .container {
                    padding: 25px;
                }
                h1 {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>CAG Project API</h1>
                <p><em>Chat with your PDF</em></p>
                <p><strong>Version 0.1.0</strong></p>
            </header>
            <section>
                <h2>Welcome!</h2>
                <p>
                    This API allows you to upload PDF documents, query their content using a Large Language Model (LLM),
                    and efficiently manage your data.
                </p>
                <h3>API Features:</h3>
                <ul>
                    <li>Upload and process PDF files securely.</li>
                    <li>Ask natural language questions about your PDF's content.</li>
                    <li>Update existing document data.</li>
                    <li>Delete specific document data when no longer needed.</li>
                    <li>Retrieve a list of all stored document IDs (UUIDs).</li>
                </ul>
                <h3>Getting Started:</h3>
                <p>Interact with the API endpoints using the following base prefix:</p>
                <p><code>/api/v1/</code></p>
                <p>
                    Explore detailed API documentation, including endpoint specifics and request/response examples, at the
                    interactive API docs:
                    <br><a href="/docs" target="_blank">/docs</a> (Swagger UI)
                    <br><a href="/redoc" target="_blank">/redoc</a> (ReDoc)
                </p>
            </section>
            <footer>
                <p>&copy; 2025 CAG Project. Empowering insights from your documents.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, host="127.0.0.1", port=8001
    )