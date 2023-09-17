from .models import Branch  # Asegúrate de importar tu modelo Branch

def branches(request):
    # Obtén las sucursales disponibles y devuélvelas en el contexto
    branches = Branch.objects.all()
    branch_user = request.user.branch
    return {'branches': branches, "branch_user": branch_user}