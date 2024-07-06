# Inventory API Service

## User Credentials
- **Superuser**: 
  - Username: `kush`
  - Password: `1234`
- **Staff User**: 
  - Username: `staff`
  - Password: `user@123`
- **Normal User**: 
  - Username: `User`
  - Password: `user@123`

This API service manages an inventory of cuboid boxes in a store. It supports CRUD operations with specific permissions and constraints.

### How to Run 🏃‍♀️

1. **Clone the project**:
    ```shell
    git clone https://github.com/kush8789/Spinny_Assignment.git
    ```

2. **Create a virtual environment**:
    ```shell
    python -m venv venv
    ```

3. **Activate the environment**:
    ```shell
    # On Linux or macOS
    source venv/bin/activate
    
    # On Windows
    .\venv\Scripts\activate
    ```

5. **Install dependencies**:
    ```shell
    pip install -r requirements.txt
    ```

6. **Apply the migrations**:
    ```shell
    python manage.py migrate
    ```

7. **Run the server**:
    ```shell
    python manage.py runserver
    ```

## Features

### 1. Add Box
- **Endpoint**: `api/boxes/`
- **Permissions**: Staff user
- **Data**: Length, breadth, height

### 2. Update Box
- **Endpoint**: `api/boxes/<id>/`
- **Permissions**: Staff user
- **Data**: Length, breadth, height

### 3. List All Boxes
- **Endpoint**: `api/boxes/`
- **Permissions**: Any user
- **Filters**: Length, breadth, height, area, volume, created by, created before/after

### 4. List My Boxes
- **Endpoint**: `api/boxes/?created_by=<username>`
- **Permissions**: Staff user
- **Filters**: Length, breadth, height, area, volume

### 5. Delete Box
- **Endpoint**: `api/boxes/<id>/`
- **Permissions**: Box creator

### Constraints
1. Average area of all boxes ≤ `A1` (default: 100).
2. Average volume of user-added boxes ≤ `V1` (default: 1000).
3. Total boxes added in a week ≤ `L1` (default: 100).
4. Total boxes added by a user in a week ≤ `L2` (default: 50).


## Deployment
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Create a superuser: `python manage.py createsuperuser`.
5. Start the server: `python manage.py runserver`.
6. Deploy to a hosting service like PythonAnywhere or Render.com.