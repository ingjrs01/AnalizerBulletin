@extends('plantilla.plantilla')

@section('contenido')
<div class="container-fluid registerinicio">
    <div class="row">
        <div class="col-md-6 register-left register-left1">
            <img src="{{asset('img/calendario.png')}}" alt=""/>
        </div>    
        <div class="col-md-6 register-left">            
            <h3>Bienvenid@</h3>
            <p>Por favor llena los datos correctamente en el sistema!</p>            
        </div>    
    </div>
</div>

<div class="row">
    
</div>

<div class="container-fluid ">

<form method="POST" action="{{route('home')}}">
@csrf
    <div class="form-group col-md-2">
        <label for="fecha">Fecha</label>
        <input type="text" class="form-control" id="fecha" placeholder="Fecha" value="{{$analisis->analysis_date}}">
    </div>

    <div class="form-row">
        <div class="form-group col-md-2">
            <label for="doga">DOGA</label>
            <input type="text" class="form-control" id="doga" value="{{$analisis->doga}}">
            
        </div>
        <div class="form-group col-md-2">
            <label for="boppo">BOPPO</label>
            <input type="text" class="form-control" id="boppo" value="{{$analisis->boppo}}">
        </div>
        <div class="form-group col-md-2">
            <label for="bopco">BOPCO</label>
            <input type="text" class="form-control" id="bopco" value="{{$analisis->bopco}}">
        </div>
        <div class="formgroup col-md-2">
            <label for="boplu">BOPLU</label>
            <input type="text" class="form-control" id="boplu" value="{{$analisis->boplu}}">
        </div>
        <div class="formgroup col-md-2">
            <label for="bopou">BOPOU</label>
            <input type="text" class="form-control" id="boplu" value="{{$analisis->bopou}}">
        </div>
    </div>

  <button type="submit" class="btn btn-primary">Volver</button>
</form>

</div>

@endsection

