class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el carrito no existe en la sesión, inicialízalo
        if 'cart' not in request.session:
            request.session['cart'] = []

        response = self.get_response(request)
        return response