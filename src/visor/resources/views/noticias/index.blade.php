@extends('plantilla.plantilla')

<script>
    function do_click (e,id)
    {
        e.preventDefault();
        $.ajax({
            data: {"_token": "{{ csrf_token() }}","id" : id},
            url: " {{ route('noticias.favorite') }}",
            type:'POST',
            dataType: 'json',
            success: function(data) {
                name = "#cfav-"+id;  

                if (data == 1)
                {
                    $(name).removeClass("far");
                    $(name).addClass("fas");
                }
                else 
                {
                    $(name).removeClass("fas");
                    $(name).addClass("far");
                }                
                console.log(data);
            }
        });
        
    }

    function send(e)
    {
        alert("enviando");
    }
</script>

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



<div class="container-fluid ">

@if ( session('datos'))
<div class="alert alert-success alert-dismissible fade show" role="alert">
    {{session('datos')}}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>    
</div>
@endif

@if ( session('cancelar'))
<div class="alert alert-danger alert-dismissible fade show" role="alert">
    {{session('cancelar')}}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>    
</div>
@endif

<br>
@php ($destacadol = ['Destacados', 'No Destacados'])
<nav class="navbar navbar-light float-right">
  <form class="form-inline">
    <select name="destacado" class="form-control mr-sm-2" id="idDestacado" onchange="this.form.submit()">
        <option>Todos</option>
        @foreach($destacadol as $des)
            <option 
            @if ($des == $destacado)
                selected
            @endif
            >{{$des}}</option>
        @endforeach
    </select>

    <select name="bulletin" class="form-control mr-sm-2" id="exampleFormControlSelect1" onchange="this.form.submit()">
      <option>Buscar por boletin</option>
      @foreach($boletines as $boletin)
      <option 
        @if ($boletin == $bulletin) 
        selected
        @endif
      >{{$boletin}}</option>
      @endforeach
    </select>

    <select name="bulletin_year" class="form-control mr-sm-2" id="idBulletinYear" onchange="this.form.submit()">
        <option>Buscar por año</option>
        @foreach ($years as $y)
            <option 
             @if ($year == $y)
              selected  
             @endif          
            >{{$y}}</option>
        @endforeach
    </select>

    <input name="bulletin_no" class="form-control mr-sm-2" type="search" placeholder="Buscar por número" aria-label="Search" value="{{$bulletin_no}}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Buscar</button>
  </form>
</nav>
   <br>
      <h1 class="text-center">Datos personales</h1>

      <br>
   <br>
<table class="table-responsive table text-center">
    <thead>
    <tr>
        <th scope="col">#</th>
        <th scope="col" style="width: 35%">Noticia</th>
        <th scope="col">Boletín</th>
        <th scope="col">Número</th>
        <th scope="col">Año</th>
        <th scope="col" style="width: 20%">Organización</th>
        <th scope="col">Creación</th>
        <th scope="col">Acción</th>
    </tr>
    </thead>
    <tbody>
        @foreach($noticias as $item)
            @php ($visto = 'table-default')
            @php ($fav = 'far fa-star')
            @if ($item->readed ==0)
                @php ($visto='table-primary')                
            @endif
            @if ($item->fav == 1)
                @php ($fav = 'fas fa-star')
            @endif

        <tr class="{{$visto}}">
            <th scope="row">{{$item->id}}</th>
            <td class="text-left "><a href="{{$item->url}}" target="_blank">{{ $item->newname }} </a></td>
            <td>{{ $item->bulletin  }}</td>
            <td>{{ $item->bulletin_no  }}</td>
            <td>{{ $item->bulletin_year  }}</td>
            <td>{{ $item->organization  }}</td>
            <td>{{ $item->created_at  }}</td>
            <td> 
                <a href="#" onclick="do_click(event,{{$item->id}})" class="btn btn-info btncolorblanco" >
                    <i class="{{$fav}}" id="cfav-{{$item->id}}"></i>  
                </a>
                <a href=" {{ route('noticias.edit',$item->id) }} " class="btn btn-success btncolorblanco">
                    <i class="fa fa-edit"></i>  
                </a>
                <a href="#" class="btn btn-danger btncolorblanco">
                    <i class="fa fa-trash-alt"></i>  
                </a>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
{{ $noticias }}

</div>

{{--@include('plantilla.footer',['container'=>'container-fluid'])--}}
@endsection