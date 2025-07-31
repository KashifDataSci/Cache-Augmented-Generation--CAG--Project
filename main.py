from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.routers.data_handler import router
app = FastAPI(
    title="CAG Project API - Chat with your PDF",
    description="Advanced API for uploading PDFs, querying content via LLM, and managing data with modern UI.",
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CAG Project - Chat with your PDF</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-container">
                <div class="nav-brand">
                    <i class="fas fa-file-pdf brand-icon"></i>
                    <span class="brand-text">CAG Project</span>
                </div>
                <div class="nav-menu">
                    <a href="#home" class="nav-link active">Home</a>
                    <a href="#upload" class="nav-link">Upload</a>
                    <a href="#chat" class="nav-link">Chat</a>
                    <a href="/docs" class="nav-link">Docs</a>
                </div>
                <input type="checkbox" id="nav-toggle" class="nav-toggle-checkbox">
                <label for="nav-toggle" class="nav-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </label>
            </div>
        </nav>

        <!-- Hero Section -->
        <section id="home" class="hero">
            <div class="hero-container">
                <div class="hero-content">
                    <h1 class="hero-title">
                        Chat with Your <span class="gradient-text">PDF Documents</span>
                    </h1>
                    <p class="hero-subtitle">
                        Upload your PDF files and ask intelligent questions using advanced AI. 
                        Get instant answers from your documents with Cache Augmented Generation.
                    </p>
                    <div class="hero-buttons">
                        <a href="#upload" class="btn btn-primary">
                            <i class="fas fa-upload"></i>
                            Start Uploading
                        </a>
                        <a href="#chat" class="btn btn-secondary">
                            <i class="fas fa-comments"></i>
                            Try Chat
                        </a>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="floating-card">
                        <i class="fas fa-file-pdf pdf-icon"></i>
                        <div class="card-content">
                            <h3>Smart PDF Analysis</h3>
                            <p>AI-powered document understanding</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features">
            <div class="container">
                <h2 class="section-title">Powerful Features</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-cloud-upload-alt"></i>
                        </div>
                        <h3>Easy Upload</h3>
                        <p>Upload your PDF files with instant processing and text extraction using our API endpoints.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-brain"></i>
                        </div>
                        <h3>AI-Powered Chat</h3>
                        <p>Ask natural language questions and get intelligent answers from your documents.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-lightning-bolt"></i>
                        </div>
                        <h3>Fast Processing</h3>
                        <p>Cache Augmented Generation ensures lightning-fast response times.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h3>Secure & Private</h3>
                        <p>Your documents are processed securely with privacy protection.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- API Usage Section -->
        <section id="upload" class="api-section">
            <div class="container">
                <h2 class="section-title">API Usage Guide</h2>
                <div class="api-grid">
                    <div class="api-card">
                        <div class="api-step">1</div>
                        <h3>Upload PDF</h3>
                        <div class="code-block">
                            <code>POST /api/v1/upload/{uuid}</code>
                        </div>
                        <p>Upload your PDF file with a unique UUID. The system will extract and cache the text content.</p>
                        <div class="api-example">
                            <strong>Example:</strong><br>
                            <code>curl -X POST "http://127.0.0.1:8002/api/v1/upload/123e4567-e89b-12d3-a456-426614174000" -F "file=@document.pdf"</code>
                        </div>
                    </div>
                    
                    <div class="api-card">
                        <div class="api-step">2</div>
                        <h3>Query Document</h3>
                        <div class="code-block">
                            <code>GET /api/v1/query/{uuid}?query=your_question</code>
                        </div>
                        <p>Ask questions about your uploaded document using natural language.</p>
                        <div class="api-example">
                            <strong>Example:</strong><br>
                            <code>curl "http://127.0.0.1:8002/api/v1/query/123e4567-e89b-12d3-a456-426614174000?query=What is the main topic?"</code>
                        </div>
                    </div>
                    
                    <div class="api-card">
                        <div class="api-step">3</div>
                        <h3>Manage Documents</h3>
                        <div class="code-block">
                            <code>GET /api/v1/list_uuids</code><br>
                            <code>DELETE /api/v1/data/{uuid}</code>
                        </div>
                        <p>List all your documents or delete specific ones when no longer needed.</p>
                        <div class="api-example">
                            <strong>List:</strong> <code>curl "http://127.0.0.1:8002/api/v1/list_uuids"</code><br>
                            <strong>Delete:</strong> <code>curl -X DELETE "http://127.0.0.1:8002/api/v1/data/123e4567-e89b-12d3-a456-426614174000"</code>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Interactive Demo Section -->
        <section id="chat" class="demo-section">
            <div class="container">
                <h2 class="section-title">Interactive API Documentation</h2>
                <div class="demo-container">
                    <div class="demo-card">
                        <div class="demo-header">
                            <i class="fas fa-code"></i>
                            <h3>Swagger UI</h3>
                        </div>
                        <p>Explore and test all API endpoints with our interactive Swagger documentation.</p>
                        <a href="/docs" class="btn btn-primary" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Open Swagger UI
                        </a>
                    </div>
                    
                    <div class="demo-card">
                        <div class="demo-header">
                            <i class="fas fa-book"></i>
                            <h3>ReDoc</h3>
                        </div>
                        <p>View comprehensive API documentation with detailed schemas and examples.</p>
                        <a href="/redoc" class="btn btn-secondary" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Open ReDoc
                        </a>
                    </div>
                </div>
                
            </div>
        </section>

        <!-- Stats Section -->
        <section class="stats-section">
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">50MB</div>
                        <div class="stat-label">Max File Size</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">PDF</div>
                        <div class="stat-label">Supported Format</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-number">REST</div>
                        <div class="stat-label">API Architecture</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-section">
                        <h3>CAG Project</h3>
                        <p>Empowering insights from your documents with AI-powered chat capabilities through our advanced REST API.</p>
                    </div>
                    <div class="footer-section">
                        <h4>API Endpoints</h4>
                        <ul>
                            <li><a href="/docs">Interactive Documentation</a></li>
                            <li><a href="/redoc">API Reference</a></li>
                            <li><code>/api/v1/upload/{uuid}</code></li>
                            <li><code>/api/v1/query/{uuid}</code></li>
                        </ul>
                    </div>
                    <div class="footer-section">
                        <h4>Features</h4>
                        <ul>
                            <li>PDF Text Extraction</li>
                            <li>AI-Powered Queries</li>
                            <li>Document Management</li>
                            <li>RESTful API Design</li>
                        </ul>
                    </div>
                    <div class="footer-section">
                        <h4>Technical Stack</h4>
                        <
                        
                        
                        >
                            <li>FastAPI Framework</li>
                            <li>OpenRouter AI Integration</li>
<li>PyPDF Text Processing</li>
                            <li>Cache Augmented Generation</li>
                        </ul>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p>&copy; 2025 CAG Project. All rights reserved. | Server running on port 8001</p>
                </div>
            </div>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, host="127.0.0.1", port=8001
    )