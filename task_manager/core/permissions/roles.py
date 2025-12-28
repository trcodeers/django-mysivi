ROLE_PERMISSIONS = {
    "MANAGER": {
        "task:create",
        "task:assign",
        "task:update:any",
        "task:delete",
        "reportee:create",
        "task:view:any",
    },
    "REPORTEE": {
        "task:view:self",
        "task:update:self",
    },
}
