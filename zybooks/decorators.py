from functools import wraps
from django.http import JsonResponse
from http.cookies import SimpleCookie

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            cookie_header = dict(request.headers).get("Cookie", "")
            cookie = SimpleCookie(cookie_header)

            role = cookie.get("role").value if "role" in cookie else None
            user_id = cookie.get("user_id").value if "user_id" in cookie else None

            print("Role:", role)
            print("User ID:", user_id)

            if not role or role not in allowed_roles:
                return JsonResponse({"error": "Permission denied"}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator