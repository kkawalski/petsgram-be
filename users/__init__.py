from app import api

auth_ns = api.namespace("auth", "Auth", "/auth")
profiles_ns = api.namespace("profiles", "Profiles", "/profiles")
