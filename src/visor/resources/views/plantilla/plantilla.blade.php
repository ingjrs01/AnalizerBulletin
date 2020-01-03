<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Visor</title>
    <meta name="viewport" content="width=with, initial-scale=1">
    <link href="http://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.0/css/all.css" integrity="sha384-lKuwvrZot6UHsBSfcMvOkWwlCMgc0TaWr+30HWe3a4ltaBwTZhyTEggF5tJv8tbt" crossorigin="anonymous">
    <script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
    <script src="{{ asset('js/functions.js') }}"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.css">
    <link rel="stylesheet" href="{{ asset('css/template.css') }}" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.js"></script>    
    <link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">
    <script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>    

    @yield('scripts')
</head>
<body> 
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
<span style="font-size: 2rem;color: white;"><i class="fas fa-bold"></i></span>&nbsp;&nbsp; <a class="navbar-brand" href="#">Bulletinator</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav">
      <a class="nav-item nav-link active" href="{{ route('noticias.index') }}">Noticias <span class="sr-only">(current)</span></a>
      <a class="nav-item nav-link" href=" {{ route('analisis.index') }} ">Análisis</a>
      <a class="nav-item nav-link" href=" {{ route('analizers.index') }} ">Analizadores</a>
    </div>
  </div>
</nav>

@yield('contenido')

</body>
</html>
