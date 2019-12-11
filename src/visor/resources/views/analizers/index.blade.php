@extends('plantilla.plantilla')

@section('scripts')
<script>
            $(function(){ $('.toggle').bootstrapToggle() });
            console.debug("hago cosas");
</script>
@endsection

@section('contenido')

<div class="container-fluid registerinicio">
    <div class="row">
        <div class="col-md-6 register-left regiter-left1">
            <a href="{{ route('noticias.index') }}">
                <img src="{{asset('img/calendario.png')}}" alt=""/>
            </a>
        </div>    
        <div class="col-md-6 register-left">
            
            <h3>Bienvenid@</h3>
            <p>Revisión de boletines oficiales !</p>
            
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
<form action="">
    <input class="toggle" type="checkbox" data-toggle="toggle" checked  data-onstyle="primary">
</form>
<table class=" table text-center" id="table-data">
    <thead>
    <tr>
        <th scope="col">
            <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                <label class="custom-control-label" for="tableDefaultCheck">#</label>
            </div>
        </th>
        <th scope="col">Nombre</th>
        <th scope="col">Activo</th>
        <th scope="col">Clase</th>
        <th scope="col">Módulo</th>
        <th scope="col">Creación</th>
        <th scope="col">Actualización</th>
    </tr>
    </thead>
    <tbody>
        @foreach($analizers as $item)
            @php ($visto = 'table-default')

        <tr class="{{$visto}}" id="table-row-id-{{$item->id}}">
            <th scope="row">
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input control-check-j" id="tableDefaultCheck{{$item->id}}" value="{{$item->id}}" ">
                    <label class="custom-control-label" for="tableDefaultCheck{{$item->id}}"> {{$item->id}} </label>
                </div>
            </th>
            <td class="text-left ">{{ $item->name }}</td>
            <td>{{ $item->active  }}</td>
            <td>{{ $item->classname }}</td>
            <td>{{ $item->module }}</td>
            <td>{{ $item->created_at }}</td>
            <td>{{ $item->updated_at }}</td>
            <td  class="align-right"> 
                <a href="{{ route('analizers.edit',$item->id) }}" class="btn btn-info btncolorblanco" >
                    <i class="far fa-edit" id="cfav-{{$item->id}}"></i>  
                </a>
                <a href=" {{ route('analizers.destroy',$item->id) }} " class="btn btn-success btncolorblanco">
                    <i class="far fa-trash-alt"></i>  
                </a>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
<div id="id_paginas">
    {{ $analizers }}
</div>

</div>

{{--@include('plantilla.footer',['container'=>'container-fluid'])--}}
@endsection