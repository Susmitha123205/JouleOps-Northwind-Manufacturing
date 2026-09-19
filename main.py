import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from hdbcli import dbapi
from datetime import datetime
from typing import Optional  
load_dotenv()  
app = FastAPI(title="JouleOps API")  
def get_db():     
    conn = dbapi.connect(         
        address=os.getenv("HANA_HOST"),         
        port=int(os.getenv("HANA_PORT")),         
        user=os.getenv("HANA_USER"),         
        password=os.getenv("HANA_PASSWORD"),         
        encrypt=True     
        )     
    return conn  
class MaterialRequest(BaseModel):     
    material_id: str     
    plant_code: str  
class SalesRequest(BaseModel):     
    region: str     
    date_from: str     
    date_to: str  
class CustomerRequest(BaseModel):     
    customer_id: str  
class TicketRequest(BaseModel):     
    material_id: str     
    plant_code: str     
    priority: str     
    assigned_team: str     
    description: str     
    created_by_role: str  
class InvoiceRequest(BaseModel):     
    customer_id: str  
@app.get("/health") 
def health():     
    return {"status": "ok"}  
@app.post("/api/material/details") 
def get_material(req: MaterialRequest):     
    conn = get_db()     
    cursor = conn.cursor()     
    cursor.execute("""         
        SELECT material_id, description, category, unit_price,                 
            stock_qty, safety_stock, plant_code         
        FROM MATERIALS          
        WHERE material_id = ? AND plant_code = ?     
    """, (req.material_id, req.plant_code))     
    row = cursor.fetchone()     
    conn.close()     
    if not row:         
        raise HTTPException(404, "Material not found")     
    return {         
        "material_id": row[0],         
        "description": row[1],         
        "category": row[2],         
        "unit_price": row[3],         
        "stock_qty": row[4],         
        "safety_stock": row[5],         
        "plant_code": row[6],         
        "is_below_safety": row[4] < row[5],         
        "tool": "get_material_details",         
        "source_tables": ["MATERIALS"]     
    }  
@app.post("/api/sales/orders") 
def get_sales(req: SalesRequest):     
    conn = get_db()     
    cursor = conn.cursor()     
    cursor.execute("""         
        SELECT customer_id, COUNT(*) as orders, SUM(qty) as total_qty         
        FROM SALES_ORDERS         
        WHERE region = ? AND status = 'Open' AND created_on BETWEEN ? AND ?         
        GROUP BY customer_id     
    """, (req.region, req.date_from, req.date_to))     
    rows = cursor.fetchall()     
    conn.close()     
    return {         
        "region": req.region,         
        "orders": [{"customer_id": r[0], "order_count": r[1], "total_qty": r[2]} for r in rows],         
        "tool": "get_open_sales_orders",         
        "source_tables": ["SALES_ORDERS"]     
    }  
@app.post("/api/customer/summary") 
def get_customer(req: CustomerRequest):     
    conn = get_db()     
    cursor = conn.cursor()     
    cursor.execute("""         
        SELECT c.customer_id, c.name, c.region, c.credit_limit, c.outstanding_amount,                
            COUNT(i.invoice_id) as inv_count, SUM(i.amount) as total_amt,                
            SUM(CASE WHEN i.status = 'Overdue' THEN i.amount ELSE 0 END) as overdue_amt         
        FROM CUSTOMERS c         
        LEFT JOIN INVOICES i ON c.customer_id = i.customer_id         
        WHERE c.customer_id = ?         
        GROUP BY c.customer_id, c.name, c.region, c.credit_limit, c.outstanding_amount     
    """, (req.customer_id,))     
    row = cursor.fetchone()     
    conn.close()     
    if not row:         
        raise HTTPException(404, "Customer not found")     
    return {         
        "customer_id": row[0],         
        "name": row[1],         
        "region": row[2],         
        "credit_limit": row[3],         
        "outstanding_amount": row[4],         
        "total_invoices": row[5] or 0,         
        "total_amount": row[6] or 0,         
        "overdue_amount": row[7] or 0,         
        "tool": "get_customer_summary",         
        "source_tables": ["CUSTOMERS", "INVOICES"]     
    }  
@app.post("/api/ticket/create") 
def create_ticket(req: TicketRequest, x_user_role: str = Header(...)):     
    if x_user_role not in ["PLANT_SUPERVISOR", "SALES_MANAGER", "FINANCE"]:         
        raise HTTPException(403, "InsuAicient permissions")          
    conn = get_db()     
    cursor = conn.cursor()          
    ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"          
    cursor.execute("""         
        INSERT INTO TICKETS (ticket_id, material_id, priority, assigned_team,                               
            description, status, created_on, created_by_role)         
        VALUES (?, ?, ?, ?, ?, 'Open', CURRENT_TIMESTAMP, ?)     
    """, (ticket_id, req.material_id, req.priority, req.assigned_team,            
        req.description, req.created_by_role))          
    masked_params = f"material={req.material_id}, priority={req.priority}, description=[MASKED]"          
    cursor.execute("""         
        INSERT INTO AUDIT_LOG (ts, user_role, tool_name, params_masked, outcome)         
        VALUES (CURRENT_TIMESTAMP, ?, 'create_ticket', ?, 'SUCCESS')     
    """, (x_user_role, masked_params))          
    conn.commit()     
    conn.close()          
    return {         
        "ticket_id": ticket_id,         
        "message": f"Ticket {ticket_id} created successfully",         
        "assigned_team": req.assigned_team,         
        "priority": req.priority,         
        "tool": "create_ticket",         
        "source_tables": ["TICKETS", "AUDIT_LOG"]     
    }  
@app.post("/api/invoices/overdue") 
def overdue_invoices(req: InvoiceRequest):     
    conn = get_db()     
    cursor = conn.cursor()     
    cursor.execute("""         
        SELECT invoice_id, amount, due_date, days_overdue, status         
        FROM INVOICES         
        WHERE customer_id = ? AND status = 'Overdue'         
        ORDER BY days_overdue DESC     
    """, (req.customer_id,))     
    rows = cursor.fetchall()     
    conn.close()          
    if not rows:         
        return {             
            "customer_id": req.customer_id,             
            "total_overdue": 0,             
            "invoices": [],             
            "tool": "summarize_overdue_invoices",             
            "source_tables": ["INVOICES"]         
        }          
    total = sum(r[1] for r in rows)     
    max_days = rows[0][3]          
    if max_days > 90:         
        recommendation = "ESCALATE_TO_LEGAL"     
    elif max_days > 60:         
        recommendation = "HOLD_SHIPMENTS"     
    else:         
        recommendation = "SEND_REMINDER"          
    return {         
        "customer_id": req.customer_id,         
        "total_overdue": total,         
        "max_days_overdue": max_days,         
        "recommendation": recommendation,         
        "invoices": [{"invoice_id": r[0], "amount": r[1], "due_date": str(r[2]),                        
            "days_overdue": r[3], "status": r[4]} for r in rows],         
        "tool": "summarize_overdue_invoices",         
        "source_tables": ["INVOICES"]     
    }