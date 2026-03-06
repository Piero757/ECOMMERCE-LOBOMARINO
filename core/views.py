from django.shortcuts import render, redirect
from django.contrib import messages

from .models import GalleryImage, ContactInfo, ContactMessage


def galeria_view(request):
    imagenes = GalleryImage.objects.filter(activo=True)
    categorias = dict(GalleryImage.CATEGORIA_CHOICES)

    return render(
        request,
        "galeria.html",
        {
            "imagenes": imagenes,
            "categorias": categorias,
        },
    )


def contacto_view(request):
    info = ContactInfo.objects.filter(activo=True).first()

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        if not nombre or not correo or not mensaje:
            messages.error(
                request,
                "Por favor completa al menos tu nombre, correo y mensaje.",
            )
        else:
            ContactMessage.objects.create(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                mensaje=mensaje,
            )
            messages.success(
                request,
                "Tu mensaje ha sido enviado. Nos pondremos en contacto contigo.",
            )
            return redirect("contacto")

    return render(
        request,
        "contacto.html",
        {
            "info": info,
        },
    )