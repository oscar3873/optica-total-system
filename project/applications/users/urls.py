from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

#
from . import views

app_name = 'users_app'

urlpatterns = [
    path(
        'signup/',
        views.UserCreateView.as_view(),
        name = 'signup'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name = 'login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name = 'logout'
    ),
    path(
        'update_password/',
        views.UpdatePasswordView.as_view(),
        name = 'update_password'
    ),

    # DJANGO RESET PASSWORD -> PARA CAMBIO DE PASSWORD OLVIDADA
    path(
        'reset_password/', 
        auth_views.PasswordResetView.as_view(
            email_template_name = 'users/email_reset_password.html',
                    # EMAIL PARA CAMBIAR PASSWORD 
                    #   -> EJEMPLO DJANGO : \venv-optica-total\Lib\site-packages\django\contrib\admin\templates\registration\password_reset_email.html
            template_name = 'users/reset_password.html', 
                    # FORMULARIO DE CAMBIO DE PASSWORD 
                    #   -> EJEMPLO DJANGO : \venv-optica-total\Lib\site-packages\django\contrib\admin\templates\registration\password_change_form.html
            success_url = reverse_lazy('users_app:password_reset_done'),
        ), 
        name='reset_password'
    ),
    path(
        'reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name = 'users/confirm_email.html', 
                    # AVISO DE EMAIL ENVIADO (CON BOTON VOLVER A LOGIN)
        ), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name = 'users/confirm_reset_password.html', 
                    # FORMULARIO DE CONFIRMACION DE CAMBIO DE PASSWORD 
                    #   -> EJEMPLO DJANGO : \venv-optica-total\Lib\site-packages\django\contrib\admin\templates\registration\password_reset_confirm.html
            success_url = reverse_lazy('users_app:password_reset_complete'),
        ), 
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name = 'users/complete_reset_password.html',
                    # AVISO DE CAMBIO EXITOSO (CON BOTON VOLVER A LOGIN) 
        ),
        name='password_reset_complete'
    ),
]
