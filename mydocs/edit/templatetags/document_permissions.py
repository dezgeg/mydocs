from mydocs.edit.models import Permission
from django import template
register = template.Library()

# template syntax: {% if user|can_modify:some_document %}
def check_perm(min_required_perm):
    def retval(user, document):
        return "ok" if document.get_permission_for(user) >= min_required_perm else ""
    return retval
    
register.filter('can_modify', check_perm(Permission.Modify))
register.filter('can_delete', check_perm(Permission.Owner))
register.filter('can_change_perms', check_perm(Permission.ChangePerms))
