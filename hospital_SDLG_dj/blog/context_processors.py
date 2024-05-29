def user_info(request):
    try:
        if request.user.is_authenticated:
            username = request.user.nombre + ' ' + request.user.apellido
            fecha_de_nacimiento = request.user.fecha_nacimiento
            leter1=[char for char in request.user.nombre][0]
            leter2=[char for char in request.user.apellido][0]
        else:
            username = 'Anónimo'
    
        return {
            'username': username,
            'fecha_de_nacimiento':fecha_de_nacimiento,
            'letras':leter1 + leter2
        }
    except Exception as err:
        print(err)
        return {}