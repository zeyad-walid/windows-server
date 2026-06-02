import sys

try:
    from pyad import adou
except ImportError:
    print("Error: Please run 'pip install pyad pywin32'")
    sys.exit(1)

domain_dn = "dc=zeyad,dc=local"
departments = ["IT", "Finance", "Sales"]

new_users = [
    {"username": "ali_sales", "firstname": "Ali", "lastname": "Ahmed", "department": "Sales"},
    {"username": "omar_fin", "firstname": "Omar", "lastname": "Hassan", "department": "Finance"},
    {"username": "zeyad_it", "firstname": "Zeyad", "lastname": "Walid", "department": "IT"}
]

print("Starting deployment...")

# 1. Create OUs if they don't exist
for dept in departments:
    try:
        target_ou_dn = f"ou={dept},{domain_dn}"
        adou.ADOrganizationalUnit.from_dn(target_ou_dn)
        print(f"OU [{dept}] already exists.")
    except Exception:
        try:
            adou.ADOrganizationalUnit.create(dept, base_dn=domain_dn)
            print(f"Created OU: {dept}")
        except Exception as e:
            print(f"Failed to create OU {dept}: {e}")

# 2. Create Users
for user in new_users:
    try:
        target_ou_dn = f"ou={user['department']},{domain_dn}"
        target_ou = adou.ADOrganizationalUnit.from_dn(target_ou_dn)
        
        created_user = target_ou.create_user(
            sAMAccountName=user['username'],
            password="Password123!"
        )
        
        created_user.update_attribute("givenName", user['firstname'])
        created_user.update_attribute("sn", user['lastname'])
        created_user.update_attribute("department", user['department'])
        
        print(f"User [{user['username']}] created in {user['department']}.")
    except Exception as e:
        print(f"Failed to create user {user['username']}: {e}")

print("Done.")
