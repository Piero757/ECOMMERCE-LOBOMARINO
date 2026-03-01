from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 REDIRECCIÓN POR ROL
            if user.rol == "admin":
                return redirect("panel_admin")
            elif user.rol == "mozo":
                return redirect("panel_mozo")
            elif user.rol == "cajero":
                return redirect("panel_cajero")
            else:
                return redirect("panel_cliente")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def panel_admin(request):
    return render(request, "panel_admin.html")

@login_required
def panel_mozo(request):
    return render(request, "panel_mozo.html")

@login_required
def panel_cajero(request):
    return render(request, "panel_cajero.html")

@login_required
def panel_cliente(request):
    return render(request, "panel_cliente.html")