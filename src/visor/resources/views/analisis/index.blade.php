@extends('plantilla.plantilla')

@section('scripts')
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

<table class=" table text-center" id="table-data">
    <thead>
    <tr>
        <th scope="col">
            <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                <label class="custom-control-label" for="tableDefaultCheck">#</label>
            </div>
        </th>
        <th scope="col">Fecha</th>
        <th scope="col">DOGA</th>
        <th scope="col">BOPPO</th>
        <th scope="col">BOPCO</th>
        <th scope="col">BOPLU</th>
        <th scope="col">BOPOU</th>
        <th scope="col">Creación</th>
        <th scope="col">Modificación</th>
    </tr>
    </thead>
    <tbody>
        @foreach($dias as $item)
            @php ($visto = 'table-default')

        <tr class="{{$visto}}" id="table-row-id-{{$item->id}}">
            <th scope="row">
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input control-check-j" id="tableDefaultCheck{{$item->id}}" value="{{$item->id}}" onclick="selectSingle()">
                    <label class="custom-control-label" for="tableDefaultCheck{{$item->id}}"> {{$item->id}} </label>
                </div>
            </th>
            <td class="text-left ">{{ $item->analysis_date }}</td>
            <td>{{ $item->doga  }}</td>
            <td>{{ $item->boppo }}</td>
            <td>{{ $item->bopco }}</td>
            <td>{{ $item->boplu }}</td>
            <td>{{ $item->bopou }}</td>
            <td>{{ $item->created_at }}</td>
            <td>{{ $item->updated_at }}</td>
            <td  class="align-right"> 
                <a href="{{ route('analisis.edit',$item->id) }}" class="btn btn-info btncolorblanco" >
                    <i class="far fa-edit" id="cfav-{{$item->id}}"></i>  
                </a>
                <a href=" {{ route('analisis.destroy',$item->id) }} " class="btn btn-success btncolorblanco">
                    <i class="far fa-trash-alt"></i>  
                </a>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
<div id="id_paginas">
    {{ $dias }}
</div>

</div>

{{--@include('plantilla.footer',['container'=>'container-fluid'])--}}
@endsection