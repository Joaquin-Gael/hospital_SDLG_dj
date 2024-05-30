def user_info(request):
    """
    Esta función proporciona información del usuario actual para ser utilizada en las plantillas.
    Retorna un diccionario con el nombre de usuario, la fecha de nacimiento y las primeras letras del nombre y apellido del usuario.
    Si el usuario no está autenticado, devuelve información predeterminada para un usuario anónimo.
    """
    try:
        if request.user.is_authenticated:
            username = request.user.nombre + ' ' + request.user.apellido
            fecha_de_nacimiento = request.user.fecha_nacimiento
            leter1 = [char for char in request.user.nombre][0]
            leter2 = [char for char in request.user.apellido][0]
        else:
            username = 'Anónimo'
            fecha_de_nacimiento = None
            leter1 = 'A'
            leter2 = 'A'
    
        return {
            'username': username,
            'fecha_de_nacimiento': fecha_de_nacimiento,
            'letras': leter1 + leter2
        }
    except Exception as err:
        print(err)
        return {}
