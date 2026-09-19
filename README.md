# JouleOps @ NorthWind Manufacturing

## SAP BTP AI Enterprise Assistant

JouleOps is an AI-powered enterprise assistant developed for NorthWind Manufacturing using SAP BTP, SAP Joule, SAP HANA Cloud, Python FastAPI, and MCP.

The system enables employees to interact with enterprise data using natural-language requests. It can retrieve business information from SAP HANA Cloud and support business workflows such as maintenance ticket creation through integrated backend services.

## Project Objective

The objective of JouleOps is to reduce manual effort in enterprise operations by allowing employees to interact with business data and workflows through a natural-language AI assistant.

Instead of manually searching through different systems or executing multiple SAP transactions, users can make requests in natural language and the assistant can select the appropriate tools and retrieve or process the required information.

## Key Features

- Natural-language interaction with enterprise data
- Enterprise data retrieval from SAP HANA Cloud
- Material information retrieval
- Customer information retrieval
- Sales order information retrieval
- Invoice information retrieval
- Maintenance ticket creation
- Role-based access
- Audit logging
- REST API backend
- MCP server integration
- SAP Joule integration
- SAP BTP Destination configuration
- Secure connection between services
- Structured enterprise data management

## Technologies Used

### SAP Technologies

- SAP BTP
- SAP Joule
- SAP Joule Studio
- SAP HANA Cloud
- SAP BTP Destinations

### Backend Technologies

- Python
- FastAPI
- REST APIs
- MCP (Model Context Protocol)
- hdbcli
- SQL

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Swagger UI
- cURL
- ngrok

## System Architecture

```text
                    Employee
                       |
                       v
                SAP Joule / Joule Studio
                       |
                       v
                 JouleOps Agent
                       |
                +------+------+
                |             |
                v             v
          MCP Server      FastAPI REST API
                |             |
                +------+------+
                       |
                       v
                 SAP HANA Cloud
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
    Materials      Customers      Sales Orders
        |              |              |
        +--------------+--------------+
                       |
                       v
              Invoices / Tickets
```

## Project Workflow

1. The employee submits a request using natural language through SAP Joule.
2. The JouleOps agent understands the request.
3. The appropriate backend tool or MCP tool is selected.
4. The FastAPI backend processes the request.
5. Required enterprise data is retrieved from SAP HANA Cloud.
6. The requested information is returned to the user.
7. For supported workflows, maintenance tickets can be created.
8. Relevant activities can be recorded through audit logging.

## Database

The project uses **SAP HANA Cloud** for enterprise data storage.

The database contains business entities such as:

- Materials
- Customers
- Sales Orders
- Invoices
- Tickets
- Audit Logs

Sample CSV data is available inside the `data` directory for development and testing.

## MCP Integration

The project uses **Model Context Protocol (MCP)** to expose backend capabilities as tools that can be used by the AI assistant.

MCP connects the AI assistant with enterprise operations and allows appropriate tools to be selected based on the user's request.

## SAP BTP Integration

SAP BTP is used as the cloud platform for integrating the AI assistant, backend services, destinations, and SAP HANA Cloud.

The project uses **SAP BTP Destinations** to configure communication between the SAP Joule environment and backend services.

## Project Structure

```text
JouleOps-Northwind-Manufacturing/
│
├── data/
│   ├── data_audit_log.csv
│   ├── data_customers.csv
│   ├── data_invoices.csv
│   ├── data_materials.csv
│   ├── data_sales_orders.csv
│   └── data_tickets.csv
│
├── generate_seed_data.py
├── main.py
├── mcp_server.py
├── requirements.txt
├── JouleOps_Capstone_Documentation.pdf
├── JouleOps_Capstone.pptx
└── README.md
```

## Project Highlights

- SAP BTP-based enterprise AI application
- SAP Joule and Joule Studio integration
- SAP HANA Cloud database integration
- Python FastAPI backend
- MCP-based tool integration
- Enterprise data retrieval
- Maintenance ticket workflow
- Role-based access
- Audit logging
- REST API development
- Structured enterprise data management

## Documentation

Detailed project documentation is available in:

**JouleOps_Capstone_Documentation.pdf**

The documentation covers:

- Project architecture
- SAP BTP integration
- SAP HANA Cloud
- FastAPI backend
- MCP integration
- SAP Joule integration
- BTP Destinations
- Testing
- Project workflow

## Project Presentation

The project presentation is available in:

**JouleOps_Capstone.pptx**

## Author

**Susmitha Boga**

B.Tech – Computer Science and Engineering

### Profiles

- GitHub: https://github.com/Susmitha123205
- LinkedIn: https://www.linkedin.com/in/susmitha11/
- Portfolio: https://susmithabogaportfolio.netlify.app/

## License

This project was developed as an academic/capstone project for learning and demonstration purposes.

## Backend API

The FastAPI backend provides REST endpoints for interacting with enterprise data and business operations.

### API Operations

- Health check
- Material details
- Sales order information
- Customer summary
- Maintenance ticket creation

The API can be tested using **Swagger UI**, **cURL**, or other REST API clients.

### Run the Backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Local Development

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate on Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the FastAPI Server

```bash
uvicorn main:app --reload
```

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

## Security

Sensitive configuration such as database credentials, passwords, API keys, and environment variables should not be committed to GitHub.

The project uses a `.gitignore` file to exclude:

```text
.env
.venv/
__pycache__/
*.pyc
```

This helps prevent sensitive credentials and unnecessary virtual-environment files from being uploaded to the repository.
