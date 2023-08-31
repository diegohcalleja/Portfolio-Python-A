###############################################################
###            RETORNA LOS USUARIOS CON EL PASS             ###
###############################################################

def user_schema (user) -> dict:

    return {"id":str(user["_id"]),
            "username":user["username"],
            "full_name":user["full_name"],
            "email":user["email"],
            "disable":user["disable"],
            "password":user["password"]}

def users_schema (users)->list:
    return [user_schema(user) for user in users]

###############################################################
###            RETORNA LOS USUARIOS SIN EL PASS             ###
###############################################################

def user_schema_public (user) -> dict:

    return {"id":str(user["_id"]),
            "username":user["username"],
            "full_name":user["full_name"],
            "email":user["email"],
            "disable":user["disable"]}

def users_schema_public (users)->list:
    return [user_schema_public(user) for user in users]