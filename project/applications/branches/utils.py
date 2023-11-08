from applications.branches.models import Branch


def set_branch_session(request):
    branch_actualy = request.session.get('branch_actualy') or request.user.branch.pk
    request.session['branch_actualy'] = int(branch_actualy)
    branch_actualy = Branch.objects.get(pk=branch_actualy)
    return branch_actualy