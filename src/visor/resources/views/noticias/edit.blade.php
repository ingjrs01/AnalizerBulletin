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
    <div class="form-group">
        <label for="newname">Noticia</label>
        <input type="text" class="form-control" id="newname" placeholder="1234 Main St" value="{{$noticia->newname}}">
    </div>

    <div class="form-row">
        <div class="form-group col-md-2">
            <label for="bulletin">Boletín</label>
            <input type="text" class="form-control" id="bulletin" placeholder="Boletín" value="{{$noticia->bulletin}}">
        </div>
        <div class="form-group col-md-2">
            <label for="bulletin_no">Número</label>
            <input type="text" class="form-control" id="bulletin_no" placeholder="Número" value="{{$noticia->bulletin_no}}">
        </div>
        <div class="form-group col-md-2">
            <label for="bulletin_year">Año</label>
            <input type="text" class="form-control" id="bulletin_year" placeholder="Año" value="{{$noticia->bulletin_year}}">
        </div>

        <div class="formgroup col-md-6">
            <label for="organization">Organización</label>
            <input type="text" class="form-control" id="organization" placeholder="Organización" value="{{$noticia->organization}}">
        </div>
    </div>

  <div class="form-group">
    <label for="inputAddress2">Address 2</label>
    <input type="text" class="form-control" id="inputAddress2" placeholder="Apartment, studio, or floor">
  </div>
  <div class="form-row">
    <div class="form-group col-md-6">
      <label for="inputCity">City</label>
      <input type="text" class="form-control" id="inputCity">
    </div>
    <div class="form-group col-md-4">
      <label for="inputState">State</label>
      <select id="inputState" class="form-control">
        <option selected>Choose...</option>
        <option>...</option>
      </select>
    </div>
    <div class="form-group col-md-2">
      <label for="inputZip">Zip</label>
      <input type="text" class="form-control" id="inputZip">
    </div>
  </div>
  <div class="form-group">
    <div class="form-check">
      <input class="form-check-input" type="checkbox" id="gridCheck">
      <label class="form-check-label" for="gridCheck">
        Check me out
      </label>
    </div>
  </div>
  <button type="submit" class="btn btn-primary">Volver</button>
</form>

</div>

@endsection

