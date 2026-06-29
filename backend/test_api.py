import json
import urllib.request
import urllib.error
import time

BASE_URL = "http://localhost:5000/api"
headers = {"Content-Type": "application/json"}
token = None

# Custom test email with timestamp to avoid duplicates
timestamp = int(time.time())
test_email = f"testuser_{timestamp}@gims.com"
test_password = "password123"

def make_request(path, method="GET", body=None, auth_token=None):
    url = f"{BASE_URL}{path}"
    req_headers = headers.copy()
    if auth_token:
        req_headers["Authorization"] = f"Bearer {auth_token}"
        
    data = None
    if body:
        data = json.dumps(body).encode("utf-8")
        
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = json.loads(response.read().decode("utf-8"))
            return status_code, response_body
    except urllib.error.HTTPError as error:
        status_code = error.getcode()
        try:
            response_body = json.loads(error.read().decode("utf-8"))
        except Exception:
            response_body = error.reason
        return status_code, response_body

def run_tests():
    global token
    print("Starting GIMS API validation tests...\n")

    # Test 1: Register User (Success)
    print("Test 1: Registering new user...")
    body = {
        "name": "Manoj M",
        "email": test_email,
        "password": test_password,
        "role": "admin"
    }
    status, res = make_request("/auth/register", "POST", body)
    assert status == 201, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Registered user ID: {res['data']['user']['id']}\n")

    # Test 2: Register User (Validation Error - Missing password)
    print("Test 2: Registering user with missing password (validation check)...")
    body = {
        "name": "Manoj M",
        "email": f"fail_{timestamp}@gims.com"
    }
    status, res = make_request("/auth/register", "POST", body)
    assert status == 400, f"Expected 400, got {status}"
    print(f"  [SUCCESS] Code: {status}. Validation messages: {res['errors']}\n")

    # Test 3: Register User (Duplicate Email)
    print("Test 3: Registering user with duplicate email...")
    body = {
        "name": "Manoj M",
        "email": test_email,
        "password": test_password
    }
    status, res = make_request("/auth/register", "POST", body)
    assert status == 400, f"Expected 400, got {status}"
    print(f"  [SUCCESS] Code: {status}. Message: {res['message']}\n")

    # Test 4: Login User (Success)
    print("Test 4: Logging in...")
    body = {
        "email": test_email,
        "password": test_password
    }
    status, res = make_request("/auth/login", "POST", body)
    assert status == 200, f"Failed: {status} - {res}"
    token = res["data"]["token"]
    print(f"  [SUCCESS] Code: {status}. Received JWT token successfully.\n")

    # Test 5: Login User (Invalid Password)
    print("Test 5: Logging in with incorrect password...")
    body = {
        "email": test_email,
        "password": "wrongpassword"
    }
    status, res = make_request("/auth/login", "POST", body)
    assert status == 401, f"Expected 401, got {status}"
    print(f"  [SUCCESS] Code: {status}. Message: {res['message']}\n")

    # Test 6: GET Products (Public)
    print("Test 6: Fetching products list (public route)...")
    status, res = make_request("/products")
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Items found: {len(res['data'])}\n")

    # Test 7: POST Product (Unauthorized)
    print("Test 7: Attempting to create a product without a token...")
    product_body = {
        "name": "Flashed Rice",
        "departmentId": "grocery",
        "stock": 150,
        "unit": "Kg",
        "cost": 65.50
    }
    status, res = make_request("/products", "POST", product_body)
    assert status == 401, f"Expected 401, got {status}"
    print(f"  [SUCCESS] Code: {status}. Message: {res['message']}\n")

    # Test 8: POST Product (Success & Status Recalculation)
    print("Test 8: Creating a product with stock = 150 (should auto-calculate status: 'in-stock')...")
    status, res = make_request("/products", "POST", product_body, token)
    assert status == 201, f"Failed: {status} - {res}"
    product_id = res["data"]["id"]
    assert res["data"]["status"] == "in-stock", f"Expected in-stock, got {res['data']['status']}"
    print(f"  [SUCCESS] Code: {status}. Product: {res['data']['name']}. Auto status: {res['data']['status']}\n")

    # Test 9: POST Product (Validation: Invalid department)
    print("Test 9: Creating product with non-existent department...")
    bad_product_body = product_body.copy()
    bad_product_body["departmentId"] = "electronics-bad"
    status, res = make_request("/products", "POST", bad_product_body, token)
    assert status == 400, f"Expected 400, got {status}"
    print(f"  [SUCCESS] Code: {status}. Validation messages: {res['errors']}\n")

    # Test 10: PUT Product (Stock Update & Transaction Delta Log)
    print("Test 10: Updating product stock: 150 -> 15 (should auto-calculate status: 'critical' and register delta: -135)...")
    update_body = product_body.copy()
    update_body["stock"] = 15
    status, res = make_request(f"/products/{product_id}", "PUT", update_body, token)
    assert status == 200, f"Failed: {status} - {res}"
    assert res["data"]["status"] == "critical", f"Expected critical, got {res['data']['status']}"
    print(f"  [SUCCESS] Code: {status}. New status: {res['data']['status']}. Stock updated successfully.\n")

    # Test 11: GET Dashboard Summary
    print("Test 11: Fetching dashboard summary stats...")
    status, res = make_request("/dashboard/summary", "GET", auth_token=token)
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Total inventory value: ${res['data']['totalValue']:.2f}\n")

    # Test 12: GET Dashboard Recent Activity
    print("Test 12: Fetching dashboard recent activity...")
    status, res = make_request("/dashboard/recent-activity", "GET", auth_token=token)
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Last log action: '{res['data'][0]['action']}' details: {res['data'][0]['details']}\n")

    # Test 13: GET Alerts (Critical)
    print("Test 13: Fetching critical alerts...")
    status, res = make_request("/alerts/critical", "GET", auth_token=token)
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Critical alerts count: {len(res['data'])}\n")

    # Test 14: GET Reports Summary (Combined Breakdown)
    print("Test 14: Fetching reports combined summary...")
    status, res = make_request("/reports/summary", "GET", auth_token=token)
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Status breakdown: {res['data']['statusDistribution']}\n")

    # Test 15: DELETE Product
    print("Test 15: Deleting test product...")
    status, res = make_request(f"/products/{product_id}", "DELETE", auth_token=token)
    assert status == 200, f"Failed: {status} - {res}"
    print(f"  [SUCCESS] Code: {status}. Message: {res['message']}\n")

    print("All verification tests passed successfully!")

if __name__ == "__main__":
    run_tests()

